#!/usr/bin/env python3

import logging

from configator.engine.publisher import SettingPublisher

LOG = logging.getLogger(__name__)

class SandboxManager():
    def __init__(self, *args, **kwargs):
        self.__publisher = SettingPublisher()
    #
    #
    def close(self):
        self.__publisher.close()
    #
    #
    def filter_command(self, channel_type, msg_text):
        if msg_text.startswith("join"):
            parts = msg_text.split()
            if len(parts) >= 3 and parts[1] == 'sandbox' and parts[0] == 'join':
                self.join_sandbox(from_code, parts[2])
        if msg_text.startswith("quit") or msg_text.startswith("leave"):
            parts = msg_text.split()
            if len(parts) >= 2 and parts[1] == 'sandbox' and parts[0] in ['quit', 'leave']:
                self.stop_sandbox(from_code)
    #
    #
    def join_sandbox(self, speaker_code, upstream_name):
        payload = { speaker_code: upstream_name }
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, 'SandboxManager.join_sandbox: %s', str(payload))
        err = self.__publisher.publish(payload, label='PROXY_JOIN_SANDBOX')
        if err:
            print(str(err))
    #
    #
    def stop_sandbox(self, speaker_code):
        payload = [ speaker_code ]
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, 'SandboxManager.stop_sandbox: %s', str(payload))
        err = self.__publisher.publish(payload, label='PROXY_STOP_SANDBOX')
        if err:
            print(str(err))
