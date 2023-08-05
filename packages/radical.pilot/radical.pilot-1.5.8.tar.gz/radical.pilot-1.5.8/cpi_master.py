#!/usr/bin/env python3

import os
import sys
import time
import signal

import threading     as mt

import radical.pilot as rp
import radical.utils as ru


# This script has to run as a task within an pilot allocation, and is
# a demonstration of a task overlay within the RCT framework.
# It will:
#
#   - create a master which bootstrappes a specific communication layer
#   - insert n workers into the pilot (again as a task)
#   - perform RPC handshake with those workers
#   - send RPC requests to the workers
#   - terminate the worker
#
# The worker itself is an external program which is not covered in this code.


# ------------------------------------------------------------------------------
#
class Request(object):

    # poor man's future
    # TODO: use proper future implementation


    # --------------------------------------------------------------------------
    #
    def __init__(self, work):

        self._uid    = ru.generate_id('request')
        self._work   = work
        self._state  = 'NEW'
        self._result = None


    # --------------------------------------------------------------------------
    #
    @property
    def uid(self):
        return self._uid


    @property
    def state(self):
        return self._state


    @property
    def result(self):
        return self._result


    # --------------------------------------------------------------------------
    #
    def as_dict(self):

        return {'uid'   : self._uid,
                'state' : self._state,
                'result': self._result,
                'call'  : self._work['call'],
                'args'  : self._work['args'],
                'kwargs': self._work['kwargs'],
               }


    # --------------------------------------------------------------------------
    #
    def set_result(self, result, error):

        self._result = result
        self._error  = error

        if error: self._state = 'FAILED'
        else    : self._state = 'DONE'


    # --------------------------------------------------------------------------
    #
    def wait(self):

        while self.state not in ['DONE', 'FAILED']:
            time.sleep(1)

        return self._result


# ------------------------------------------------------------------------------
#
class MyMaster(rp.agent.Master):

    # --------------------------------------------------------------------------
    #
    def __init__(self):

        self._pwd      = os.getcwd()
        self._requests = dict()
        self._lock     = mt.Lock()

        rp.agent.Master.__init__(self)

        req_cfg = ru.Config(cfg={'channel'    : 'mw_req',
                                 'type'       : 'queue',
                                 'uid'        : self._uid + '.req',
                                 'path'       : self._pwd,
                                 'stall_hwm'  : 0,
                                 'bulk_size'  : 0})

        res_cfg = ru.Config(cfg={'channel'    : 'mw_res',
                                 'type'       : 'queue',
                                 'uid'        : self._uid + '.res',
                                 'path'       : self._pwd,
                                 'stall_hwm'  : 0,
                                 'bulk_size'  : 0})

        self._req_queue = ru.zmq.Queue(req_cfg)
        self._res_queue = ru.zmq.Queue(res_cfg)

        self._req_queue.start()
        self._res_queue.start()

        time.sleep(1)

        self._req_addr_put = str(self._req_queue.addr_put)
        self._req_addr_get = str(self._req_queue.addr_get)

        self._res_addr_put = str(self._res_queue.addr_put)
        self._res_addr_get = str(self._res_queue.addr_get)

        self._req_put = ru.zmq.Putter('mw_req', self._req_addr_put)
        self._res_get = ru.zmq.Getter('mw_res', self._res_addr_get,
                                                cb=self.result_cb)

        time.sleep(1)


    # --------------------------------------------------------------------------
    #
    @property
    def mw_addr_put(self):
        return self._mw_addr_put


    @property
    def mw_addr_get(self):
        return self._mw_addr_get


    # --------------------------------------------------------------------------
    #
    def submit(self, count=1):

        # FIXME: hardcoded, should be client_sandbox
        script = '%s/cpi_worker.py' % '/home/merzky/radical/radical.pilot.test'
        info   = {'req_addr_get': self._req_addr_get,
                  'res_addr_put': self._res_addr_put}

        return rp.agent.Master.submit(self, script, info, count)


    # --------------------------------------------------------------------------
    #
    def request(self, call, *args, **kwargs):

        req = Request(work={'call'  : call,
                            'args'  : args,
                            'kwargs': kwargs})
        with self._lock:
            self._requests[req.uid] = req

        self._req_put.put(req.as_dict())

        return req


    # --------------------------------------------------------------------------
    #
    def result_cb(self, msg):

        self._log.debug(' ==== got result msg: %s', msg)
        uid = msg['req']
        res = msg['res']
        err = msg['err']
        self._requests[uid].set_result(res, err)


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    start = time.time()
    print('hi')

    master = MyMaster()
        # FIXME: path

    pwd = os.path.dirname(__file__)
    master.submit(count=64)
    master.wait(count=64)

    print(len(master.workers))

    req = list()
    for n in range(1024 * 32):
        print('req hello %s' % n)
        req.append(master.request('hello', n))

    for r in req:
        r.wait()
        print(r.result)

    stop = time.time()
    print('all done: %2f' % (stop - start))
    os.kill(os.getpid(), signal.SIGKILL)
    os.kill(os.getpid(), signal.SIGTERM)


# ------------------------------------------------------------------------------

