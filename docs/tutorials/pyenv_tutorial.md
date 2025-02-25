# Pyenv Virtual Environments Setup Guide

## 1. Installing Pyenv

More detailed instruction for installation can be found [here](https://github.com/pyenv/pyenv) for Mac/Linux and [here](https://github.com/pyenv-win/pyenv-win) for Windows.

### Mac Installation

1. **Install Homebrew (if not already installed):**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Pyenv using Homebrew:**
   ```bash
   brew update
   brew install pyenv
   ```

3. **Configure the shell to use Pyenv:**
   - For **Zsh** (default on macOS):
     ```bash
     echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
     echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
     echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
     source ~/.zshrc
     ```
   - For **Bash**:
     ```bash
     echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
     echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
     echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
     source ~/.bashrc
     ```

4. **Verify Installation:**
   ```bash
   pyenv --version
   ```

### Linux Installation

1. **Install Dependencies (Required for Pyenv to work properly):**
   
   On **Debian/Ubuntu-based** systems:
   ```bash
   sudo apt update && sudo apt install -y make build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
   libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
   ```

2. **Install Pyenv:**
   ```bash
   curl https://pyenv.run | bash
   ```
   
3. **Configure the shell to use Pyenv:**
   - For **Bash**:
     ```bash
     echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
     echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
     echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
     source ~/.bashrc
     ```


4. **Verify Installation:**
   ```bash
   pyenv --version
   ```

### Windows Installation (Using Pyenv-Win)

1. **Install Pyenv-Win**
   ```powershell
   git clone https://github.com/pyenv-win/pyenv-win.git $env:USERPROFILE\.pyenv
   ```
   
2. **Add Pyenv to the system PATH:**
   Open PowerShell and run:
   ```powershell
   [System.Environment]::SetEnvironmentVariable("PYENV", "$env:USERPROFILE\.pyenv", "User")
   [System.Environment]::SetEnvironmentVariable("PYENV_ROOT", "$env:PYENV", "User")
   [System.Environment]::SetEnvironmentVariable("Path", "$env:PYENV\bin;$env:PYENV\shims;" + $env:Path, "User")
   ```

3. **Restart PowerShell and Verify Installation:**
   ```powershell
   pyenv --version
   ```

---

## 2. Setting Up Virtual Environments in Pyenv

### Installing a Specific Python Version
To install a specific version of Python using Pyenv, run:
```bash
pyenv install 3.9.7
```
Replace `3.9.7` with the desired Python version.

### Listing Available Python Versions
To see installed Python versions:
```bash
pyenv versions
```

To see all available Python versions:
```bash
pyenv install --list
```

---

## 3. Activating and Deactivating Virtual Environments

### Creating a Virtual Environment
To create a new virtual environment:
```bash
pyenv virtualenv 3.9.7 myenv
```

### Activating a Virtual Environment
To activate the environment:
```bash
pyenv activate myenv
```

### Deactivating a Virtual Environment
To deactivate an environment:
```bash
pyenv deactivate
```

---

## 4. Managing Packages Within a Virtual Environment

### Installing Packages
Once inside an environment, install packages using:
```bash
pip install numpy pandas matplotlib
```

### Listing Installed Packages
To list all installed packages:
```bash
pip list
```

### Updating Packages
To update all packages:
```bash
pip install --upgrade pip
pip list --outdated | awk '{print $1}' | xargs pip install --upgrade
```

### Removing a Package
To remove a package:
```bash
pip uninstall package-name
```

---

## 5. Deleting Virtual Environments
To delete an environment:
```bash
pyenv virtualenv-delete myenv
```

### Force Deleting an Environment (Manually)
If needed, manually remove an environment:
```bash
rm -rf ~/.pyenv/versions/myenv
```
(For Linux/Mac users, adjust the path accordingly.)

For Windows:
```powershell
Remove-Item -Recurse -Force $env:PYENV\.pyenv\versions\myenv
```

---

## Final Notes
- Always **activate** the correct virtual environment before running scripts.
- Use `pip install` for package management within environments.
- Regularly update Pyenv with:
  ```bash
  pyenv update
  ```

By following this guide, you’ll efficiently manage Python environments across Windows, Mac, and Linux using Pyenv! 
