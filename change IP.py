import tkinter as tk
from tkinter import messagebox
import subprocess
import psutil
import socket
import time

# 自定义软件版本号
software_version = "Ver:1.0"

def set_static_ip(ip_address, subnet_mask):
    # 使用powershell命令设置静态IP地址
    command = f"powershell -Command \"Start-Process netsh -ArgumentList 'interface ip set address name=\\\"以太网\\\" static {ip_address} {subnet_mask}' -Verb RunAs\""
    subprocess.run(command, shell=True)


def set_dhcp():
    # 使用powershell命令设置为自动获取IP地址
    command = f"powershell -Command \"Start-Process netsh -ArgumentList 'interface ip set address name=\\\"以太网\\\" source=dhcp' -Verb RunAs\""
    subprocess.run(command, shell=True)


def get_ethernet_ipv4():
    interfaces = psutil.net_if_addrs()
    for interface_name, interface_addresses in interfaces.items():
        if interface_name == '以太网':
            for addr in interface_addresses:
                if addr.family == socket.AF_INET:
                    return addr.address
    return None


def set_ip_static(ip_address):
    if ip_address == "192.168.1.26":
        ping_ip = "192.168.1.251"
    elif ip_address == "192.168.30.24":
        ping_ip = "192.168.30.42"
    else:
        messagebox.showerror("错误", "无效的IP地址")
        return

    set_static_ip(ip_address, "255.255.255.0")
    local_ip = get_ethernet_ipv4()
    if local_ip:
        messagebox.showinfo("成功", f"IP地址已设置为 {ip_address}\n以太网IPv4地址为: {local_ip}")
        # 打开命令行窗口执行ping命令
        subprocess.Popen(["cmd", "/c", f"ping {ping_ip}"])
        # 设置定时器，在15秒后关闭ping命令的命令行窗口
        root.after(20000, lambda: subprocess.run("taskkill /f /im cmd.exe", shell=True))
    else:
        messagebox.showerror("错误", "无法获取以太网IPv4地址")


def set_ip_dhcp():  # 设置自动获取 IP 地址
    set_dhcp()
    local_ip = get_ethernet_ipv4()
    if local_ip:
        messagebox.showinfo("成功", f"已切换为自动获取 IP 地址")
    else:
        messagebox.showerror("错误", "无法获取以太网IPv4地址")


# 创建主窗口
root = tk.Tk()
root.title("IP设置工具")

# 设置窗口大小
root.geometry("300x200")

# 设置按钮间距
ping_ip_label = tk.Label(root, text="选择要设置及Ping的IP地址:")
ping_ip_label.pack(pady=5)  # pady 设置间距 默认5

btn_static_ip1 = tk.Button(root, text="设置IP地址 192.168.1网段", command=lambda: set_ip_static("192.168.1.26"))
btn_static_ip1.pack(pady=5)

btn_static_ip2 = tk.Button(root, text="设置IP地址 192.168.30网段", command=lambda: set_ip_static("192.168.30.24"))
btn_static_ip2.pack(pady=5)

btn_dhcp = tk.Button(root, text="设置为自动获取IP地址", command=set_ip_dhcp)
btn_dhcp.pack(pady=5)

# 显示软件版本号
version_label = tk.Label(root, text=f"软件版本号：{software_version}")
version_label.pack(pady=5)

# 运行主循环
root.mainloop()

