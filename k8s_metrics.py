
import subprocess
import time
from prometheus_client import Gauge, start_http_server

cpu = Gauge(
    "flashsale_pod_cpu_millicores",
    "CPU usage of Flask pods in millicores",
    ["pod"]
)

memory = Gauge(
    "flashsale_pod_memory_mebibytes",
    "Memory usage of Flask pods in MiB",
    ["pod"]
)

pod_count = Gauge(
    "flashsale_pod_count",
    "Number of pods reporting resource metrics"
)

def cpu_millicores(value):
    if value.endswith("m"):
        return float(value[:-1])
    if value.endswith("n"):
        return float(value[:-1]) / 1_000_000
    return float(value) * 1000

def memory_mib(value):
    for suffix, factor in [
        ("Ki", 1 / 1024),
        ("Mi", 1),
        ("Gi", 1024)
    ]:
        if value.endswith(suffix):
            return float(value[:-len(suffix)]) * factor
    return float(value) / (1024 * 1024)

start_http_server(8001, addr="0.0.0.0")
print("Kubernetes exporter running on port 8001")

while True:
    try:
        result = subprocess.run(
            [
                "kubectl", "top", "pods",
                "-l", "app=flashsale",
                "--no-headers"
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=15
        )

        cpu.clear()
        memory.clear()

        count = 0

        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) < 3:
                continue

            name, cpu_value, memory_value = parts[:3]

            cpu.labels(pod=name).set(
                cpu_millicores(cpu_value)
            )
            memory.labels(pod=name).set(
                memory_mib(memory_value)
            )
            count += 1

        pod_count.set(count)
        print("Updated metrics for", count, "pods")

    except Exception as e:
        print("Metrics collection failed:", e)

    time.sleep(10)
