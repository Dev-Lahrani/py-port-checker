#!/usr/bin/env python3
import subprocess
import socket
import sys
import os
from prettytable import PrettyTable

ASCII_BANNER = r"""
██████╗  ██████╗ ██████╗ ███████╗████████╗███████╗███████╗
██╔══██╗██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝
██████╔╝██║   ██║██████╔╝█████╗     ██║   █████╗  █████╗  
██╔═══╝ ██║   ██║██╔═══╝ ██╔══╝     ██║   ██╔══╝  ██╔══╝  
██║     ╚██████╔╝██║     ███████╗   ██║   ███████╗███████╗
╚═╝      ╚═════╝ ╚═╝     ╚══════╝   ╚═╝   ╚══════╝╚══════╝

        ╔══════════════════════════╗
        ║   ▄▄▄▄ PyPort ▄▄▄▄      ║
        ║  ▄▀░░░░░░░░░░░░░░░░░▀▄  ║
        ║ ▄▀░░░░░░░░░░░░░░░░░░░░▀▄ ║
        ║ █░░░░░ Active Ports ░░█ ║
        ║ █░░░░  Kill / Enable ░█ ║
        ║ █░░░░  Disable / Scan░█ ║
        ╚══════════════════════════╝
"""

def list_ports():
    table = PrettyTable(["Port", "Protocol", "Status", "Process/Service"])
    try:
        output = subprocess.check_output(["sudo", "lsof", "-i", "-P", "-n"], universal_newlines=True)
        lines = output.strip().split("\n")[1:]  # skip header
        for line in lines:
            parts = line.split()
            if len(parts) < 9:
                continue
            command, pid, user, fd, type_, device, size, node, name = parts[:9]
            proto = name.split(":")[-1] if ":" in name else "unknown"
            port = name.split(":")[-1].split("->")[0]
            status = "LISTENING" if "LISTEN" in name else "ESTABLISHED"
            table.add_row([port, proto, status, f"{command} ({pid})"])
    except subprocess.CalledProcessError:
        print("Error scanning ports.")
    print(table)

def kill_port(port):
    try:
        output = subprocess.check_output(["sudo", "lsof", "-i", f":{port}"], universal_newlines=True)
        lines = output.strip().split("\n")[1:]
        for line in lines:
            parts = line.split()
            if len(parts) < 2:
                continue
            pid = parts[1]
            subprocess.run(["sudo", "kill", "-9", pid])
            print(f"Killed process {pid} on port {port}")
    except subprocess.CalledProcessError:
        print(f"No process found using port {port}")

def manage_service(action, service):
    if action not in ["enable", "disable", "start", "stop"]:
        print("Unknown action")
        return
    try:
        subprocess.run(["sudo", "systemctl", action, service], check=True)
        print(f"Service {service} {action}d successfully")
    except subprocess.CalledProcessError:
        print(f"Failed to {action} service {service}")

def main():
    print(ASCII_BANNER)
    print("\nCommands:\n  list -> show all ports\n  kill <port>\n  enable <service>\n  disable <service>\n  exit\n")
    while True:
        cmd = input("> ").strip().split()
        if not cmd:
            continue
        if cmd[0] == "list":
            print("Scanning ports...\n")
            list_ports()
        elif cmd[0] == "kill" and len(cmd) == 2:
            kill_port(cmd[1])
        elif cmd[0] == "enable" and len(cmd) == 2:
            manage_service("enable", cmd[1])
        elif cmd[0] == "disable" and len(cmd) == 2:
            manage_service("disable", cmd[1])
        elif cmd[0] == "exit":
            print("Exiting PyPort.")
            sys.exit(0)
        else:
            print("Unknown command")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This program requires sudo/root privileges. Please run with sudo.")
        sys.exit(1)
    main()
