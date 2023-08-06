#!/usr/bin/env python3

import copy
import logging
import os
import random

from abc import abstractmethod
from typing import Dict, List, Tuple
from urllib import parse as urlparse

from proxy.common.constants import DEFAULT_BUFFER_SIZE, DEFAULT_HTTP_PORT
from proxy.common.utils import build_http_response, socket_connection, text_
from proxy.http.codes import httpStatusCodes
from proxy.http.parser import HttpParser
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.server import HttpWebServerBasePlugin, httpProtocolTypes
from proxy.http.websocket import WebsocketFrame

from sockoutlet.utils.object_util import json_loads, json_dumps
from sockoutlet.utils.string_util import stringToArray
from sockoutlet.proxy.sandbox import SandboxStorage

LOG = logging.getLogger(__name__)
SANDBOX_STORAGE = SandboxStorage()

class WebhookReverseProxyPlugin(HttpWebServerBasePlugin):
    #
    REVERSE_PROXY_LOCATION: str = r'/*'
    #
    #
    def __init__(self, *args, **kwargs):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, 'Initialize the WebhookReverseProxyPlugin')
        self._sandbox_storage = SANDBOX_STORAGE
        super(WebhookReverseProxyPlugin, self).__init__(*args, **kwargs)
    #
    #
    def on_websocket_open(self) -> None:
        pass
    #
    def on_websocket_message(self, frame: WebsocketFrame) -> None:
        pass
    #
    def on_websocket_close(self) -> None:
        pass
    #
    #
    def routes(self) -> List[Tuple[int, str]]:
        return [
            (httpProtocolTypes.HTTP, self.REVERSE_PROXY_LOCATION),
            (httpProtocolTypes.HTTPS, self.REVERSE_PROXY_LOCATION)
        ]
    #
    #
    def handle_request(self, request: HttpParser) -> None:
        if self._sandbox_storage.minor_upstream:
            major_request, minor_requests = self._parse_request(request)
        else:
            major_request, minor_requests = (request, None)
        #
        if major_request is not None:
            self.__request_upstream(major_request, self._sandbox_storage.major_upstream)
        #
        if minor_requests is not None:
            self.__dispatch_requests_to_upstreams(minor_requests, self._sandbox_storage.minor_upstream)
    #
    #
    def _parse_request(self, request: HttpParser) -> Tuple[HttpParser, Dict[str, HttpParser]]:
        if request.body is None:
            return (request, None)
        #
        major_body, minor_bodies = self._parse_request_body(request.body)
        #
        minor_requests = None
        if minor_bodies:
            minor_requests = dict()
            for upstream_name in minor_bodies:
                minor_requests_item = copy.deepcopy(request)
                minor_requests_item.parse(minor_bodies[upstream_name])
                minor_requests[upstream_name] = minor_requests_item
        else:
            return (request, None)
        #
        major_request = None
        if major_body:
            major_request = request
            major_request.parse(major_body)
        #
        return (major_request, minor_requests)
    #
    #
    @abstractmethod
    def _parse_request_body(self, request_body: bytes) -> Tuple[bytes, Dict[str, bytes]]:
        pass
    #
    #
    def __request_upstream(self, request, upstream_url_list):
        try:
            url = random.choice(upstream_url_list)
            assert url
            with socket_connection((text_(url.hostname), url.port if url.port else DEFAULT_HTTP_PORT)) as conn:
                conn.send(request.build())
                if LOG.isEnabledFor(logging.DEBUG):
                    LOG.log(logging.DEBUG, 'waiting for proxy result')
                response = b''
                while True:
                    buffer = conn.recv(DEFAULT_BUFFER_SIZE)
                    if not buffer:
                        break
                    response += buffer
                if LOG.isEnabledFor(logging.DEBUG):
                    LOG.log(logging.DEBUG, 'received result length: (%d)', len(response))
                self.client.queue(memoryview(response))
        except ConnectionRefusedError as err:
            self.client.queue(memoryview(build_http_response(
                httpStatusCodes.NOT_FOUND, body=b'Reversed Proxy not found')))
    #
    #
    def __dispatch_requests_to_upstreams(self, upstream_request_map: Dict[str, HttpParser], upstream_map):
        if upstream_map:
            for upstream_name, request in upstream_request_map.items():
                upstream_url_list = upstream_map[upstream_name]
                if upstream_url_list:
                    self.__request_upstream(request, upstream_url_list)
