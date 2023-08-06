#
# Module providing various facilities to other parts of the package
#
# multiprocessing/util.py
#
# Copyright (c) 2006-2008, R Oudkerk
# Licensed to PSF under a Contributor Agreement.
#
# Modifications Copyright (c) 2020 Cloudlab URV
#

import os
import itertools
import sys
import weakref
import atexit
import redis
import uuid
import threading  # we want threading to install it's cleanup function before multiprocessing does
from . import process
import logging
import lithops
from lithops.config import default_config

#
# Logging
#

NOTSET = 0
SUBDEBUG = 5
DEBUG = 10
INFO = 20
SUBWARNING = 25

_logger = logging.getLogger(lithops.__name__)
_log_to_stderr = False


def sub_debug(msg, *args):
    if _logger:
        _logger.log(SUBDEBUG, msg, *args)


def debug(msg, *args):
    if _logger:
        _logger.log(DEBUG, msg, *args)


def info(msg, *args):
    if _logger:
        _logger.log(INFO, msg, *args)


def sub_warning(msg, *args):
    if _logger:
        _logger.log(SUBWARNING, msg, *args)


def get_logger():
    return _logger


def log_to_stderr():
    raise NotImplementedError()


#
# Function returning a temp directory which will be removed on exit
#

def get_temp_dir():
    # get name of a temp directory which will be automatically cleaned up
    tempdir = process.current_process()._config.get('tempdir')
    if tempdir is None:
        import shutil, tempfile
        tempdir = tempfile.mkdtemp(prefix='pymp-')
        info('created temp directory %s', tempdir)
        Finalize(None, shutil.rmtree, args=[tempdir], exitpriority=-100)
        process.current_process()._config['tempdir'] = tempdir
    return tempdir


#
# Support for reinitialization of objects when bootstrapping a child process
#

_afterfork_registry = weakref.WeakValueDictionary()
_afterfork_counter = itertools.count()


def _run_after_forkers():
    items = list(_afterfork_registry.items())
    items.sort()
    for (index, ident, func), obj in items:
        try:
            func(obj)
        except Exception as e:
            info('after forker raised exception %s', e)


def register_after_fork(obj, func):
    _afterfork_registry[(next(_afterfork_counter), id(obj), func)] = obj


#
# Finalization using weakrefs
#

_finalizer_registry = {}
_finalizer_counter = itertools.count()


class Finalize(object):
    """
    Class which supports object finalization using weakrefs
    """

    def __init__(self, obj, callback, args=(), kwargs=None, exitpriority=None):
        assert exitpriority is None or type(exitpriority) is int

        if obj is not None:
            self._weakref = weakref.ref(obj, self)
        else:
            assert exitpriority is not None

        self._callback = callback
        self._args = args
        self._kwargs = kwargs or {}
        self._key = (exitpriority, next(_finalizer_counter))
        self._pid = os.getpid()

        _finalizer_registry[self._key] = self

    def __call__(self, wr=None,
                 # Need to bind these locally because the globals can have
                 # been cleared at shutdown
                 _finalizer_registry=_finalizer_registry,
                 sub_debug=sub_debug, getpid=os.getpid):
        """
        Run the callback unless it has already been called or cancelled
        """
        try:
            del _finalizer_registry[self._key]
        except KeyError:
            sub_debug('finalizer no longer registered')
        else:
            if self._pid != getpid():
                sub_debug('finalizer ignored because different process')
                res = None
            else:
                sub_debug('finalizer calling %s with args %s and kwargs %s',
                          self._callback, self._args, self._kwargs)
                res = self._callback(*self._args, **self._kwargs)
            self._weakref = self._callback = self._args = \
                self._kwargs = self._key = None
            return res

    def cancel(self):
        """
        Cancel finalization of the object
        """
        try:
            del _finalizer_registry[self._key]
        except KeyError:
            pass
        else:
            self._weakref = self._callback = self._args = \
                self._kwargs = self._key = None

    def still_active(self):
        '''
        Return whether this finalizer is still waiting to invoke callback
        '''
        return self._key in _finalizer_registry

    def __repr__(self):
        try:
            obj = self._weakref()
        except (AttributeError, TypeError):
            obj = None

        if obj is None:
            return '<%s object, dead>' % self.__class__.__name__

        x = '<%s object, callback=%s' % (
            self.__class__.__name__,
            getattr(self._callback, '__name__', self._callback))
        if self._args:
            x += ', args=' + str(self._args)
        if self._kwargs:
            x += ', kwargs=' + str(self._kwargs)
        if self._key[0] is not None:
            x += ', exitprority=' + str(self._key[0])
        return x + '>'


def _run_finalizers(minpriority=None):
    """
    Run all finalizers whose exit priority is not None and at least minpriority
    Finalizers with highest priority are called first; finalizers with
    the same priority will be called in reverse order of creation.
    """
    if _finalizer_registry is None:
        # This function may be called after this module's globals are
        # destroyed.  See the _exit_function function in this module for more
        # notes.
        return

    if minpriority is None:
        f = lambda p: p[0] is not None
    else:
        f = lambda p: p[0] is not None and p[0] >= minpriority

    # Careful: _finalizer_registry may be mutated while this function
    # is running (either by a GC run or by another thread).

    # list(_finalizer_registry) should be atomic, while
    # list(_finalizer_registry.items()) is not.
    keys = [key for key in list(_finalizer_registry) if f(key)]
    keys.sort(reverse=True)

    for key in keys:
        finalizer = _finalizer_registry.get(key)
        # key may have been removed from the registry
        if finalizer is not None:
            sub_debug('calling %s', finalizer)
            try:
                finalizer()
            except Exception:
                import traceback
                traceback.print_exc()

    if minpriority is None:
        _finalizer_registry.clear()


#
# Clean up on exit
#

def is_exiting():
    '''
    Returns true if the process is shutting down
    '''
    return _exiting or _exiting is None


_exiting = False


# def _exit_function(info=info, debug=debug, _run_finalizers=_run_finalizers,
#                    active_children=process.active_children,
#                    current_process=process.current_process):
#     # We hold on to references to functions in the arglist due to the
#     # situation described below, where this function is called after this
#     # module's globals are destroyed.
#
#     global _exiting
#
#     if not _exiting:
#         _exiting = True
#
#         info('process shutting down')
#         debug('running all "atexit" finalizers with priority >= 0')
#         _run_finalizers(0)
#
#         if current_process() is not None:
#             # We check if the current process is None here because if
#             # it's None, any call to ``active_children()`` will raise
#             # an AttributeError (active_children winds up trying to
#             # get attributes from util._current_process).  One
#             # situation where this can happen is if someone has
#             # manipulated sys.modules, causing this module to be
#             # garbage collected.  The destructor for the module type
#             # then replaces all values in the module dict with None.
#             # For instance, after setuptools runs a test it replaces
#             # sys.modules with a copy created earlier.  See issues
#             # #9775 and #15881.  Also related: #4106, #9205, and
#             # #9207.
#
#             for p in active_children():
#                 if p.daemon:
#                     info('calling terminate() for daemon %s', p.name)
#                     p._popen.terminate()
#
#             for p in active_children():
#                 info('calling join() for process %s', p.name)
#                 p.join()
#
#         debug('running the remaining "atexit" finalizers')
#         _run_finalizers()
#
#
# atexit.register(_exit_function)


#
# Some fork aware types
#

class ForkAwareThreadLock(object):
    def __init__(self):
        self._reset()
        register_after_fork(self, ForkAwareThreadLock._reset)

    def _reset(self):
        self._lock = threading.Lock()
        self.acquire = self._lock.acquire
        self.release = self._lock.release

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return self._lock.__exit__(*args)


class ForkAwareLocal(threading.local):
    def __init__(self):
        register_after_fork(self, lambda obj: obj.__dict__.clear())

    def __reduce__(self):
        return type(self), ()


#
# Close fds except those specified
#

try:
    MAXFD = os.sysconf("SC_OPEN_MAX")
except Exception:
    MAXFD = 256


def close_all_fds_except(fds):
    fds = list(fds) + [-1, MAXFD]
    fds.sort()
    assert fds[-1] == MAXFD, 'fd too large'
    for i in range(len(fds) - 1):
        os.closerange(fds[i] + 1, fds[i + 1])


#
# Close sys.stdin and replace stdin with os.devnull
#

def _close_stdin():
    if sys.stdin is None:
        return

    try:
        sys.stdin.close()
    except (OSError, ValueError):
        pass

    try:
        fd = os.open(os.devnull, os.O_RDONLY)
        try:
            sys.stdin = open(fd, closefd=False)
        except:
            os.close(fd)
            raise
    except (OSError, ValueError):
        pass


#
# Flush standard streams, if any
#

def _flush_std_streams():
    try:
        sys.stdout.flush()
    except (AttributeError, ValueError):
        pass
    try:
        sys.stderr.flush()
    except (AttributeError, ValueError):
        pass


#
# Start a program with only specified fds kept open
#

def spawnv_passfds(path, args, passfds):
    import _posixsubprocess
    passfds = tuple(sorted(map(int, passfds)))
    errpipe_read, errpipe_write = os.pipe()
    try:
        return _posixsubprocess.fork_exec(
            args, [os.fsencode(path)], True, passfds, None, None,
            -1, -1, -1, -1, -1, -1, errpipe_read, errpipe_write,
            False, False, None)
    finally:
        os.close(errpipe_read)
        os.close(errpipe_write)


#
# Picklable redis client
#

class PicklableRedis(redis.StrictRedis):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        super().__init__(*self._args, **self._kwargs)

    def __getstate__(self):
        return self._args, self._kwargs

    def __setstate__(self, state):
        self.__init__(*state[0], **state[1])


def get_redis_client(**overwrites):
    conn_params = default_config()['redis']
    conn_params.update(overwrites)
    return PicklableRedis(**conn_params)


#
# Unique id for redis keys/hashes
#

def get_uuid(length=12):
    return uuid.uuid1().hex[:length]


#
# Make stateless redis Lua script (redis.client.Script)
# Just to ensure no redis client is cache'd and avoid 
# creating another connection when unpickling this object.
#

def make_stateless_script(script):
    script.registered_client = None
    return script


#
# object for counting remote references (redis keys)
# and garbage collect them automatically when nothing
# is pointing at them
#

class RemoteReference:

    def __init__(self, referenced, managed=False, client=None):
        if isinstance(referenced, str):
            referenced = [referenced]
        if not isinstance(referenced, list):
            raise TypeError("referenced must be a key (str) or"
                            "a list of keys")
        self._referenced = referenced

        # reference counter key
        self._rck = '{}-{}'.format('ref', self._referenced[0])
        self._referenced.append(self._rck)
        self._client = client or get_redis_client()

        self._callback = None
        self.managed = managed

    @property
    def managed(self):
        return self._callback is None

    @managed.setter
    def managed(self, value):
        managed = value

        if self._callback is not None:
            self._callback.atexit = False
            self._callback.detach()

        if managed:
            self._callback = None
        else:
            self._callback = weakref.finalize(self, type(self)._finalize,
                                              self._client, self._rck, self._referenced)

    def __getstate__(self):
        return (self._rck, self._referenced,
                self._client, self.managed)

    def __setstate__(self, state):
        (self._rck, self._referenced,
         self._client) = state[:-1]
        self._callback = None
        self.managed = state[-1]
        self.incref()

    def incref(self):
        if not self.managed:
            return int(self._client.incr(self._rck, 1))

    def decref(self):
        if not self.managed:
            return int(self._client.decr(self._rck, 1))

    def refcount(self):
        count = self._client.get(self._rck)
        return 1 if count is None else int(count) + 1

    def collect(self):
        if len(self._referenced) > 0:
            self._client.delete(*self._referenced)
            self._referenced = []

    @staticmethod
    def _finalize(client, rck, referenced):
        count = int(client.decr(rck, 1))
        if count < 0 and len(referenced) > 0:
            client.delete(*referenced)
