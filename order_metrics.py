from prometheus_client import start_http_server, Summary, Gauge
import random
import time

# Metrics
total_orders = Gauge("total_orders", "Total number of orders")
pending_orders = Gauge("pending_orders", "Number of pending orders")
on_the_way_orders = Gauge("on_the_way_orders", "Number of orders on the way")
average_order_time = Summary("average_order_time", "Average order time in seconds")

# Simulate order statuses
def simulate_order():
    pending = random.randint(50, 100)  # Increase range to exceed alert threshold # Ensure values exceed the threshold
    on_the_way = random.randint(5, 20)
    delivered = random.randint(30, 70)
    avg_time = random.uniform(15, 45)

    total = pending + on_the_way + delivered

    print(f"[DEBUG] Total orders: {total}")
    print(f"[DEBUG] Pending orders: {pending}")
    print(f"[DEBUG] On-the-way orders: {on_the_way}")
    print(f"[DEBUG] Average order time: {avg_time:.2f} seconds")

    total_orders.set(total)
    pending_orders.set(pending)
    on_the_way_orders.set(on_the_way)
    average_order_time.observe(avg_time)

if __name__ == "__main__":
    print("[INFO] Starting the HTTP server on port 8000...")
    start_http_server(8000, addr="0.0.0.0")
    print("[INFO] HTTP server started. Simulating orders...")
    while True:
        simulate_order()
        print("[INFO] Sleeping for 1 seconds...")
        time.sleep(1)