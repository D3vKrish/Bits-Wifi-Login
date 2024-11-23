import os
import subprocess
import sys
import time
import shutil

# Function to install required Python packages only if not installed
def install_package(package_name):
    try:
        # Check if the package is already installed
        subprocess.check_call([sys.executable, "-m", "pip", "show", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        # If not installed, install the package
        print(f"Installing missing package: {package_name}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Install required packages
required_packages = ["selenium", "webdriver-manager", "plyer", "cryptography", "importlib"]
for package in required_packages:
    install_package(package)

# Importing the newly installed libraries
import importlib
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from plyer import notification

# Key for encrypting and decrypting the username and password
key = "GEmycEl1J8Jq7mVUy0ji7eyYS3hJLLN8s9L2g6fPbBw="

#Site to log into
site = 'https://campnet.bits-goa.ac.in:8090/httpclient.html'

class Browser:
    browser = None

    def __init__(self):
        # Get the current directory of the script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        chromedriver_path = os.path.join(current_dir, "chromedriver.exe")

        if os.path.exists(chromedriver_path):
            print("Using existing ChromeDriver.")
            service = Service(executable_path=chromedriver_path)
        else:
            print("ChromeDriver not found. Downloading...")
            # Use webdriver-manager to download the driver
            downloaded_driver_path = ChromeDriverManager().install()

            # Move the downloaded driver to the current directory
            shutil.copy(downloaded_driver_path, chromedriver_path)
            print(f"ChromeDriver downloaded and moved to: {chromedriver_path}")

            # Create service using the moved driver
            service = Service(executable_path=chromedriver_path)

        # Initialize the browser
        self.browser = webdriver.Chrome(service=service, options=self.get_chrome_options())

    def get_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode (optional)
        options.add_argument('--disable-gpu')  # Disable GPU acceleration
        return options

    def open(self, url: str):
        self.browser.get(url)

    def close_browser(self):
        self.browser.quit()

    def add_input(self, by: By, value: str, text: str):
        field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((by, value))
        )
        field.send_keys(text)

    def click_button(self, by: By, value: str):
        button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((by, value))
        )
        button.click()

    def login_net(self, username: str, password: str):
        self.add_input(by=By.ID, value='username', text=username)
        self.add_input(by=By.ID, value='password', text=password)
        self.click_button(by=By.ID, value='loginbutton')

# Retry mechanism for network connection
def connect_to_network(retries=3):
    for attempt in range(retries):
        try:
            results = subprocess.check_output(["netsh", "wlan", "show", "network"])
            results = results.decode("ascii").replace("\r", "")
            ls = results.split("\n")
            final = [net.split(" ")[-1] for net in ls if net.strip().startswith("SSID") and "BPGC" in net]
            if len(final) == 1:
                router_name = final[0]
            else:
                print("Available networks:", final)
                choice = int(input("Network to be joined(1,2,..): "))
                router_name = final[choice - 1]

            print("The Wi-Fi you are connecting to is:", router_name)
            os.system(f'''cmd /c "netsh wlan connect name={router_name}"''')
            return True  # Successful connection
        except subprocess.CalledProcessError as e:
            print(f"Network connection failed (attempt {attempt + 1}/{retries}). Error: {e}")
            time.sleep(2)  # Wait before retrying
    return False  # Failed after retries

# Retry mechanism for browser login
def login_with_retry(browser, username, password, retries=3):
    for attempt in range(retries):
        try:
            browser.open(site)
            time.sleep(3)
            browser.login_net(username, password)
            time.sleep(1)
            browser.close_browser()
            return True  # Successful login
        except Exception as e:
            print(f"Login failed (attempt {attempt + 1}/{retries}). Error: {e}")
            time.sleep(2)  # Wait before retrying
    return False  # Failed after retries

def check_or_create_login_file():
    if not os.path.exists("Login.py"):
        print("Login.py not found. Let's create it.")
        username = input("Enter your network username: ")
        password = input("Enter your network password: ")
        fernet = Fernet(key)
        en_username = fernet.encrypt(username.encode()).decode()
        en_password = fernet.encrypt(password.encode()).decode()

        # Write the credentials to Login.py
        with open("Login.py", "w") as login_file:
            login_file.write(f'username = "{en_username}"\n')
            login_file.write(f'password = "{en_password}"\n')

        print("Login.py created successfully!")
    else:
        print("Login.py file found. Using existing credentials.")

if __name__ == '__main__':
    # Ensure Login.py exists or is created
    check_or_create_login_file()

    # Import credentials
    try:
        Login = importlib.import_module("Login")
        fernet = Fernet(key)
        dusername = fernet.decrypt(Login.username.encode()).decode()
        dpassword = fernet.decrypt(Login.password.encode()).decode()
    except ImportError:
        print("Failed to import credentials. Ensure Login.py is in the same directory.")
        exit(1)

    # Network connection logic with retry
    if not connect_to_network():
        print("Failed to connect to network after several attempts.")
        exit(1)

    # Browser logic with retry
    browser = Browser()
    if not login_with_retry(browser, dusername, dpassword):
        print("Failed to log in after several attempts.")
        exit(1)

    # Notify user of successful connection
    notification.notify(
        title="Network Connected",
        message="Successfully logged into the network",
        timeout=3
    )
