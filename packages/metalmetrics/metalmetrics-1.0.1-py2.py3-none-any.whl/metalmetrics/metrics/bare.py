# -*- coding: utf-8 -*-

import os
import psutil
import socket
import subprocess

from metalmetrics.config.config import Spec
from metalmetrics.metrics.abstract import MetricsAbstract


class BareException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Bare(MetricsAbstract):
    def __init__(self, config):
        super().__init__(config)
        self._exec = {
            Spec.CPU: self._cpu(),
            Spec.DISK: self._disk(),
            Spec.IO: self._io(),
            Spec.IP: self._ip(),
            Spec.KERNEL: self._kernel(),
            Spec.MAC: self._mac(),
            Spec.NETWORK: self._network(),
            Spec.OS: self._os(),
            Spec.RAM: self._ram(),
        }

    def _execution(self):
        return self._exec

    def _popen(self, cmd, stdin=None):
        return subprocess.Popen(
            cmd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def _cpu(self):
        """
        awk -F: '/model name/ {core++} END {print core}' /proc/cpuinfo
        """
        return "%s CPU" % str(psutil.cpu_count())

    def _disk(self):
        """
        df -hPl | grep -wvE '\\-|none|tmpfs|devtmpfs|by-uuid|chroot|Filesystem|udev|docker' | awk '{print $2}'
        df -hPl | grep -wvE '\\-|none|tmpfs|devtmpfs|by-uuid|chroot|Filesystem|udev|docker' | awk '{print $3}'
        """
        usage = psutil.disk_usage("/")
        return "%.1f GB (%.1f GB Used)" % (
            float(usage.total >> 30),
            float(usage.used >> 30),
        )

    def _io(self):
        read = psutil.disk_io_counters().read_bytes >> 10
        write = psutil.disk_io_counters().write_bytes >> 10
        return "RD %s KB WR %s KB" % (str(read), str(write))

    def _ip(self):
        def _helper(nic):
            buf = ""
            for item in psutil.net_if_addrs()[nic]:
                if item.family == socket.AF_INET:
                    buf = item.address
                    break
            return buf

        buf = []
        for key, val in psutil.net_if_stats().items():
            if key != "lo" and val.isup is True:
                addr = _helper(key)
                if len(addr) != 0:
                    buf.append(addr)
        return os.linesep.join(buf)

    def _kernel(self):
        """
        uname -r
        """
        cmd = ["uname", "-r"]
        with self._popen(cmd) as proc:
            out, _ = proc.communicate()
            if proc.returncode != 0:
                return ""
        return out.strip().decode("utf-8")

    def _mac(self):
        def _helper(nic):
            buf = ""
            for item in psutil.net_if_addrs()[nic]:
                if item.family == psutil.AF_LINK:
                    buf = item.address
                    break
            return buf

        buf = []
        for key, val in psutil.net_if_stats().items():
            if key != "lo" and val.isup is True:
                addr = _helper(key)
                if len(addr) != 0:
                    buf.append(addr)
        return os.linesep.join(buf)

    def _network(self):
        def _helper(nic):
            sent = psutil.net_io_counters(pernic=True)[nic].packets_sent
            recv = psutil.net_io_counters(pernic=True)[nic].packets_recv
            return "RX packets %s TX packets %s" % (str(recv), str(sent))

        buf = []
        for key, val in psutil.net_if_stats().items():
            if key != "lo" and val.isup is True:
                addr = _helper(key)
                if len(addr) != 0:
                    buf.append(addr)
        return os.linesep.join(buf)

    def _os(self):
        """
        awk -F'[= "]' '/PRETTY_NAME/{print $3,$4,$5}' /etc/os-release
        """
        cmd = ["awk", '-F[= "]', "/PRETTY_NAME/{print $3,$4,$5}", "/etc/os-release"]
        with self._popen(cmd) as proc:
            out, _ = proc.communicate()
            if proc.returncode != 0:
                return "invalid"
        return out.strip().decode("utf-8")

    def _ram(self):
        """
        free -m | awk '/Mem/ {print $2}'
        free -m | awk '/Mem/ {print $3}'
        """
        mem = psutil.virtual_memory()
        return "%s MB (%s MB Used)" % (str(mem.total >> 20), str(mem.used >> 20))
