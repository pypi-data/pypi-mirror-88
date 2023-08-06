#!/usr/bin/env python3

import logging
import os

from configator.engine.subscriber import SettingSubscriber
from configator.utils.function import match_by_label, transform_json_data
from urllib import parse as urlparse
from sockoutlet.utils.object_util import json_loads, json_dumps
from sockoutlet.utils.string_util import stringToArray


LOG = logging.getLogger(__name__)


class SandboxStorage():
    def __init__(self, *args, **kwargs):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, 'Initialize the SandboxStorage')
        self.__subscriber = SettingSubscriber()
        self.__subscriber.set_transformer(transform_json_data)
        self.__subscriber.add_event_handler(match_by_label(b'PROXY_JOIN_SANDBOX'), self.on_join_sandbox)
        self.__subscriber.add_event_handler(match_by_label(b'PROXY_STOP_SANDBOX'), self.on_quit_sandbox)
        if os.getenv('REDANT_PROXY_SANDBOX_STARTED'):
            self.__subscriber.start()
    #
    #
    def close(self):
        self.__subscriber.close()
    #
    #
    def on_join_sandbox(self, message, *args, **kwargs):
        data = message.get('data')
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, 'SandboxStorage.on_join_sandbox (before): %s', str(self.minor_mappings))
        if isinstance(data, dict):
            self.minor_mappings.update(data)
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, 'SandboxStorage.on_join_sandbox (after): %s', str(self.minor_mappings))
        pass
    #
    def on_quit_sandbox(self, message, *args, **kwargs):
        data = message.get('data')
        if isinstance(data, list):
            for item in data:
                if item in self.minor_mappings:
                    del self.minor_mappings[item]
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, 'SandboxStorage.on_quit_sandbox (after): %s', str(self.minor_mappings))
        pass
    #
    #
    __minor_mappings = None
    #
    @property
    def minor_mappings(self):
        if self.__minor_mappings is None:
            mappings_json, err = json_loads(os.getenv('REDANT_MINOR_PHONE_NUMBERS'))
            if mappings_json is not None:
                self.__minor_mappings = mappings_json
            else:
                self.__minor_mappings = dict()
            if LOG.isEnabledFor(logging.DEBUG):
                LOG.log(logging.DEBUG, 'initialize minor_mappings: %s', str(self.__minor_mappings))
        return self.__minor_mappings
    #
    #
    __minor_upstream = None
    #
    @property
    def minor_upstream(self):
        if self.__minor_upstream is None:
            lookup_json, _ = json_loads(os.getenv('REDANT_MINOR_UPSTREAM_SERVERS'))
            if lookup_json is not None and isinstance(lookup_json, dict):
                self.__minor_upstream = dict()
                for name, urls in lookup_json.items():
                    compiled_urls = self.__load_upstream_server_urls(urls)
                    if compiled_urls:
                        self.__minor_upstream[name] = compiled_urls
            if LOG.isEnabledFor(logging.DEBUG):
                LOG.log(logging.DEBUG, '__minor_upstream: %s', str(self.__minor_upstream))
        return self.__minor_upstream
    #
    #
    __major_upstream = None
    #
    @property
    def major_upstream(self):
        if self.__major_upstream is None:
            baseurls = stringToArray(os.getenv('REDANT_MAJOR_UPSTREAM_SERVERS'))
            self.__major_upstream = self.__load_upstream_server_urls(baseurls, ['127.0.0.1:8088'])
            if LOG.isEnabledFor(logging.DEBUG):
                LOG.log(logging.DEBUG, '__major_upstream: %s', str(self.__major_upstream))
        return self.__major_upstream
    #
    #
    @staticmethod
    def __load_upstream_server_urls(baseurls, default_values=None):
        urls = baseurls
        if not urls and default_values:
            urls = default_values
        urls = map(lambda s: s if s.startswith('http://') else 'http://' + s, urls)
        urls = map(lambda s: urlparse.urlsplit(s), urls)
        urls = list(urls)
        return urls
