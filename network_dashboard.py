
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import psutil
import socket
import urllib.request
import threading
from datetime import datetime

# =====================================
# WINDOW SETTINGS
# =====================================

root = tk.Tk()
root.title("CyberSecurity Toolkit - V5")
root.geometry("900x700")
root.minsize(780, 620)
root.configure(bg="#101827")

BG = "#101827"
CARD = "#1d2b40"
GREEN = "#00d68f"
WHITE = "#ffffff"
MUTED = "#aab8ca"
BLUE = "#55aaff"

# =====================================
# NETWORK DATA
# =====================================

previous = psutil.net_io_counters()

monitoring = True
network_data = {}

download_speed = 0
upload_speed = 0

# =====================================
# NETWORK INFORMATION
# =====================================

def get_local_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    except OSError:
        return "Unavailable"


def get_public_ip():

    try:
        request = urllib.request.Request(
            "https://api.ipify.org",
            headers={"User-Agent": "Python-Network-Dashboard"}
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            return response.read().decode("utf-8").strip()

    except Exception:
        return "Unavailable"


def load_ip_information():

    hostname = socket.gethostname()
    local_ip = get_local_ip()

    public_value = get_public_ip()

    def update():

        hostname_value.config(text=hostname)
        local_value.config(text=local_ip)
        public_value_label.config(text=public_value)

        network_data["Hostname"] = hostname
        network_data["Local IP"] = local_ip
        network_data["Public IP"] = public_value

    root.after(0, update)


# =====================================
# CREATE GUI CARDS
# =====================================

title = tk.Label(
    root,
    text="CYBERSECURITY TOOLKIT",
    font=("Segoe UI", 23, "bold"),
    bg=BG,
    fg=GREEN
)
title.pack(pady=(18, 4))

subtitle = tk.Label(
    root,
    text="LIVE NETWORK MONITORING DASHBOARD",
    font=("Segoe UI", 11),
    bg=BG,
    fg=MUTED
)
subtitle.pack(pady=(0, 18))


dashboard = tk.Frame(root, bg=BG)
dashboard.pack(fill="both", expand=True, padx=25)

for col in range(2):
    dashboard.grid_columnconfigure(col, weight=1)


def create_card(title_text, row, col):

    card = tk.Frame(
        dashboard,
        bg=CARD,
        padx=18,
        pady=16,
        highlightthickness=1,
        highlightbackground="#30445e"
    )

    card.grid(
        row=row,
        column=col,
        padx=8,
        pady=8,
        sticky="nsew"
    )

    heading = tk.Label(
        card,
        text=title_text,
        font=("Segoe UI", 10, "bold"),
        bg=CARD,
        fg=MUTED
    )
    heading.pack(anchor="w")

    value = tk.Label(
        card,
        text="Loading...",
        font=("Segoe UI", 18, "bold"),
        bg=CARD,
        fg=WHITE
    )
    value.pack(anchor="w", pady=(10, 0))

    return value


download_value = create_card(
    "LIVE DOWNLOAD SPEED", 0, 0
)

upload_value = create_card(
    "LIVE UPLOAD SPEED", 0, 1
)

received_value = create_card(
    "TOTAL DATA RECEIVED", 1, 0
)

sent_value = create_card(
    "TOTAL DATA SENT", 1, 1
)

hostname_value = create_card(
    "COMPUTER HOSTNAME", 2, 0
)

local_value = create_card(
    "LOCAL IP ADDRESS", 2, 1
)

public_value_label = create_card(
    "PUBLIC IP ADDRESS", 3, 0
)

status_value = create_card(
    "MONITORING STATUS", 3, 1
)


# =====================================
# LIVE NETWORK MONITOR
# =====================================

def update_network():

    global previous
    global download_speed, upload_speed

    current = psutil.net_io_counters()

    download_speed = max(
        0, current.bytes_recv - previous.bytes_recv
    )

    upload_speed = max(
        0, current.bytes_sent - previous.bytes_sent
    )

    # Update baseline every second
    previous = current

    if monitoring:

        download_value.config(
            text=f"{download_speed / 1024:.2f} KB/s",
            fg=GREEN
        )

        upload_value.config(
            text=f"{upload_speed / 1024:.2f} KB/s",
            fg=BLUE
        )

        received_value.config(
            text=f"{current.bytes_recv / (1024**2):.2f} MB"
        )

        sent_value.config(
            text=f"{current.bytes_sent / (1024**2):.2f} MB"
        )

        status_value.config(
            text="RUNNING",
            fg=GREEN
        )

    else:

        download_value.config(text="STOPPED")
        upload_value.config(text="STOPPED")

        status_value.config(
            text="STOPPED",
            fg="#ff7373"
        )

    root.after(1000, update_network)


# =====================================
# START / STOP MONITORING
# =====================================

def start_monitoring():

    global monitoring
    monitoring = True


def stop_monitoring():

    global monitoring
    monitoring = False


# =====================================
# EXPORT REPORT
# =====================================

def export_report():

    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        initialfile="Live_Network_Report.txt"
    )

    if not filename:
        return

    current = psutil.net_io_counters()

    report = [
        "CYBERSECURITY TOOLKIT",
        "LIVE NETWORK REPORT",
        "=" * 40,
        "Date: " + datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "",
        "Hostname: " + socket.gethostname(),
        "Local IP: " + network_data.get("Local IP", "Unknown"),
        "Public IP: " + network_data.get("Public IP", "Unknown"),
        "",
        f"Total Received: {current.bytes_recv / (1024**2):.2f} MB",
        f"Total Sent: {current.bytes_sent / (1024**2):.2f} MB",
        f"Download Speed: {download_speed / 1024:.2f} KB/s",
        f"Upload Speed: {upload_speed / 1024:.2f} KB/s",
        "",
        "Report generated successfully."
    ]

    try:

        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n".join(report))

        messagebox.showinfo(
            "Success",
            "Network report exported successfully!"
        )

    except OSError as error:

        messagebox.showerror("Export Error", str(error))


# =====================================
# BUTTONS
# =====================================

button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=15)

def create_button(text, command, color):

    return tk.Button(
        button_frame,
        text=text,
        command=command,
        bg=color,
        fg=WHITE,
        font=("Segoe UI", 10, "bold"),
        padx=15,
        pady=11,
        relief="flat",
        cursor="hand2"
    )


create_button(
    "START MONITOR",
    start_monitoring,
    "#16845f"
).grid(row=0, column=0, padx=5)

create_button(
    "STOP MONITOR",
    stop_monitoring,
    "#b33a48"
).grid(row=0, column=1, padx=5)

create_button(
    "EXPORT REPORT",
    export_report,
    "#30445e"
).grid(row=0, column=2, padx=5)


footer = tk.Label(
    root,
    text="Python Cybersecurity Toolkit | V5",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 9)
)
footer.pack(pady=(0, 12))


# =====================================
# START APPLICATION
# =====================================

threading.Thread(
    target=load_ip_information,
    daemon=True
).start()

update_network()

root.mainloop()
