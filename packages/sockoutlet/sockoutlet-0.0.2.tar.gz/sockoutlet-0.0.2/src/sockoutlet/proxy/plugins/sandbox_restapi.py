# -*- coding: utf-8 -*-

import logging
from typing import List, Tuple

from proxy.common.utils import build_http_response, socket_connection, text_
from proxy.http.codes import httpStatusCodes
from proxy.http.parser import HttpParser
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.server import HttpWebServerBasePlugin, httpProtocolTypes
from proxy.http.websocket import WebsocketFrame

from sockoutlet.utils.object_util import json_loads, json_dumps
from sockoutlet.utils.string_util import stringToArray
from sockoutlet.proxy.sandbox import SandboxManager


LOG = logging.getLogger(__name__)
SANDBOX_MANAGER = SandboxManager()


class SandboxManagerRestapiPlugin(HttpWebServerBasePlugin):
    """Demonstrates inbuilt web server routing using plugin."""

    def __init__(self, *args, **kwargs):
        if LOG.isEnabledFor(logging.DEBUG):
            LOG.log(logging.DEBUG, 'Initialize the SandboxManagerRestapiPlugin')
        self._sandbox_manager = SANDBOX_MANAGER
        super(SandboxManagerRestapiPlugin, self).__init__(*args, **kwargs)

    def routes(self) -> List[Tuple[int, str]]:
        return [
            (httpProtocolTypes.HTTP, r'/_proxy_outlet$'),
            (httpProtocolTypes.HTTPS, r'/_proxy_outlet$'),
        ]

    def handle_request(self, request: HttpParser) -> None:
        if request.path in [b'/_proxy_outlet/join']:
            self.handle_join_sandbox(request)
        elif request.path in [b'/_proxy_outlet/quit']:
            self.handle_quit_sandbox(request)

    def handle_join_sandbox(self, request: HttpParser) -> None:
        self.client.queue(memoryview(build_http_response(
                httpStatusCodes.OK, body=b'Join sandbox')))

    def handle_quit_sandbox(self, request: HttpParser) -> None:
        self.client.queue(memoryview(build_http_response(
                httpStatusCodes.OK, body=b'Quiz sandbox')))

    def on_websocket_open(self) -> None:
        LOG.info('Websocket open')

    def on_websocket_message(self, frame: WebsocketFrame) -> None:
        LOG.info(frame.data)

    def on_websocket_close(self) -> None:
        LOG.info('Websocket close')
