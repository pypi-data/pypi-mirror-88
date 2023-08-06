# -*- coding: utf-8 -*-

import queue
import threading


class QueueException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Queue(object):
    queue_num = 1
    routine_num = 1

    def __init__(self, config):
        if config is None:
            pass
        self._queue = queue.Queue(self.queue_num)
        for _ in range(self.routine_num):
            Worker(self._queue)

    def _add(self, routine, args):
        self._queue.put((routine, args))

    def _wait(self):
        self._queue.join()

    def run(self, routine, args=[]):
        for _ in range(self.queue_num):
            self._add(routine, args)
        self._wait()


class WorkerException(QueueException):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Worker(threading.Thread):
    def __init__(self, _queue):
        super(Worker, self).__init__()
        self._queue = _queue
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, _ = self._queue.get()
            func()
            self._queue.task_done()
