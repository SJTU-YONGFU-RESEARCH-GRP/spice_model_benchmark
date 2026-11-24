"""System and hardware resource discovery for benchmark reports."""

from __future__ import annotations

import os
import platform
import subprocess
from typing import Dict


def get_hardware_specs() -> Dict[str, str]:
    """Extract host CPU model, socket/core/thread counts, RAM, and platform."""
    info = {
        "platform": platform.platform(),
        "processor": platform.processor(),
        "cpu_model": "Unknown CPU",
        "total_threads": str(os.cpu_count() or 1),
        "physical_cores": "N/A",
        "sockets": "1",
        "total_memory": "N/A",
    }
    try:
        cpu = subprocess.check_output(
            "lscpu | grep 'Model name:' | sed 's/Model name:[ \t]*//'",
            shell=True, text=True, stderr=subprocess.DEVNULL
        ).strip()
        if cpu:
            info["cpu_model"] = cpu

        threads = subprocess.check_output(
            "lscpu | grep 'CPU(s):' | head -1 | awk '{print $2}'",
            shell=True, text=True, stderr=subprocess.DEVNULL
        ).strip()
        if threads:
            info["total_threads"] = threads

        cores_per_socket = subprocess.check_output(
            "lscpu | grep 'Core(s) per socket:' | awk '{print $NF}'",
            shell=True, text=True, stderr=subprocess.DEVNULL
        ).strip()
        sockets = subprocess.check_output(
            "lscpu | grep 'Socket(s):' | awk '{print $NF}'",
            shell=True, text=True, stderr=subprocess.DEVNULL
        ).strip()
        if sockets and cores_per_socket:
            info["sockets"] = sockets
            try:
                info["physical_cores"] = str(int(sockets) * int(cores_per_socket))
            except Exception:
                info["physical_cores"] = cores_per_socket

        mem = subprocess.check_output(
            "free -h | awk '/Mem:/ {print $2}'",
            shell=True, text=True, stderr=subprocess.DEVNULL
        ).strip()
        if mem:
            info["total_memory"] = mem
    except Exception:
        pass

    return info
