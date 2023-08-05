#!/usr/bin/env python

import random

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    with rp.Session() as session:

        pmgr    = rp.PilotManager(session=session)
        pd_init = {'resource'      : 'debug.summit',
                   'runtime'       : 60,
                   'exit_on_error' : True,
                   'cores'         : 1024 * 42
                  }
        pdesc = rp.ComputePilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)
        umgr  = rp.UnitManager(session=session)
        umgr.add_pilots(pilot)

        n    = 1024 * 32
        cuds = list()
        for i in range(0, n):

            cud = rp.ComputeUnitDescription()
          # cud.executable       = '%s/examples/hello_rp.sh' % os.getcwd()
            cud.executable       = '/bin/sleep',
            cud.arguments        = [random.randint(1, 30) * 1]
            cud.gpu_processes    = random.choice([0, 0, 0, 0, 0, 1, 1, 2, 3])
            cud.cpu_processes    = random.randint(1, 16)
            cud.cpu_threads      = random.randint(1, 8)
            cud.gpu_process_type = rp.MPI
            cud.cpu_process_type = rp.MPI
            cud.cpu_thread_type  = rp.OpenMP
            cuds.append(cud)

        umgr.submit_units(cuds)
        umgr.wait_units()


# ------------------------------------------------------------------------------

