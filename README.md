# PyPort 🚀

**PyPort** is a powerful, user-friendly command-line tool for managing system ports and services on Linux systems. Built with Python, it provides an intuitive interface for monitoring active connections, killing processes, and managing systemd services.

```
██████╗ ██╗   ██╗██████╗  ██████╗ ██████╗ ████████╗
██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
██████╔╝ ╚████╔╝ ██████╔╝██║   ██║██████╔╝   ██║   
██╔═══╝   ╚██╔╝  ██╔═══╝ ██║   ██║██╔══██╗   ██║   
██║        ██║   ██║     ╚██████╔╝██║  ██║   ██║   
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
```

## ✨ Features

- **Port Management**: List active ports, kill processes using specific ports
- **Service Control**: Start, stop, enable, disable systemd services
- **Remote Scanning**: Scan ports on remote hosts
- **Safety First**: Confirmation prompts for dangerous operations
- **User-Friendly**: Clear visual feedback with emojis and colors
- **Smart Filtering**: View all ports or filter by specific port number
- **Error Handling**: Robust error handling with helpful messages

## 🔧 Requirements

- **OS**: Linux (Ubuntu, Debian, CentOS, etc.)
- **Python**: 3.6 or higher
- **Privileges**: Root/sudo access required
- **Dependencies**: 
  - `lsof` (usually pre-installed)
  - `systemctl` (systemd systems)
  - `prettytable` Python package

## 📦 Installation

1. **Clone or download** the script:
   ```bash
   wget https://raw.githubusercontent.com/yourusername/pyport/main/pyport.py
   # or
   curl -O https://raw.githubusercontent.com/yourusername/pyport/main/pyport.py
   ```

2. **Install Python dependencies**:
   ```bash
   pip3 install prettytable
   ```

3. **Make executable**:
   ```bash
   chmod +x pyport.py
   ```

4. **Run with sudo**:
   ```bash
   sudo python3 pyport.py
   ```

## 🚀 Usage

### Basic Commands

```bash
sudo python3 pyport.py
```

Once running, you'll see the interactive prompt:

```
PyPort> 
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list` | Show all active ports | `list` |
| `list <port>` | Show specific port info | `list 3000` |
| `kill <port>` | Kill processes on port | `kill 8080` |
| `start <service>` | Start systemd service | `start nginx` |
| `stop <service>` | Stop systemd service | `stop apache2` |
| `restart <service>` | Restart systemd service | `restart mysql` |
| `enable <service>` | Enable service at boot | `enable ssh` |
| `disable <service>` | Disable service at boot | `disable nginx` |
| `status <service>` | Check service status | `status docker` |
| `scan <host>` | Scan common ports on host | `scan 192.168.1.1` |
| `scan <host> <port>` | Scan specific port on host | `scan google.com 80` |
| `help` | Show help information | `help` |
| `clear` | Clear the screen | `clear` |
| `exit` | Exit PyPort | `exit` |

## 📋 Examples

### Port Management
```bash
# List all active connections
PyPort> list

# Check what's running on port 3000
PyPort> list 3000

# Kill all processes using port 8080
PyPort> kill 8080
```

### Service Management
```bash
# Check nginx status
PyPort> status nginx

# Stop Apache web server
PyPort> stop apache2

# Start and enable SSH service
PyPort> start ssh
PyPort> enable ssh
```

### Network Scanning
```bash
# Scan common ports on local network device
PyPort> scan 192.168.1.100

# Check if website is accessible on port 443
PyPort> scan github.com 443
```

## 🛡️ Safety Features

PyPort includes several safety mechanisms:

- **Confirmation prompts** before killing processes or stopping critical services
- **Warning messages** for potentially dangerous operations (like disabling SSH)
- **Input validation** to prevent invalid commands
- **Clear feedback** about what actions are being performed

Example safety prompt:
```
⚠️  Warning: stopping ssh might affect connectivity. Continue? [y/N]:
```

## 📊 Sample Output

```bash
PyPort> list

🔍 Scanning active ports...

📊 Found 8 active connections:
+------+----------+------------------+-------------------+--------+
| Port | Protocol | Status           | Process (PID)     | User   |
+------+----------+------------------+-------------------+--------+
| 22   | TCP      | 🟢 LISTENING     | sshd (1234)       | root   |
| 80   | TCP      | 🟢 LISTENING     | nginx (5678)      | www    |
| 3000 | TCP      | 🟢 LISTENING     | node (9012)       | user   |
| 443  | TCP      | 🟢 LISTENING     | nginx (5679)      | www    |
+------+----------+------------------+-------------------+--------+
```

## 🔍 Troubleshooting

### Common Issues

**"Permission denied" error**:
```bash
# Solution: Run with sudo
sudo python3 pyport.py
```

**"lsof command not found"**:
```bash
# Ubuntu/Debian:
sudo apt-get install lsof

# CentOS/RHEL:
sudo yum install lsof
```

**"prettytable module not found"**:
```bash
# Install the required Python package
pip3 install prettytable
```

**Service commands not working**:
- Ensure you're on a systemd-based Linux distribution
- Check if the service name is correct: `systemctl list-units --type=service`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup
```bash
git clone https://github.com/yourusername/pyport.git
cd pyport
pip3 install -r requirements.txt
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

PyPort requires root privileges and can kill processes or stop services. Use with caution, especially in production environments. Always test commands in a safe environment first.

## 🆘 Support

If you encounter issues:

1. Check the [troubleshooting section](#-troubleshooting)
2. Open an issue on GitHub
3. Provide your OS version, Python version, and error messages

## 🎯 Roadmap

- [ ] Add configuration file support
- [ ] Implement logging functionality  
- [ ] Add Docker container management
- [ ] Create GUI version
- [ ] Add port forwarding features
- [ ] Support for Windows systems

---

**Made with ❤️ for system administrators and developers**

*PyPort - Making port management simple and safe!*
