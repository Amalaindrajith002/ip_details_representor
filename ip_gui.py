
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import socket
import urllib.request
import subprocess
import re
import threading
from datetime import datetime


# ==============================
# WINDOW SETTINGS
# ==============================

root = tk.Tk()
root.title("CyberSecurity Toolkit - IP Information")
root.geometry("850x650")
root.minsize(750, 580)
root.configure(bg="#101827")

BG = "#101827"
CARD = "#1d2b40"
GREEN = "#00d68f"
WHITE = "#ffffff"
MUTED = "#aab8ca"


# ==============================
# DATA STORAGE
# ==============================

network_data = {}


# ==============================
# NETWORK INFORMATION
# ==============================

def get_network_information():

    data = {}

    # Hostname
    data["Hostname"] = socket.gethostname()

    # Local IP
    try:
        connection = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )
        connection.connect(("1.1.1.1", 80))
        data["Local IP"] = connection.getsockname()[0]
        connection.close()

    except OSError:
        data["Local IP"] = "Unavailable"

    # Public IP
    try:
        request = urllib.request.Request(
            "https://api.ipify.org",
            headers={"User-Agent": "Python-Cybersecurity-Toolkit"}
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            public_ip = response.read().decode("utf-8").strip()

        data["Public IP"] = public_ip

    except Exception:
        data["Public IP"] = "Unavailable"

    # Internet connection test
    try:
        test = socket.create_connection(
            ("1.1.1.1", 53),
            timeout=3
        )
        test.close()
        data["Internet Status"] = "Connected"

    except OSError:
        data["Internet Status"] = "Not Connected / Blocked"

    # Windows network configuration
    try:
        result = subprocess.run(
            ["ipconfig", "/all"],
            capture_output=True,
            text=True,
            errors="replace",
            timeout=10
        )

        output = result.stdout

        # Find IPv4 values from matching lines
        def find_network_value(label):

            lines = output.splitlines()

            for index, line in enumerate(lines):

                if label.lower() in line.lower():

                    values = re.findall(
                        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                        line.split(":")[-1]
                    )

                    # Check the next line if the value is blank
                    if not values and index + 1 < len(lines):
                        values = re.findall(
                            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                            lines[index + 1]
                        )

                    if values:
                        return ", ".join(values)

            return "Unavailable"

        data["Gateway"] = find_network_value("Default Gateway")
        data["DNS"] = find_network_value("DNS Servers")

    except Exception:
        data["Gateway"] = "Unavailable"
        data["DNS"] = "Unavailable"

    return data


# ==============================
# DISPLAY INFORMATION
# ==============================

def update_dashboard(data):

    global network_data

    network_data = data

    hostname_value.config(text=data["Hostname"])
    local_value.config(text=data["Local IP"])
    public_value.config(text=data["Public IP"])
    gateway_value.config(text=data["Gateway"])
    dns_value.config(text=data["DNS"])

    status = data["Internet Status"]

    status_value.config(
        text=status,
        fg=GREEN if status == "Connected" else "#ff7373"
    )

    refresh_button.config(
        text="REFRESH INFORMATION",
        state="normal"
    )


# ==============================
# REFRESH BUTTON
# ==============================

def refresh_information():

    refresh_button.config(
        text="COLLECTING...",
        state="disabled"
    )

    status_value.config(
        text="Checking...",
        fg="#ffd166"
    )

    def worker():

        try:
            data = get_network_information()

            root.after(
                0,
                lambda: update_dashboard(data)
            )

        except Exception as error:

            root.after(
                0,
                lambda: refresh_failed(str(error))
            )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()


def refresh_failed(error):

    refresh_button.config(
        text="REFRESH INFORMATION",
        state="normal"
    )

    messagebox.showerror(
        "Error",
        error
    )


# ==============================
# EXPORT REPORT
# ==============================

def export_report():

    if not network_data:
        messagebox.showwarning(
            "Warning",
            "Please refresh network information first."
        )
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        initialfile="Network_Report.txt"
    )

    if not filename:
        return

    report = []
    report.append("PYTHON CYBERSECURITY TOOLKIT")
    report.append("IP INFORMATION REPORT")
    report.append("=" * 45)
    report.append("Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    report.append("")

    for key, value in network_data.items():
        report.append(f"{key}: {value}")

    report.append("")
    report.append("=" * 45)
    report.append("Report generated successfully.")

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n".join(report))

        messagebox.showinfo(
            "Success",
            "Report saved successfully!"
        )

    except OSError as error:
        messagebox.showerror("Export Error", str(error))


# ==============================
# GUI DESIGN
# ==============================

title = tk.Label(
    root,
    text="CYBERSECURITY TOOLKIT",
    font=("Segoe UI", 22, "bold"),
    bg=BG,
    fg=GREEN
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="IP INFORMATION DASHBOARD",
    font=("Segoe UI", 11),
    bg=BG,
    fg=MUTED
)
subtitle.pack(pady=(0, 20))


# Dashboard frame
dashboard = tk.Frame(root, bg=BG)
dashboard.pack(fill="both", expand=True, padx=25)


def create_card(parent, title_text, row, column):

    card = tk.Frame(
        parent,
        bg=CARD,
        padx=15,
        pady=18,
        highlightthickness=1,
        highlightbackground="#30445e"
    )

    card.grid(
        row=row,
        column=column,
        padx=8,
        pady=8,
        sticky="nsew"
    )

    label = tk.Label(
        card,
        text=title_text,
        font=("Segoe UI", 10, "bold"),
        bg=CARD,
        fg=MUTED
    )
    label.pack(anchor="w")

    value = tk.Label(
        card,
        text="Waiting...",
        font=("Segoe UI", 12, "bold"),
        bg=CARD,
        fg=WHITE,
        wraplength=300,
        justify="left"
    )
    value.pack(anchor="w", pady=(12, 0))

    return value


for column in range(2):
    dashboard.grid_columnconfigure(column, weight=1)

for row in range(3):
    dashboard.grid_rowconfigure(row, weight=1)


hostname_value = create_card(
    dashboard, "COMPUTER HOSTNAME", 0, 0
)

local_value = create_card(
    dashboard, "LOCAL IP ADDRESS", 0, 1
)

public_value = create_card(
    dashboard, "PUBLIC IP ADDRESS", 1, 0
)

gateway_value = create_card(
    dashboard, "DEFAULT GATEWAY", 1, 1
)

dns_value = create_card(
    dashboard, "DNS SERVER", 2, 0
)

status_value = create_card(
    dashboard, "INTERNET STATUS", 2, 1
)


# ==============================
# BUTTONS
# ==============================

button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=18)

refresh_button = tk.Button(
    button_frame,
    text="REFRESH INFORMATION",
    command=refresh_information,
    bg=GREEN,
    fg="#101827",
    font=("Segoe UI", 10, "bold"),
    padx=18,
    pady=12,
    relief="flat",
    cursor="hand2"
)
refresh_button.grid(row=0, column=0, padx=8)

export_button = tk.Button(
    button_frame,
    text="EXPORT REPORT",
    command=export_report,
    bg="#30445e",
    fg=WHITE,
    font=("Segoe UI", 10, "bold"),
    padx=18,
    pady=12,
    relief="flat",
    cursor="hand2"
)
export_button.grid(row=0, column=1, padx=8)


footer = tk.Label(
    root,
    text="Python Cybersecurity Toolkit | Educational Project",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 9)
)
footer.pack(pady=(0, 12))


# ==============================
# START APPLICATION
# ==============================

refresh_information()

root.mainloop()
