# Automated Network Login Script
---
## Table of Contents
  1. [Introduction](#Introduction)
  2. [Features](#Features)
  3. [Requirements](#Requirements)
  4. [Installation](#Installation)
  5. [Usage](#Usage)
  6. [First time setup](#First-Time-Setup)
  7. [Subsequent Logins](#Subsequent-Logins)
  8. [How it works](#Working)
  9. [Troubleshooting](#Troubleshooting)
---
## Introduction
This Python script automates the process of connecting to a Wi-Fi network and logging in to a captive portal, such as those used in campus networks. 

The script:
- Connects to a specified Wi-Fi network.
- Automates browser login using credentials securely stored and encrypted.
- Provides retry mechanisms for both network connection and login processes.
- Notifies the user of a successful login via desktop notifications.
---
## Features
- Automates Wi-Fi Connection: Automatically connects to networks matching specific criteria ("BPGC" in this case)
- Encrypted Credential Storage: Protects sensitive login information using encryption.
- Retry Mechanism: Ensures reliable operation with multiple retry attempts for both network connection and login.
- Browser Automation: Uses Selenium to handle browser interactions with the login portal.
- Notifications: Displays a desktop notification upon successful login.
---
## Requirements
Python 3.8 or later
The following Python libraries:
- `selenium`
- `webdriver-manager`
- `plyer`
- `cryptography`
- `importlib`
  
Google Chrome installed on your system

Administrator privileges to execute certain network commands (on Windows)

---
## Installation
Clone the repository or download the script:

```bash
git clone https://github.com/your-repo/automated-network-login.git
cd automated-network-login
```

Install the required Python libraries:
```bash
pip install selenium webdriver-manager plyer cryptography
```
Ensure you have Google Chrome installed. The script uses webdriver-manager to automatically download the appropriate version of ChromeDriver.

Also make sure to store the main program in a separate folder as the chromedriver and login credentials are set to be stored in the same folder as the main code

Grant the necessary permissions for the script to execute.

---
## Usage
### First-Time-Setup
Run the script:

```bash
python your_script.py
```
Here your_script is the name of the file you have saved this code as
If Login.py is not found in the directory, the script will prompt you to:

Enter your network username.

Enter your network password.

These credentials will be securely encrypted and stored in a Login.py file for future use.

The script will then attempt to connect to a network and log in automatically.

### Subsequent-Logins
Once the setup is complete:

Simply run the script:
```bash
python your_script.py
```
The script will automatically:
Connect to the Wi-Fi network.
Log in to the captive portal using stored credentials.
---
## Working
### Credential Storage:

Credentials are encrypted (via the cryptography library) and saved in a Login.py file.

### Network Connection:

The script uses netsh wlan commands to identify and connect to available Wi-Fi networks that match a specified pattern.

### Browser Automation:

The selenium library is used to automate browser interactions with the login portal.

ChromeDriver (managed by webdriver-manager) is used to control Google Chrome.

### Retry Mechanisms:

Both network connection and login processes have a retry mechanism with configurable attempts and delays.

### Notifications:

Uponn successful logn, the script sends a desktop notification using plyer library

---
## Troubleshooting
### ChromeDriver Issues:

Ensure that Google Chrome is installed and up-to-date.

If ChromeDriver fails to install, manually download the correct version and place it in the script directory.

### Permission Errors:

Run the script as an administrator, especially if it fails to execute netsh commands.

### Credential Decryption Issues:

Ensure the encryption key matches the one used when creating Login.py
.
If Login.py is corrupted or missing, delete it and re-run the script to recreate it.

### Wi-Fi Connection Fails:

Verify that the target network is available and that the system has the necessary permissions to connect.
