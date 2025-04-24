
# Raspberry Pi Zero Python Environment Setup Tutorial

## 1. Why you need *two* package managers on a Pi Zero

Your Raspberry Pi Zero runs two parallel “worlds” of software:

| Layer | Tooling | Typical scope |
|-------|---------|----------------|
| **Operating-system packages** | **`apt`** | Anything the whole OS might use (kernels, libraries, apps, *system* Python modules, …) |
| **Project-specific Python code** | **`pip`** inside a **virtual environment** (managed by **`pyenv-virtualenv`**) | Exactly the set of Python packages one project needs |

Keeping those worlds separate prevents version clashes and keeps student projects reproducible.

---

## 2. `apt`—the Debian package manager

`apt` (Advanced Package Tool) is the command-line front end to Raspberry Pi OS’s package database. It downloads pre-built `.deb` files from the Pi Foundation mirrors, resolves dependencies and installs them system-wide (into `/usr/bin`, `/usr/lib`, `/usr/share`, …).

```bash
# Update package lists (always do this first)
sudo apt update

# Upgrade any out-of-date packages (optional but recommended)
sudo apt full-upgrade
```

### Install the camera driver stack

```bash
sudo apt install python3-picamera2
```

> **Why *not* use `pip` for Picamera2?**  
> Picamera2 contains low-level C/C++ components tightly coupled to the operating system’s camera stack. The Pi Foundation builds those pieces for you and ships them via `apt`, so you avoid a long compile and potential incompatibilities.

---

## 3. Python versions & `pyenv`

Your Pi already has `pyenv` installed.  
`pyenv`’s job is *version management*: it can fetch, compile and keep multiple **complete** Python interpreters under `~/.pyenv/versions/`. You then pick which interpreter you want active in each shell directory.

```bash
pyenv versions          # show everything installed
pyenv global system     # (default) use the OS Python everywhere
```

You can ignore installing a new interpreter for this tutorial—we’ll reuse the system build.

---

## 4. What a virtual environment actually is

A **virtual environment** is just a private directory tree that contains:

* a copy (or thin symlink) of one Python interpreter
* an isolated `site-packages/` directory
* small activation scripts that tweak the shell’s `PATH` and a couple of env-vars

Activating it makes Python **and** `pip` look **first** inside that tree, so anything you install cannot break other projects.

### How it differs from `apt`

| | `virtualenv` + `pip` | `apt` |
|--|---------------------|-------|
| Scope | Only the shell that activates the env | Whole operating system |
| Un-installs | Just remove the env folder | Must keep track of reverse dependencies |
| Version granularity | Any version on PyPI | Whatever the Debian maintainer packaged |

---

## 5. Create a project env called **`cps`**

```bash
pyenv virtualenv --system-site-packages system cps
```

* `system` tells pyenv to clone the OS’s default Python (*not* compile a new one).  
* `--system-site-packages` creates a symlink so the env can *read* globally installed libraries.  
* Anything you `pip install` later still lands in the env’s private directory and does **not** pollute `/usr/lib`.

---

## 6. Using the environment

```bash
# Activate
pyenv activate cps        # or: source ~/.pyenv/versions/cps/bin/activate

# Check you’re in (prompt usually shows "(cps)")
python -V

# Install your project libraries
pip install opencv-python numpy imagezmq

# Work on your code...
python my_robot_script.py

# When done
deactivate
```

---

## 7. What is `pip` and how does it differ from `apt`?

* **pip** is Python’s package manager for code published on **PyPI**, the Python Package Index.
* It installs **into the currently-active interpreter**.
* `apt` never looks at PyPI—it installs Debian packages maintained by distro volunteers.

Thus you can happily mix them: Picamera2 from `apt`, OpenCV from `pip`, all living together inside the same virtualenv.

---

## 8. House-keeping: deleting an env you no longer need

```bash
pyenv uninstall cps
```

---

## 9. Quick-reference cheat-sheet

| Action | Command |
|--------|---------|
| Update system repo indices | `sudo apt update` |
| Install Picamera2 | `sudo apt install python3-picamera2` |
| Create env (with global packages) | `pyenv virtualenv --system-site-packages system cps` |
| Activate env | `pyenv activate cps` |
| Deactivate env | `deactivate` |
| Install project packages | `pip install opencv-python numpy imagezmq` |
| List installed pip packages | `pip list` |
| Delete env | `pyenv uninstall cps` |
