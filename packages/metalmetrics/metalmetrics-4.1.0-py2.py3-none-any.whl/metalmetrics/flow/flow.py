# -*- coding: utf-8 -*-

import grpc

from concurrent import futures
from metalmetrics.flow.flow_pb2 import FlowReply
from metalmetrics.flow.flow_pb2_grpc import (
    add_FlowProtoServicer_to_server,
    FlowProtoServicer,
)


class FlowException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Flow(object):
    _workers = 10

    def __init__(self, config):
        if config is None:
            raise FlowException("config invalid")
        self._config = config

    def _serve(self, routine, args):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._workers))
        add_FlowProtoServicer_to_server(FlowProto(routine, args), server)
        server.add_insecure_port(self._config.listen_url)
        server.start()
        server.wait_for_termination()

    def run(self, routine, args=None):
        self._serve(routine, args)


class FlowProto(FlowProtoServicer):
    _len = 3
    _prefix = "metalmetrics"
    _sep = "/"

    def __init__(self, routine, args):
        self._args = args
        self._routine = routine

    def _parse(self, message):
        if len(message) == 0 or not message.startswith(self._prefix + self._sep):
            return None, None
        msg = self._sep.split(message)
        if len(msg) != self._len:
            return None, None
        return msg[1], msg[2]

    def SendFlow(self, request, _):
        host, spec = self._parse(request.message)
        if host is None or spec is None:
            return FlowReply(message="")
        buf = self._routine(host=host, spec=spec).get(host, None)
        if buf is not None:
            message = buf.get(spec, "")
        else:
            message = ""
        return FlowReply(message=message)
