#!/usr/bin/env python3

import sys
import time

import radical.utils       as ru
import radical.pilot.agent as rp_to


# ------------------------------------------------------------------------------
#
class MyWorker(rp_to.Worker):

    # --------------------------------------------------------------------------
    #
    def __init__(self, cfg):

        rp_to.Worker.__init__(self, cfg)


    # --------------------------------------------------------------------------
    #
    def initialize(self):

      # self._register_method('hello', self.hello)

        self._req_get = ru.zmq.Getter('mw_req', self._info.req_addr_get,
                                                cb=self.request_cb)
        self._res_put = ru.zmq.Putter('mw_res', self._info.res_addr_put)

        return {'foo': 'bar'}


    # --------------------------------------------------------------------------
    #
    def request_cb(self, msg):

        self._log.debug(' ==== got request: %s' % msg)

        if msg['call'] == 'hello':
            res = {'req': msg['uid'],
                   'res': self.hello(*msg['args'], **msg['kwargs']),
                   'err': None}
            self._res_put.put(res)

        else:
            res = {'req': msg['uid'],
                   'res': None,
                   'err': 'no such call %s' % msg['call']}
            self._res_put.put(res)



    # --------------------------------------------------------------------------
    #
    def hello(self, req):

        return 'hello %s @ %s' % (req, time.time())



# ------------------------------------------------------------------------------
#
if __name__ == '__main__':


    worker = MyWorker(sys.argv[1])
    worker.run()


# ------------------------------------------------------------------------------

