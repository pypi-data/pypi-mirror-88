#!/usr/bin/env python

import sys
import time

import radical.utils as ru
import radical.pilot as rp

glyphs = {
          rp.NEW                          : '#',
          rp.UMGR_SCHEDULING_PENDING      : '.',
          rp.UMGR_SCHEDULING              : '.',
          rp.UMGR_STAGING_INPUT_PENDING   : '.',
          rp.UMGR_STAGING_INPUT           : '.',
          rp.AGENT_STAGING_INPUT_PENDING  : '_',
          rp.AGENT_STAGING_INPUT          : '_',
          rp.AGENT_SCHEDULING_PENDING     : '_',
          rp.AGENT_SCHEDULING             : '_',
          rp.AGENT_EXECUTING_PENDING      : '@',
          rp.AGENT_EXECUTING              : '@',
          rp.AGENT_STAGING_OUTPUT_PENDING : '=',
          rp.AGENT_STAGING_OUTPUT         : '=',
          rp.UMGR_STAGING_OUTPUT_PENDING  : '=',
          rp.UMGR_STAGING_OUTPUT          : '=',
          rp.DONE                         : '+',
          rp.FAILED                       : '-',
          rp.CANCELED                     : 'x'
         }


def listen(topic, msgs):

    try:
        for msg in ru.as_list(msgs):
            if msg['cmd'] == 'update':
                for thing in msg['arg']:

                    uid   = thing['uid']
                    state = thing['state']

                  # print('%-20s: %s' % (uid, state))

                    if 'pilot' in uid:
                        cores = thing.get('description', {'cores':'?'}) \
                                     .get('cores')
                        print('\n%s [%s]: %s' % (uid, cores, state))

                    elif 'unit' in uid:
                        print(glyphs[state], end='')
    except Exception as e:
        print(e)


cfg = ru.read_json('%s/state_pubsub.cfg' % sys.argv[1])
sub = ru.zmq.Subscriber('state_pubsub', url=cfg['sub'])
sub.subscribe(topic='state_pubsub', cb=listen)

time.sleep(100000)

