# WebRTC on Raspberry Pi Zero 2 W

## Setup Zero 

**Assumptions:**

  * You have a Raspberry Pi Zero 2 W with Raspberry Pi OS (Bullseye or later, Lite version recommended for performance) installed and configured for network access (Wi-Fi or Ethernet adapter).
  * You have a Raspberry Pi Camera Module (v1, v2, or v3) correctly connected and enabled via `sudo raspi-config` (Interface Options -\> Camera -\> Enable).
  * You have SSH access to your Raspberry Pi or can work directly from its command line.
  * Your Raspberry Pi and laptop are on the same local network.

**Steps to Set Up WebRTC with MediaMTX:**

**1. Update Your Raspberry Pi:**

It's always a good practice to start with an updated system.

```bash
sudo apt update
sudo apt full-upgrade -y
```

Reboot if necessary:

```bash
sudo reboot
```

**2. Install `libcamera-apps` (if not already present):**

MediaMTX will use `libcamera` to access the camera. While MediaMTX often bundles what it needs or uses system libraries, ensuring `libcamera-apps` (which provides tools like `libcamera-vid`) is installed can be helpful for testing and ensures all dependencies are met.

```bash
sudo apt install -y libcamera-apps
```

Test your camera quickly with:

```bash
libcamera-hello -t 5000
```

This should show a 5-second preview. If you see an error, troubleshoot your camera connection and configuration.

## Setup the WebRTC Server

1. Download and Install MediaMTX:**

MediaMTX (formerly rtsp-simple-server) provides pre-compiled binaries, which makes installation easy.

  * **Check your Pi's architecture:**
    The Raspberry Pi Zero 2 W has an ARMv7 (32-bit) or ARMv8 (64-bit, if running a 64-bit OS) processor. You can check your OS architecture with `uname -m`. If it shows `armv7l`, it's 32-bit. If it shows `aarch64`, it's 64-bit.

  * **Go to the MediaMTX GitHub Releases page:**
    Open a web browser and search for "MediaMTX GitHub Releases" or go directly to `https://github.com/bluenviron/mediamtx/releases`.

  * **Download the correct binary for your Pi:**
    Look for the latest release. You'll want an archive file (`.tar.gz`) for Linux ARM.

      * For a 32-bit OS (armv7l): `mediamtx_vX.Y.Z_linux_armv7.tar.gz`
      * For a 64-bit OS (aarch64): `mediamtx_vX.Y.Z_linux_arm64.tar.gz`
        (Replace `vX.Y.Z` with the actual latest version number).

    You can download it directly on your Pi using `wget`. Right-click the link to the desired file on the GitHub releases page and "Copy link address". Then, on your Pi:

    ```bash
    # Example for 64-bit OS and version 1.9.1 (replace with actual latest URL)
    wget https://github.com/bluenviron/mediamtx/releases/download/v1.9.1/mediamtx_v1.9.1_linux_arm64.tar.gz
    ```

  * **Extract the archive:**

    ```bash
    # Replace with the actual filename you downloaded
    tar -xvf mediamtx_vX.Y.Z_linux_arm64.tar.gz
    ```

    This will extract two files: `mediamtx` (the executable) and `mediamtx.yml` (the configuration file).

**2. Configure MediaMTX (`mediamtx.yml`):**

This is the crucial step to tell MediaMTX to use your Raspberry Pi camera and enable WebRTC.

  * **Open `mediamtx.yml` for editing:**

    ```bash
    nano mediamtx.yml
    ```

  * **Key Configuration Sections for WebRTC and Pi Camera:**
    MediaMTX has many default settings that are often fine. We need to ensure the WebRTC listener is enabled (it usually is by default on port `8888`) and configure a path for your camera.

    Modify or ensure the following settings are present and correctly configured:

    ```yaml
    # Global settings (usually fine by default)
    # webRTCServerAddress: :8888/ # This is the default WebRTC port for HTTP
    # webRTCICEServers: [] # For local network, usually no STUN/TURN servers needed.
                          # For streaming outside your local network, you'd configure STUN/TURN servers here.

    # Paths: This is where you define your camera stream
    paths:
      # 'cam' is a name for your stream path, you can change it if you like.
      # The stream will be accessible at /cam (e.g., http://<pi_ip>:8888/cam)
      cam:
        # Source for the Raspberry Pi Camera using libcamera
        source: rpiCamera

        # rpiCamera specific settings (libcamera backend)

        # Adjust these to your needs and Pi Zero 2 W capabilities for low latency
        rpiCameraWidth: 1280        # Resolution width (e.g., 640, 1280)
        rpiCameraHeight: 720       # Resolution height (e.g., 480, 720)
        rpiCameraFps: 20           # Frames per second (e.g., 15, 20, 25, 30)
                                    # Higher FPS needs more processing; 15-20 is often good for Zero 2 W
        rpiCameraHFlip: false      # Horizontal flip (true or false)
        rpiCameraVFlip: false      # Vertical flip (true or false)
        # rpiCameraId: 0             # Camera ID, usually 0 if you have one camera
        # rpiCameraMode: ''          # Specific sensor mode, usually auto is fine
        # rpiCameraBitrate: 1000000  # Bitrate (bits per second), e.g., 1 Mbps. Adjust for quality vs. bandwidth.
                                    # For low latency, don't set too high.
        # rpiCameraAfMode: "auto" # Auto-focus mode (continuous, auto, manual) - depends on camera module
        # rpiCameraLensPosition: 0.0 # For manual focus, if supported

        # Enable WebRTC for this path (usually enabled by default if WebRTC is globally on)
        # publish: true # Not strictly needed for source-initiated paths like rpiCamera
        # read: true    # Ensure clients can read/view the stream

        # Optional: Add RTSP if you want to access it via VLC as well
        # rtsp: true
    ```

  * **Explanation of `mediamtx.yml` settings:**

      * `webRTCServerAddress`: Defines the port MediaMTX listens on for WebRTC connections. The default `:8888` means it will serve an HTML page with the player.
      * `paths`: This is a dictionary where each key is a unique stream path (e.g., `cam`).
      * `source: rpiCamera`: Tells MediaMTX to use a Raspberry Pi camera as the source.
      * `rpiCameraRaspiStill: false`: **Crucial for modern Raspberry Pi OS.** This directs MediaMTX to use the `libcamera` framework. If this was `true`, it would try to use the older `raspivid` which is deprecated.
      * `rpiCameraWidth`, `rpiCameraHeight`, `rpiCameraFps`: Adjust these for your desired balance of quality, performance, and latency. The Pi Zero 2 W can handle 720p at 15-30fps for streaming, but lower resolutions like 640x480 might yield even lower latency if acceptable.
      * `rpiCameraHFlip`, `rpiCameraVFlip`: Set to `true` if your camera image is upside down or mirrored.
      * `rpiCameraBitrate`: Controls the video quality and bandwidth usage. Lower can mean lower latency but also lower quality.
      * `rpiCameraAfMode`, `rpiCameraLensPosition`: Relevant if you have a Camera Module 3 or other autofocus-capable module.

  * **Save the file and exit nano:** `Ctrl+X`, then `Y`, then `Enter`.

**5. Run MediaMTX:**

Navigate to the directory where you extracted MediaMTX and run it:

```bash
./mediamtx
```

You should see log output in your terminal indicating that MediaMTX has started, that it's listening on various ports (including HTTP/WebRTC, typically 8888, and RTSP, typically 8554 if enabled), and that it's trying to access your camera.

Look for lines like:

```
INF MediaMTX vX.Y.Z
INF [path cam] [rpiCamera] opened
INF [WebRTC] listener opened on :8888 (HTTP)
INF [RTSP] listener opened on :8554 (TCP) (if RTSP is enabled for the path or globally)
```

If you see errors related to the camera, double-check your `mediamtx.yml` configuration, camera connection, and `libcamera` functionality.

**6. Access the WebRTC Stream on Your Laptop:**

  * **Find your Raspberry Pi's IP address:**
    On the Pi, run:

    ```bash
    hostname -I
    ```

    This will show you the IP address (e.g., `192.168.1.10`).

  * **Open a web browser on your laptop:**
    Use a modern browser that supports WebRTC (Chrome, Firefox, Edge, Safari).

  * **Navigate to the WebRTC stream URL:**
    The URL will be `http://<YOUR_RASPBERRY_PI_IP>:8888/cam`
    (Replace `<YOUR_RASPBERRY_PI_IP>` with the actual IP address and `cam` with the path name you used in `mediamtx.yml`).

    You should see a simple web page with a video player, and after a brief moment, your Raspberry Pi's camera stream should appear with low latency.

## MedianMTX Service (Optional)

Running MediaMTX directly in the terminal means it will stop when you close the terminal or SSH session. To run it persistently, you can set it up as a systemd service.

  * **Create a service file:**

    ```bash
    sudo nano /etc/systemd/system/mediamtx.service
    ```

  * **Paste the following content into the file:**
    (Adjust `User`, `WorkingDirectory`, and `ExecStart` paths if your username is not `pi` or if you placed MediaMTX elsewhere. Assuming you extracted it in `/home/pi/mediamtx_folder_name`)

    ```ini
    [Unit]
    Description=MediaMTX RTSP/RTMP/HLS/WebRTC server
    After=network.target
    Wants=network.target
    
    [Service]
    User=CPSPi
    WorkingDirectory=/home/CPSPi/mediamtx
    ExecStart=/home/CPSPi/mediamtx/mediamtx /home/CPSPi/mediamtx/mediamtx.yml
    Restart=always
    RestartSec=5
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=mediamtx
    
    [Install]
    WantedBy=multi-user.target
    ```

    **Make sure the `WorkingDirectory` and `ExecStart` paths are correct\!** For `ExecStart`, provide the full path to the `mediamtx` executable and the full path to your `mediamtx.yml` file.

  * **Save and close the service file:** `Ctrl+X`, `Y`, `Enter`.

  * **Reload systemd, enable, and start the service:**

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable mediamtx.service
    sudo systemctl start mediamtx.service
    ```

  * **Check the status:**

    ```bash
    sudo systemctl status mediamtx.service
    ```

    You can also view logs with:

    ```bash
    sudo journalctl -u mediamtx -f
    ```

**Troubleshooting and Tips for Low Latency:**

  * **Network:** A strong, stable Wi-Fi connection is paramount. The Pi Zero 2 W's Wi-Fi can be a bottleneck. If latency is an issue, try moving closer to your router or using a less congested Wi-Fi channel. A wired USB Ethernet adapter can significantly improve stability and reduce latency.
  * **Resolution/FPS/Bitrate:** If latency is still too high, try reducing `rpiCameraWidth`, `rpiCameraHeight`, or `rpiCameraFps` in `mediamtx.yml`. A lower bitrate can also help but will reduce quality.
  * **CPU Load:** Use `htop` on the Pi to monitor CPU usage. If it's consistently very high (e.g., \>80-90% across cores), the Pi might be struggling. This usually means hardware encoding isn't working correctly or the settings are too demanding. MediaMTX using `libcamera` should leverage hardware H.264 encoding.
  * **Client-Side:** Ensure your laptop isn't overloaded, and the browser is up to date.
  * **Firewall:** If you're using a firewall on your Raspberry Pi or laptop, ensure port `8888` (or your configured WebRTC port) and any ports used for WebRTC data channels (usually a dynamic range over UDP) are allowed. For local networks, this is typically not an issue unless you have custom firewall rules.
  * **MediaMTX Logs:** The output from `./mediamtx` (or `journalctl -u mediamtx -f` if running as a service) is invaluable for diagnosing issues.

This detailed guide should help you get WebRTC streaming up and running with MediaMTX on your Raspberry Pi Zero 2 W. Remember that achieving sub-300ms consistently depends on optimizing all parts of the chain, especially the network and encoding settings.