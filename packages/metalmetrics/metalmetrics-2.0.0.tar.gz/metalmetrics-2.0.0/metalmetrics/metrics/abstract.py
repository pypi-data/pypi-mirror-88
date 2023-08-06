# -*- coding: utf-8 -*-

import abc


class MetricsAbstract(abc.ABC):
    def __init__(self, config):
        self._config = config

    @abc.abstractmethod
    def _execution(self):
        pass

    def run(self, spec):
        _exec = self._execution()
        if _exec is None or not isinstance(_exec, dict):
            return None
        return _exec.get(spec, None)
