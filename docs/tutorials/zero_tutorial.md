# Raspberry Pi Zero 2 W: Setup and Usage Guide

## 1. Overview and Prerequisites

You will be working with a Raspberry Pi Zero 2 W that has been preconfigured to:
- Automatically join the **RedRover** Wi-Fi network.
- Present a **serial console** over the USB micro port so you can connect via a serial terminal (using VS Code or PuTTY).

### Default Login Credentials
- **Username**: `CPSPi`
- **Password**: `CPS`

### Software Setup
- The Pi has **Pyenv** installed, with a Python virtual environment called **`cps`**.
- You will use **VS Code** for:
  - Serial communication (via the "Serial Terminal" plugin).
  - SSH connections (via the integrated terminal or an SSH plugin).
  - File transfers using `scp` (Secure Copy Protocol).

- **Optional**: Instructions for using **PuTTY** (external serial terminal tool) are included but not recommended.

---

## 2. Setting Up a Serial Connection

### 2.1 Using VS Code Serial Terminal (Recommended)

1. **Install the Serial Terminal plugin**:
   - Open **VS Code**.
   - Go to **Extensions** (square icon in the left toolbar).
   - Search for **"Serial Terminal"** and install it.

2. **Connect your Pi to your computer**:
   - Use a **USB data cable** (micro USB to USB-A or USB-C).
   - Plug it into the **USB data port** on the Pi Zero (not the power-only port).

3. **Open the Serial Terminal in VS Code**:
   - Open the **Serial Terminal** plugin.
   - Select the appropriate **port**:
     - On **Windows**, it may be `COM3`, `COM4`, etc.
     - On **macOS/Linux**, it may be `/dev/tty.usbmodemXXXX` or `/dev/ttyUSB0`.

4. **Set the baud rate**:
   ```plaintext
   Baud Rate: 115200
   ```

5. **Login to the Pi**:
   - When prompted, enter:
     ```plaintext
     Username: CPSPi
     Password: CPS
     ```

### 2.2 Using PuTTY (Optional)

1. **Install PuTTY** (if not already installed):
   - Windows: [https://www.putty.org/](https://www.putty.org/)
   - Mac/Linux: Install via a package manager:
     ```bash
     brew install putty   # macOS
     sudo apt-get install putty  # Linux
     ```

2. **Identify the serial port**:
   - **Windows**: Look in Device Manager (`COMx`).
   - **Mac/Linux**: Run:
     ```bash
     ls /dev/tty.*
     ```

3. **Open PuTTY and configure the connection**:
   - **Connection type**: Serial.
   - **Serial line**: `COM3` (Windows) or `/dev/ttyUSB0` (macOS/Linux).
   - **Speed**: `115200`.
   - Click **Open**.

4. **Login to the Pi**:
   - Enter:
     ```plaintext
     Username: CPSPi
     Password: CPS
     ```

---

## 3. Activating the Python Virtual Environment

Once logged in via serial, you should see a prompt like:

```bash
CPSPi@raspberrypi:~ $
```

### Activate the Python virtual environment:
```bash
pyenv activate cps
```

Your prompt should now display `(cps)`:
```bash
(cps) CPSPi@raspberrypi:~ $
```

---

## 4. Connecting via SSH

### 1. Get the Pi’s IP Address
Run the following command in the serial terminal:
```bash
ifconfig
```
Look for the **`wlan0`** entry and find the **inet** IP address (e.g., `192.168.1.42`).

### 2. Open a terminal on your computer (VS Code integrated terminal or system terminal)
Run:
```bash
ssh CPSPi@<ip_address>
```
Example:
```bash
ssh CPSPi@192.168.1.42
```
Enter the **password: `CPS`** when prompted.

### 3. Activate the Python Virtual Environment
```bash
pyenv activate cps
```

---

## 5. Transferring Files Using `scp`

1. **Ensure the file is in a known directory** on your computer.
2. **Use `scp` to copy the file to the Pi**:
   ```bash
   scp <path_to_local_file> CPSPi@<ip_address>:<destination_path_on_pi>
   ```
   Example:
   ```bash
   scp lab1.py CPSPi@192.168.1.42:~
   ```
   (Enter the `CPS` password when prompted.)

3. **Check the file on the Pi**:
   ```bash
   ls
   ```

4. **Organize your labs**:
   ```bash
   mkdir lab1
   mv lab1.py lab1/
   cd lab1
   ```

---

## 6. Installing Python Packages with `pip`

Inside the `cps` virtual environment, install packages as needed:

```bash
pip install <package_name>
```

Example:
```bash
pip install numpy
```

To verify installation:
```bash
pip list
```

---

## 7. Linux Command Cheat Sheet

| Command       | Description                                                    | Example                           |
|--------------|----------------------------------------------------------------|-----------------------------------|
| **ls**       | List files and directories.                                    | `ls`                             |
| **mkdir**    | Create a directory.                                            | `mkdir myFolder`                 |
| **cd**       | Change directory.                                              | `cd myFolder`                     |
| **pwd**      | Show current directory.                                        | `pwd`                            |
| **rm**       | Remove a file.                                                 | `rm file.txt`                     |
| **rm -r**    | Remove a directory and its contents.                           | `rm -r myFolder`                  |
| **cp**       | Copy a file or directory.                                      | `cp file1.txt file2.txt`         |
| **mv**       | Move or rename a file.                                         | `mv oldName.txt newName.txt`      |
| **ifconfig** | Display network interface info (IP address, etc.).             | `ifconfig`                        |
| **sudo**     | Execute a command with admin privileges.                       | `sudo apt-get update`            |
| **ping**     | Check network connectivity.                                    | `ping www.google.com`             |
| **apt-get**  | Install/remove software packages (system-wide).                | `sudo apt-get install python3`    |

**Warning**: Use `sudo rm -r` with caution. It can delete important files!

---

## 8. Next Steps

### **Practice**:
- Create folders for each lab and organize files.
- Transfer files using `scp`.
- Install packages in your `cps` environment.
- Explore system commands (`ifconfig`, `sudo`, `ping`, etc.).

### **Keep your system updated**:
```bash
sudo apt-get update
sudo apt-get upgrade
```

---

## That’s It!
You now have a reliable workflow for:
- Serial connection via VS Code (or PuTTY).
- SSH login and file transfers (`scp`).
- Python virtual environment management.
- Installing packages with `pip`.
- Basic Linux commands.