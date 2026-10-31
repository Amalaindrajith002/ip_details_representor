
import psutil
import time

print("=" * 45)
print("      LIVE NETWORK MONITOR")
print("=" * 45)

previous = psutil.net_io_counters()

print("\nMonitoring started...")
print("Press CTRL + C to stop.\n")

try:
    while True:

        time.sleep(1)

        current = psutil.net_io_counters()

        download_speed = (
            current.bytes_recv - previous.bytes_recv
        )

        upload_speed = (
            current.bytes_sent - previous.bytes_sent
        )

        print(
            f"Download: {download_speed / 1024:.2f} KB/s | "
            f"Upload: {upload_speed / 1024:.2f} KB/s"
        )

        previous = current

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
