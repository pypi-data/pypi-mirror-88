#!/usr/bin/env python3

import random

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    with rp.Session() as session:

        pmgr    = rp.PilotManager(session=session)
        pd_init = {'resource'      : 'local.localhost',
                   'runtime'       : 60,
                   'exit_on_error' : True,
                   'cores'         : 1024 * 42
                  }
        pdesc = rp.ComputePilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)

        print(pilot.rpc(rpc='prep_env', args=['world']))


# ------------------------------------------------------------------------------

