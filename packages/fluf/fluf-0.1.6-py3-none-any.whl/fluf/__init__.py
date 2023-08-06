
import argparse
import atexit
from collections import defaultdict, namedtuple
from functools import partial
from hashlib import sha256
import inspect
import logging
import os
import pickle
import socket
import sqlite3
import sys

import dill
import matplotlib.pyplot as plt


lgr = logging.getLogger('FLUF')
lgr_memcache = logging.getLogger('FLUF.memcache')
lgr_callstack = logging.getLogger('FLUF.callstack')

lgr.setLevel(logging.INFO)
lgr_memcache.setLevel(logging.INFO)
lgr_callstack.setLevel(logging.INFO)

flufcall = namedtuple('FlufCall', ['name', 'objhash', 'callhash'])


# globals
WORKFOLDER = 'fluf'
DEFAULTPUBLISH = True
HASHLEN = 10
MEMCACHE = defaultdict(list)
OBJHASHES = set()
CACHENAMES = set()
PUBLISHED = []
CALLHISTORY = []

# fluf workflows are meant to be simple - so one main script is responsible
# the checksum of that script is the call database
callscript = os.path.abspath(os.path.expanduser(sys.argv[0]))
scripthash = sha256()
scripthash.update(socket.gethostname().encode())
scripthash.update(callscript.encode())
scripthash = scripthash.hexdigest()[:HASHLEN]
lgr.debug("Script: %s scripthash %s", callscript, scripthash)
fluffolder = os.path.join(os.path.expanduser('~'), '.cache', 'fluf')
if not os.path.exists(fluffolder):
    os.makedirs(fluffolder)

calldbname = os.path.join(fluffolder, f"{scripthash}.db")
dbconn = sqlite3.connect(calldbname)
dbcursor = dbconn.cursor()
dbcursor.execute('''CREATE TABLE IF NOT EXISTS calls
                   (caller_name text,
                    caller_objhash text,
                    caller_callhash text,
                    called_name text,
                    called_objhash text,
                    called_callhash text) ''')


def exit_handler():
    lgr.info("closing db")
    dbconn.commit()
    dbconn.close()


atexit.register(exit_handler)


#
# fluf configuration
#

def set_workfolder(workfolder):
    global WORKFOLDER
    if len(OBJHASHES) > 0:
        print("Must set workfolder before any fluf definitions")
        exit()
    WORKFOLDER = workfolder


def set_defaultpublish(publish):
    global DEFAULTPUBLISH
    DEFAULTPUBLISH = publish


def pickle_loader(filename):
    with open(filename, 'rb') as F:
        return pickle.load(F)


def pickle_saver(obj, filename):
    with open(filename, 'wb') as F:
        pickle.dump(obj, F, protocol=4)


def mpl_saver(obj, filename):
    if obj is None:
        obj = plt.gcf()
    lgr.info("saving image to %s", filename)
    obj.savefig(filename, format='png', bbox_inches='tight')
    plt.close()


def mpl_loader(filename):
    """ we really never want to load an image again """
    return None


def txt_saver(obj, filename):
    with open(filename, 'w') as F:
        F.write(obj)


def txt_loader(filename):
    with open(filename) as F:
        return F.read()


def get_obj_hash(func):
    """ Calculate a per function call specific hash """
    hasher = sha256()
    func_code = inspect.getsource(func).strip()
    hasher.update(dill.dumps(func_code))
    objhash = hasher.hexdigest()[:HASHLEN]

    lgr.debug(f"function hash for {func.__name__} call is {objhash}")

    return objhash


def get_call_hash(objhash, args, kwargs):

    hasher = sha256()
    hasher.update(objhash.encode())

    for a in args:
        hasher.update(dill.dumps(a))

    for (k, v) in sorted(kwargs.items()):
        hasher.update(dill.dumps(k))
        hasher.update(dill.dumps(v))

    callhash = hasher.hexdigest()[:HASHLEN]
    lgr.debug(f"call hash with func {objhash}: {callhash}")

    return callhash


#
# MEMCACHE
#

def insert_memcache(objhash, callhash, rv):
    global MEMCACHE
    lgr_memcache.debug(f"Insert into memcache: {objhash}/{callhash}")
    MEMCACHE[objhash].append((callhash, rv))


def from_memcache(objhash, callhash):
    for k, v in MEMCACHE[objhash]:
        if k == callhash:
            lgr_memcache.debug(
                f"Returning from memcache: {objhash}/{callhash}")
            return v


def in_memcache(objhash, callhash):
    lgr_memcache.debug('check objhash/callhash in memcache: %s/%s',
                       objhash, callhash)
    if objhash in MEMCACHE:
        for a, b in MEMCACHE[objhash]:
            if a == callhash:
                lgr_memcache.debug(f"Found in memcache: {objhash}/{callhash}")
                return True
    else:
        lgr_memcache.debug(f"Not in memcache: {objhash}/{callhash}")
        return False


def publish_file(cachefilename, pubfilename):
    """ publish a file - e.g. - hardlink from the cache
        folder to the workfolder
    """
    if os.path.exists(pubfilename):
        os.unlink(pubfilename)
    os.link(cachefilename, pubfilename)


def cache(cachename=None,
          extension='pkl',
          loader=pickle_loader,
          saver=pickle_saver,
          publish=None,
          cache=True,
          diskcache=True,
          memcache=8):

    workfolder = WORKFOLDER
    cachefolder = os.path.join(WORKFOLDER, 'fluf')
    if publish is None:
        publish = DEFAULTPUBLISH

    if not os.path.exists(cachefolder):
        os.makedirs(cachefolder)

    def cache_decorator(func):

        objhash = get_obj_hash(func)
        OBJHASHES.add(objhash)

        def _fluf_func_wrapper(*args, **kwargs):

            callhash = get_call_hash(objhash, args, kwargs)

            publish_this_call = kwargs.get('_publish', publish)

            if '_cachename' in kwargs:
                basename = kwargs['_cachename']
            elif cachename is None:
                basename = func.__name__
                if cachename in CACHENAMES:
                    i = 0
                    while f"{cachename}{i:03d}" in CACHENAMES:
                        i += 1
                    basename = f"{cachename}{i:03d}"
            else:
                basename = cachename

            CACHENAMES.add(basename)

            this_function_call = flufcall(name=basename, objhash=objhash,
                                          callhash=callhash)
            cfbase = callhash + '.' + basename + '.' + extension
            pubname = basename + '.' + extension
            cachefilename = os.path.join(cachefolder, cfbase)
            pubfilename = os.path.join(workfolder, pubname)

            if publish_this_call:
                if pubfilename in PUBLISHED:
                    lgr.critical("Duplicate publish name - " +
                                 "they will be overwritten")

            lgr.debug(f"final cache file name is {cachefilename}")

            insert_call_into_stack(this_function_call)

            if cache:
                # we do try to use the cache

                if in_memcache(objhash, callhash):
                    lgr.info("<M Return from memcache %s obj:%s call:%s",
                             basename, objhash, callhash)
                    # if already im memcache - we assume the file was
                    # published - so do not check here
                    return from_memcache(objhash, callhash)

                if diskcache:
                    # attempt retrieval from diskache

                    diskcache_exist = os.path.exists(cachefilename)
                    diskcache_notzero = os.stat(cachefilename).st_size > 0 \
                        if diskcache_exist else False

                    diskcache_callstack = check_call_stack(this_function_call)

                if not diskcache_exist:
                    lgr.debug("Not using diskcache - cachefile does not exist")
                elif not diskcache_notzero:
                    lgr.debug("Not using diskcache - cachefile is empty")
                elif not diskcache_callstack:
                    lgr.debug("Not using diskcache - callstack changed")

                if (diskcache_exist \
                    and diskcache_notzero \
                    and diskcache_callstack):

                    lgr.info("<D Return from diskcache: %s obj:%s call:%s",
                             basename, objhash, callhash)
                    rv = loader(cachefilename)
                    insert_memcache(objhash, callhash, rv)

                    if publish_this_call:
                        publish_file(cachefilename, pubfilename)
                    return rv

            lgr.info("<R (re)running function: %s obj:%s call:%s", basename, objhash, callhash)
            lgr.debug('#### Run function: %s %s %s', func.__name__,
                      objhash, callhash)

            # when calling this function - see what is called
            # so we can recall later if all parent bits have not
            # changed

            rv = func(*args, **kwargs)
            if cache and diskcache and cachefilename is not None:
                lgr.debug("caching to: %s", cachefilename)
                saver(rv, cachefilename)
            insert_memcache(objhash, callhash, rv)
            if publish_this_call:
                publish_file(cachefilename, pubfilename)
            return rv

        return _fluf_func_wrapper
    return cache_decorator


INSERT_SQL = '''
INSERT INTO calls (caller_name, caller_objhash, caller_callhash,
                   called_name, called_objhash, called_callhash)
SELECT ?, ?, ?, ?, ?, ?
WHERE NOT EXISTS(SELECT 1
                   FROM calls
                  WHERE caller_name = ?
                  AND caller_objhash = ?
                  AND caller_callhash = ?
                  AND called_name = ?
                  AND called_objhash = ?
                  AND called_callhash = ?)
'''


def insert_call_into_stack(called_function):
    # we also store the 'self' call - if we do not find the self call -
    # then we have no record of this function running - need rerun
    for frameinfo in inspect.stack()[:]:
        frameloc = frameinfo.frame.f_locals
        #print('--', called_function.name, 'called by', frameinfo.function)
        if frameinfo.function == '_fluf_func_wrapper':
            caller_function = flufcall(name=frameloc['basename'],
                                       objhash=frameloc['objhash'],
                                       callhash=frameloc['callhash'])
            save_to_callstack(caller_function, called_function)
            # only store immediate caller
            break


def save_to_callstack(caller_function, called_function):

    # check if the call
    lgr_callstack.debug('insert into callstack %s called %s',
                        caller_function.name, called_function.name)

    #print("~~~~INSERT", caller_function, called_function)
    dbcursor.execute(INSERT_SQL,
                     (caller_function.name, caller_function.objhash,
                      caller_function.callhash, called_function.name,
                      called_function.objhash, called_function.callhash,
                      caller_function.name, caller_function.objhash,
                      caller_function.callhash, called_function.name,
                      called_function.objhash, called_function.callhash))

    dbconn.commit()


def get_called(caller):

    for rec in dbcursor.execute(
            """SELECT called_name, called_objhash, called_callhash
               FROM calls
               WHERE caller_objhash = ?
               AND caller_callhash = ?""",
            (caller.objhash, caller.callhash)):

        called = flufcall(name=rec[0], objhash=rec[1], callhash=rec[2])
        yield caller.name, called
        if caller.objhash != called.objhash:
            yield from get_called(called)


def check_call_stack(caller):

    lgr_callstack.debug('$ check callstack for call "%s" obj:%s call:%s ',
                        caller.name, caller.objhash, caller.callhash)

    nothing_changed = True
    self_call_found = False

    for _cn, called in get_called(caller):
        # print('!!!!', caller.name, _cn, called.name, called.objhash)
        if called.objhash == caller.objhash:
            # ~~~ should alwasy be there
            self_call_found = True
        function_still_present = called.objhash in OBJHASHES
        if function_still_present:
            lgr_callstack.debug(
                "  - called %s obj:%s still ok",
                                called.name, called.objhash)
        else:
            lgr_callstack.info("!Change in callstack for %s: %s obj:%s !!!",
                               caller.name, called.name, called.objhash)
            nothing_changed = False
            # remove this caller record from callstack
            # the stack is not complete - so need to rerun
            dbcursor.execute(
                """DELETE FROM calls
                         WHERE caller_objhash = ?
                           AND caller_callhash = ?
                           AND called_objhash = ? """,
                (caller.objhash, caller.callhash, called.objhash))
            break

    if not self_call_found:
        return False
        # unsure if this should be the case - but we cannot validate that the
        # callstack has changed - so best advise rerun
        return False

    # else - if no called code has changed - keep it as is
    return nothing_changed


mplcache = partial(cache, extension='png', loader=mpl_loader, saver=mpl_saver)
txtcache = partial(cache, extension='txt', loader=txt_loader, saver=txt_saver)
