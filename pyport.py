print(help_text)
    
    def scan_remote_host(self, host: str, port: Optional[str] = None):
        """Scan ports on a remote host"""
        print(f"🌐 Scanning {host}...")
        
        ports_to_scan = [port] if port else ['22', '80', '443', '21', '25', '53', '110', '143', '993', '995', '3389']
        open_ports = []
        
        for p in ports_to_scan:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, int(p)))
                sock.close()
                
                if result == 0:
                    open_ports.append(p)
                    print(f"✅ Port {p} - OPEN")
                elif port:  # Only show closed if scanning specific port
                    print(f"❌ Port {p} - CLOSED")
            except (socket.gaierror, ValueError):
                print(f"❌ Error scanning port {p}")
        
        if not port:  # Summary for multiple ports
            print(f"\n📊 Found {len(open_ports)} open ports on {host}")
            if open_ports:
                print(f"Open ports: {', '.join(open_ports)}")#!/usr/bin/env python3
import subprocess
import socket
import sys
import os
import re
from prettytable import PrettyTable
from typing import List, Tuple, Optional

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

class PortManager:
    def __init__(self):
        self.check_privileges()
    
    def check_privileges(self):
        """Check if running with root privileges"""
        if os.geteuid() != 0:
            print("❌ This program requires sudo/root privileges. Please run with sudo.")
            sys.exit(1)
    
    def parse_lsof_output(self, output: str) -> List[Tuple[str, str, str, str, str]]:
        """Parse lsof output and return structured data"""
        ports = []
        lines = output.strip().split("\n")
        
        for line in lines[1:]:  # Skip header
            parts = line.split()
            if len(parts) < 9:
                continue
            
            command = parts[0]
            pid = parts[1]
            user = parts[2]
            name = parts[8] if len(parts) > 8 else parts[-1]
            
            # Extract port and protocol info
            if ':' in name:
                try:
                    # Handle different formats like *:80, 127.0.0.1:3306, etc.
                    if '->' in name:
                        # Connection format: 127.0.0.1:8080->127.0.0.1:41234
                        local_part = name.split('->')[0]
                        status = "ESTABLISHED"
                    else:
                        # Listening format: *:80 or 127.0.0.1:3306
                        local_part = name
                        status = "LISTENING"
                    
                    port = local_part.split(':')[-1]
                    
                    # Determine protocol from the file descriptor
                    proto = "TCP" if "TCP" in line else "UDP" if "UDP" in line else "UNKNOWN"
                    
                    ports.append((port, proto, status, f"{command} ({pid})", user))
                except (IndexError, ValueError):
                    continue
        
        return ports
    
    def list_ports(self):
        """List all active ports with improved formatting"""
        table = PrettyTable(["Port", "Protocol", "Status", "Process (PID)", "User"])
        table.align = "l"
        
        try:
            print("🔍 Scanning active ports...")
            output = subprocess.check_output(
                ["lsof", "-i", "-P", "-n"], 
                universal_newlines=True,
                stderr=subprocess.DEVNULL
            )
            
            ports = self.parse_lsof_output(output)
            
            # Remove duplicates and sort by port number
            unique_ports = {}
            for port, proto, status, process, user in ports:
                key = f"{port}-{proto}-{status}"
                if key not in unique_ports:
                    unique_ports[key] = (port, proto, status, process, user)
            
            # Sort by port number
            sorted_ports = sorted(unique_ports.values(), 
                                key=lambda x: int(x[0]) if x[0].isdigit() else float('inf'))
            
            for port, proto, status, process, user in sorted_ports:
                # Color coding for status
                status_display = f"🟢 {status}" if status == "LISTENING" else f"🔵 {status}"
                table.add_row([port, proto, status_display, process, user])
            
            if not sorted_ports:
                print("ℹ️  No active ports found.")
            else:
                print(f"\n📊 Found {len(sorted_ports)} active connections:")
                print(table)
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error scanning ports: {e}")
        except FileNotFoundError:
            print("❌ 'lsof' command not found. Please install it first.")
    
    def kill_port(self, port: str):
        """Kill processes using a specific port with confirmation"""
        if not port.isdigit():
            print("❌ Invalid port number. Please enter a numeric port.")
            return
        
        try:
            # Find processes using the port
            output = subprocess.check_output(
                ["lsof", "-i", f":{port}"], 
                universal_newlines=True,
                stderr=subprocess.DEVNULL
            )
            
            lines = output.strip().split("\n")[1:]  # Skip header
            if not lines:
                print(f"ℹ️  No processes found using port {port}")
                return
            
            processes = []
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    pid = parts[1]
                    command = parts[0]
                    processes.append((pid, command))
            
            if not processes:
                print(f"ℹ️  No processes found using port {port}")
                return
            
            # Show what will be killed
            print(f"\n🎯 Processes using port {port}:")
            for pid, command in processes:
                print(f"  - {command} (PID: {pid})")
            
            # Confirm before killing
            confirm = input(f"\n⚠️  Kill {len(processes)} process(es)? [y/N]: ").lower()
            if confirm not in ['y', 'yes']:
                print("❌ Operation cancelled.")
                return
            
            # Kill processes
            killed_count = 0
            for pid, command in processes:
                try:
                    subprocess.run(["kill", "-9", pid], check=True, stderr=subprocess.DEVNULL)
                    print(f"✅ Killed {command} (PID: {pid})")
                    killed_count += 1
                except subprocess.CalledProcessError:
                    print(f"❌ Failed to kill {command} (PID: {pid})")
            
            print(f"\n📈 Successfully killed {killed_count}/{len(processes)} processes on port {port}")
            
        except subprocess.CalledProcessError:
            print(f"ℹ️  No processes found using port {port}")
        except FileNotFoundError:
            print("❌ 'lsof' command not found. Please install it first.")
    
    def manage_service(self, action: str, service: str):
        """Manage systemd services with better error handling"""
        valid_actions = ["enable", "disable", "start", "stop", "restart", "status"]
        
        if action not in valid_actions:
            print(f"❌ Invalid action. Valid actions: {', '.join(valid_actions)}")
            return
        
        if not service.strip():
            print("❌ Service name cannot be empty.")
            return
        
        try:
            if action == "status":
                # Special handling for status to show output
                result = subprocess.run(
                    ["systemctl", "status", service], 
                    capture_output=True, 
                    text=True
                )
                print(f"\n📋 Status for service '{service}':")
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)
            else:
                # Confirm dangerous actions
                if action in ["stop", "disable"] and service in ["ssh", "sshd", "networking", "network-manager"]:
                    confirm = input(f"⚠️  Warning: {action}ing {service} might affect connectivity. Continue? [y/N]: ").lower()
                    if confirm not in ['y', 'yes']:
                        print("❌ Operation cancelled.")
                        return
                
                subprocess.run(["systemctl", action, service], check=True, stderr=subprocess.PIPE)
                print(f"✅ Service '{service}' {action}d successfully")
                
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else "Unknown error"
            print(f"❌ Failed to {action} service '{service}': {error_msg.strip()}")
        except FileNotFoundError:
            print("❌ 'systemctl' command not found. This feature requires systemd.")
    
    def show_help(self):
        """Display help information"""
        help_text = """
📚 Available Commands:
  
  list                    - Show all active ports and connections
  kill <port>            - Kill processes using specified port
  enable <service>       - Enable a systemd service
  disable <service>      - Disable a systemd service
  start <service>        - Start a systemd service
  stop <service>         - Stop a systemd service
  restart <service>      - Restart a systemd service
  status <service>       - Show status of a systemd service
  help                   - Show this help message
  clear                  - Clear the screen
  exit                   - Exit PyPort

💡 Examples:
  > list
  > kill 8080
  > stop apache2
  > status nginx
  > enable ssh
"""
        print(help_text)
    
    def run(self):
        """Main interactive loop"""
        print(ASCII_BANNER)
        print("\n🚀 Welcome to PyPort - Enhanced Port Management Tool")
        print("Type 'help' for available commands or 'exit' to quit.\n")
        
        while True:
            try:
                cmd = input("PyPort> ").strip().split()
                
                if not cmd:
                    continue
                
                command = cmd[0].lower()
                
                if command == "list":
                    self.list_ports()
                
                elif command == "kill" and len(cmd) == 2:
                    self.kill_port(cmd[1])
                
                elif command in ["enable", "disable", "start", "stop", "restart", "status"] and len(cmd) == 2:
                    self.manage_service(command, cmd[1])
                
                elif command == "help":
                    self.show_help()
                
                elif command == "clear":
                    os.system('clear' if os.name == 'posix' else 'cls')
                    print(ASCII_BANNER)
                
                elif command == "exit":
                    print("👋 Thanks for using PyPort!")
                    sys.exit(0)
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                
                print()  # Add spacing between commands
                
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using PyPort!")
                sys.exit(0)
            except EOFError:
                print("\n\n👋 Thanks for using PyPort!")
                sys.exit(0)

def main():
    try:
        port_manager = PortManager()
        port_manager.run()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
