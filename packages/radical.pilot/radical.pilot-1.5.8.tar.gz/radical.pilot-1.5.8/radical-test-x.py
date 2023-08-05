#!/usr/bin/env python3

import time
import radical.pilot as rp


try:
    session = rp.Session()

    pmgr  = rp.PilotManager(session=session)
    pdesc = rp.ComputePilotDescription({
    	'resource': 'local.debug',
    	'runtime': 60,
    	'cores': 1
    })

    pilots = pmgr.submit_pilots([pdesc] * 4)

    while True:

        time.sleep(1)

        states = [p.state for p in pilots]
        print(states)

        if rp.PMGR_ACTIVE in states:

            time.sleep(60)

            states = [p.state for p in pilots]
            print(states)
            assert(len(set(states)) == 1), states
            break

except:
    session.close(download=False)
    raise


