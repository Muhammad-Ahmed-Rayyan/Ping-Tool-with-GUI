import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import platform, os, socket
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def ping_host():
    host = host_entry.get()
    count = count_entry.get()
    if not host or not count.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid host and numeric count.")
        return

    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = f"ping {param} {count} {host}"

    result_box.config(state='normal')
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, f"🖥️ Pinging {host} {count} times...\n\n")

    output = os.popen(command).read()
    result_box.insert(tk.END, output + "\n")

    # Resolved Hostname
    try:
        resolved = socket.gethostbyaddr(socket.gethostbyname(host))[0]
        result_box.insert(tk.END, f"\nResolved Hostname: {resolved}\n")
    except:
        result_box.insert(tk.END, "\nCould not resolve hostname.\n")

    # Packet Loss
    loss_line = [line for line in output.splitlines() if "Lost = " in line or "loss" in line]
    if loss_line:
        result_box.insert(tk.END, f"Packet Loss Info: {loss_line[0]}\n")

    if "Received = 0" in output or "0 received" in output:
        result_box.insert(tk.END, f"\nPing to {host} failed ❌\n")
    else:
        result_box.insert(tk.END, f"\nPing to {host} successful ✅\n")

    # Extract ping times
    ping_times = []
    for line in output.splitlines():
        if "time=" in line:
            try:
                time_part = line.split("time=")[1].split()[0].replace("ms", "")
                ping_times.append(float(time_part))
            except:
                pass

    if ping_times:
        with open("ping_data.csv", "w") as f:
            f.write("Ping #,Time (ms)\n")
            for i, t in enumerate(ping_times, start=1):
                f.write(f"{i},{t}\n")

        fig = plt.Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(ping_times, marker='o', color='green')
        ax.set_title(f"Ping Times to {host}")
        ax.set_xlabel("Ping #")
        ax.set_ylabel("Time (ms)")
        ax.grid(True)

        for widget in plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    result_box.config(state='disabled')

# GUI Setup
root = tk.Tk()
root.title("🎯 Elegant Ping Tool")
root.geometry("720x600")
root.configure(bg="#f0f2f5")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#28a745")
style.configure("TLabel", font=("Segoe UI", 10), background="#f0f2f5")

tk.Label(root, text="🌐 Enter Host:", font=("Segoe UI", 11, "bold"), bg="#f0f2f5").pack(pady=(10, 0))
host_entry = ttk.Entry(root, width=50)
host_entry.pack(pady=5)

tk.Label(root, text="📶 Ping Count:", font=("Segoe UI", 11, "bold"), bg="#f0f2f5").pack()
count_entry = ttk.Entry(root, width=20)
count_entry.pack(pady=5)

ttk.Button(root, text="🚀 Start Ping", command=ping_host).pack(pady=10)

result_box = scrolledtext.ScrolledText(root, width=85, height=15, state='disabled', font=("Consolas", 10))
result_box.pack(padx=10, pady=10)

plot_frame = tk.Frame(root, bg="#f0f2f5", height=200)
plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
