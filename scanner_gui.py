import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import nmap
import os
from datetime import datetime

scanner = nmap.PortScanner()

def start_scan():
    target = target_entry.get()
    ports = port_entry.get()

    if not target:
        messagebox.showerror("Error", "Enter target IP/domain")
        return

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Scanning {target}...\n\n")

    try:
        selected = scan_type.get()

        if selected == "Quick Scan":
            arguments = "-T4"
        elif selected == "Aggressive Scan":
            arguments = "-A"
        else:
            arguments = "-sV"

        scanner.scan(target, ports, arguments=arguments)

        report = []

        for host in scanner.all_hosts():
            result = f"Host: {host}\nState: {scanner[host].state()}\n"
            output_box.insert(tk.END, result)
            report.append(result)

            for proto in scanner[host].all_protocols():
                output_box.insert(tk.END, f"\nProtocol: {proto}\n")

                for port in sorted(scanner[host][proto].keys()):
                    state = scanner[host][proto][port]['state']
                    service = scanner[host][proto][port]['name']

                    line = f"Port: {port} | State: {state} | Service: {service}\n"
                    output_box.insert(tk.END, line)
                    report.append(line)
        save_to_history(target, report)
        save_report(report)

    except Exception as e:
        messagebox.showerror("Scan Error", str(e))
        


def save_report(report):
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile=f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    if filename:
        with open(filename, "w") as f:
            f.writelines(report)

        messagebox.showinfo("Saved", "Report saved successfully")

def save_to_history(target, report):
    if not os.path.exists("history"):
        os.makedirs("history")

    filename = f"history/{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as f:
        f.writelines(report)

def view_history():
    history_window = tk.Toplevel(root)
    history_window.title("Scan History")
    history_window.geometry("700x500")

    history_box = scrolledtext.ScrolledText(history_window, width=85, height=30)
    history_box.pack(pady=10)

    if not os.path.exists("history"):
        history_box.insert(tk.END, "No scan history found.")
        return

    files = os.listdir("history")

    if not files:
        history_box.insert(tk.END, "No scans available.")
        return

    for file in files:
        history_box.insert(tk.END, f"{file}\n")


# GUI setup
root = tk.Tk()
root.title("NetProbe Scanner Pro")
root.geometry("900x650")
root.configure(bg="#1e1e1e")

title = tk.Label(
    root,
    text="NETPROBE SCANNER PRO",
    font=("Consolas", 20, "bold"),
    bg="#1e1e1e",
    fg="#00ff88"
)
title.pack(pady=10)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

tk.Label(frame, text="Target IP/Domain:", bg="#1e1e1e", fg="white").grid(row=0, column=0, padx=5)

tk.Label(frame, text="Port Range:", bg="#1e1e1e", fg="white").grid(row=1, column=0, padx=5)

tk.Label(frame, text="Scan Type:", bg="#1e1e1e", fg="white").grid(row=2, column=0, padx=5)

target_entry = tk.Entry(
    frame,
    width=30,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white"
)
target_entry.grid(row=0, column=1, padx=10, pady=5)

port_entry = tk.Entry(
    frame,
    width=30,
    bg="#2d2d2d",
    fg="white",
    insertbackground="white"
)
port_entry.grid(row=1, column=1, padx=10, pady=5)

port_entry.insert(0, "1-1000")

scan_btn = tk.Button(
    root,
    text="Start Scan",
    command=start_scan,
    bg="#00ff88",
    fg="black",
    font=("Arial", 12, "bold"),
    width=15
)
scan_btn.pack(pady=10)

scan_type = tk.StringVar()
scan_type.set("Service Detection")

scan_menu = tk.OptionMenu(
    frame,
    scan_type,
    "Quick Scan",
    "Service Detection",
    "Aggressive Scan"
)

scan_menu.config(bg="#2d2d2d", fg="white")
scan_menu.grid(row=2, column=1, padx=10, pady=5)

history_btn = tk.Button(
    root,
    text="View History",
    command=view_history,
    bg="#444444",
    fg="white",
    font=("Arial", 12),
    width=15
)
history_btn.pack(pady=5)

output_box = scrolledtext.ScrolledText(
    root,
    width=100,
    height=25,
    bg="#121212",
    fg="#00ff88",
    insertbackground="white",
    font=("Consolas", 10)
)
output_box.pack(pady=10)

root.mainloop()