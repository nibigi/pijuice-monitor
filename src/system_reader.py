#!/usr/bin/env python3
"""Read Raspberry Pi system metrics without external dependencies."""

from pathlib import Path
import os
import shutil


def read_system_snapshot():
    cpu_temp = int(
        Path("/sys/class/thermal/thermal_zone0/temp").read_text().strip()
    ) / 1000

    cpu_freq = int(
        Path("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
        .read_text().strip()
    ) / 1000

    meminfo = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        key, value = line.split(":", 1)
        meminfo[key] = int(value.strip().split()[0])

    disk = shutil.disk_usage("/")

    uptime = float(
        Path("/proc/uptime").read_text().split()[0]
    )

    return {
        "cpu_usage_percent": read_cpu_usage(),
        "cpu_temperature_c": cpu_temp,
        "cpu_frequency_mhz": cpu_freq,
        "cpu_count": os.cpu_count(),
        "memory_total_mb": round(meminfo["MemTotal"] / 1024, 1),
        "memory_available_mb": round(meminfo["MemAvailable"] / 1024, 1),
        "disk_total_gb": round(disk.total / 1024**3, 2),
        "disk_free_gb": round(disk.free / 1024**3, 2),
        "uptime_seconds": round(uptime, 1),
    }


def read_cpu_usage(interval=1.0):
    """Calculate CPU usage from two /proc/stat samples."""
    import time

    def sample():
        values = list(map(
            int,
            Path("/proc/stat").read_text().splitlines()[0].split()[1:]
        ))
        idle = values[3] + values[4]
        total = sum(values)
        return idle, total

    idle1, total1 = sample()
    time.sleep(interval)
    idle2, total2 = sample()

    delta_total = total2 - total1
    delta_idle = idle2 - idle1

    if delta_total <= 0:
        return None

    usage = 100 * (1 - delta_idle / delta_total)
    return round(max(0, min(100, usage)), 1)
