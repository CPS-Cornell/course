# **Configuring Wi-Fi on Raspberry Pi Using NetworkManager and `raspi-config`**

## **Step 1: Disable Auto-Connect Configuration**
By default, NetworkManager is preconfigured to connect to RedRover. If you want to change the network that your Raspberry Pi Zero connects to, you need to remove the configuration file that NetworkManager uses to connect to the wifi automatically and create a manual connection.

Rather than delete this configuration file, we are going to move it to a different location and create a backup, so that you can undo this configuration change in the future. 

1. Open a terminal on your Raspberry Pi.
2. Move the **preconfigured network connection file** to a backup location:
   ```bash
   sudo mv /etc/NetworkManager/system-connections/preconfigured.nmconnection ~/preconfigured.nmconnection.bak
   ```
   This moves the file to the home directory so it can be restored if needed.

3. Reload NetworkManager to apply the changes:
   ```bash
   sudo systemctl restart NetworkManager
   ```
   This ensures that the removed configuration no longer affects network connections.

## **Undoing the Configuration to Reconnect to RedRover Automatically**

If you want your Raspberry Pi to reconnect to the RedRover network automatically, you can restore the original configuration file.

1. Open a terminal on your Raspberry Pi.
2. Move the backup configuration file back to its original location:
    ```bash
    sudo mv ~/preconfigured.nmconnection.bak /etc/NetworkManager/system-connections/preconfigured.nmconnection
    ```
    This restores the original configuration file that was moved earlier.

3. Reload NetworkManager to apply the changes:
    ```bash
    sudo systemctl restart NetworkManager
    ```
    This ensures that the restored configuration takes effect and the Raspberry Pi will automatically connect to RedRover.

4. Verify the connection by checking the connected Wi-Fi SSID:
    ```bash
    iwgetid
    ```
    This will display the current SSID that the Raspberry Pi is connected to, confirming it is connected to RedRover.
---

## **Step 2: Configure a New Wi-Fi Connection Using `raspi-config`**
Once the default configuration has been removed, use `raspi-config` to set up a new connection.

1. Open `raspi-config`:
   ```bash
   sudo raspi-config
   ```
2. Navigate to:
   - **System Options**  
   - **Wireless LAN**
3. Enter the **SSID (network name)** and **Wi-Fi passphrase** when prompted.
4. Exit `raspi-config` and allow the Raspberry Pi to apply the settings.

---

## **Step 3: Verify the Connection**
After configuring the connection, confirm that the Raspberry Pi is connected to the new Wi-Fi network.

1. **Check internet connectivity** by running:
   ```bash
   ping google.com
   ```
   This will send continuous pings to Google’s servers. If the connection is successful, you will see responses showing latency times.

2. **Stop the ping test** by pressing:
   ```
   CTRL + C
   ```

3. **Verify the connected Wi-Fi SSID**:
   ```bash
   iwgetid
   ```
   This will display the current SSID that the Raspberry Pi is connected to.

---

## **Step 4: Important Notes About Wi-Fi SSIDs**
- **SSID names are case-sensitive and space-sensitive**. Be sure to enter them exactly as they appear in the network settings.
- **Apostrophes (`'`) in SSIDs may cause issues** with some connection methods. If `raspi-config` fails to connect to a network with an apostrophe in the SSID, try manually configuring it using `wpa_supplicant.conf` (this is an advanced method and may require additional troubleshooting).

---

## **Conclusion**
By following these steps, you have configured your Raspberry Pi to **disable auto-connect**, **set up a new Wi-Fi connection**, and **verify the connection** using `ping` and `iwgetid`. If you experience any connection issues, ensure that the Wi-Fi SSID and passphrase are correct and try restarting the Raspberry Pi.
