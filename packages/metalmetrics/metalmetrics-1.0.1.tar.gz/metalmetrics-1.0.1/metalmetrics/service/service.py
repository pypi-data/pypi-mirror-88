# -*- coding: utf-8 -*-

import grpc

from concurrent import futures
from metalmetrics.service.service_pb2 import BareReply
from metalmetrics.service.service_pb2 import ContainerReply
from metalmetrics.service.service_pb2 import KubernetesReply
from metalmetrics.service.service_pb2_grpc import (
    add_ServiceProtoServicer_to_server,
    ServiceProtoServicer,
)


class ServiceException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Service(object):
    _workers = 10

    def __init__(self, config):
        if config is None:
            raise ServiceException("config invalid")
        self._config = config

    def _serve(self, routine, args):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._workers))
        add_ServiceProtoServicer_to_server(ServiceProto(routine, args), server)
        server.add_insecure_port(self._config.grpc_url)
        server.start()
        server.wait_for_termination()

    def run(self, routine, args=[]):
        self._serve(routine, args)


class ServiceProto(ServiceProtoServicer):
    def __init__(self, routine, args):
        self._args = args
        self._routine = routine

    def SendBare(self, request, context):
        buf = self._routine(host="bare", spec=request.name)
        host = buf.get("bare", None)
        if host is not None:
            spec = host.get(request.name, "")
        else:
            spec = ""
        return BareReply(message=spec)

    def SendContainer(self, request, context):
        buf = self._routine(host="container", spec=request.name)
        host = buf.get("container", None)
        if host is not None:
            spec = host.get(request.name, "")
        else:
            spec = ""
        return ContainerReply(message=spec)

    def SendKubernetes(self, request, context):
        buf = self._routine(host="kubernetes", spec=request.name)
        host = buf.get("kubernetes", None)
        if host is not None:
            spec = host.get(request.name, "")
        else:
            spec = ""
        return KubernetesReply(message=spec)
