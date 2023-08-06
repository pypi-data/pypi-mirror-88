# -*- coding: utf-8 -*-

from metalmetrics.metrics.abstract import MetricsAbstract


class KubernetesException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Kubernetes(MetricsAbstract):
    def __init__(self, config):
        super().__init__(config)

    def _execution(self):
        pass
