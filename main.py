import os
import shutil
import zipfile
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchDriverException, TimeoutException, WebDriverException
import time
import json
from fake_data import generate_fake_data
from check_email import check_email
import requests
import random
import fake_useragent

NOPECHA_EXTENSION_URL = "https://nopecha.com/f/ext.crx"
NOPECHA_EXTENSION_PATH = "ext.crx"
DIAGNOSTICS_DIR = "diagnostics"


def normalize_api_key(raw_key):
    """Normalize API key: convert empty string, 'token_here', or None to None."""
    if not raw_key:
        return None
    key = str(raw_key).strip()
    if key == '' or key.lower() == 'token_here':
        return None
    return key


def get_nopecha_status(api_key):
    """Get NopeCHA API status."""
    url = "https://api.nopecha.com/v1/status"
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        if api_key:
            response = requests.get(url, params={"key": api_key}, timeout=10, verify=False)
        else:
            response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to NopeCHA API: {e}")
        return None


def validate_nopecha_status(status):
    """Validate NopeCHA status and return (is_valid, message)."""
    if status is None:
        return False, "Unable to connect to NopeCHA API. Please check your network connection."
    
    status_code = status.get('status', '')
    credit = status.get('credit', 0)
    plan = status.get('plan', '')
    
    if status_code == 'Active' and credit > 0:
        return True, f"Plan: {plan}, Credits: {credit}"
    
    if status_code == 'Expired' or credit == 0:
        return False, "Out of credit. Please wait for credit reset or use a paid API key."
    
    if 'Free Tier Ineligible' in str(status.get('message', '')) or status_code == 'Banned IP':
        return False, "Free tier not available for this IP. Please use a residential/home network or configure a paid API key."
    
    if 'Invalid API key' in str(status.get('message', '')):
        return False, "Invalid API key. Please check your API key and try again."
    
    return False, f"NopeCHA status check failed: {status.get('message', 'Unknown error')}"


def load_config():
    """Load and validate configuration from config.json."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found")
        return None
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON")
        return None
    
    proxy_host = config.get('proxy_host', '').strip()
    proxy_port = config.get('proxy_port', '').strip()
    username = config.get('username', '').strip()
    password = config.get('password', '').strip()
    chromedriver_path = config.get('chromedriver_path', '').strip()
    api_key = normalize_api_key(config.get('api_key'))
    mode = config.get('mode', 0)
    
    return {
        'proxy_host': proxy_host,
        'proxy_port': proxy_port,
        'username': username,
        'password': password,
        'chromedriver_path': chromedriver_path,
        'api_key': api_key,
        'mode': mode
    }


def ensure_nopecha_extension(path=NOPECHA_EXTENSION_PATH):
    """Download the NopeCHA extension without destroying an existing copy."""
    tmp_path = f"{path}.tmp"

    try:
        response = requests.get(NOPECHA_EXTENSION_URL, timeout=30)
        response.raise_for_status()

        if not response.content:
            raise RuntimeError("downloaded extension is empty")

        with open(tmp_path, 'wb') as f:
            f.write(response.content)

        if os.path.getsize(tmp_path) == 0:
            raise RuntimeError("downloaded extension file is empty")

        os.replace(tmp_path, path)
        print("NopeCHA extension downloaded.")
        return path
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

        if os.path.exists(path) and os.path.getsize(path) > 0:
            print(f"Warning: failed to download latest NopeCHA extension: {e}")
            print(f"Using existing {path} instead.")
            return path

        raise RuntimeError(
            "Failed to download NopeCHA extension and no valid local ext.crx exists. "
            "Download https://nopecha.com/f/ext.crx manually and save it as ext.crx."
        ) from e


def resolve_chromedriver_path(configured_path):
    """Return a usable ChromeDriver path or None when Selenium Manager is required."""
    if configured_path:
        if not os.path.isfile(configured_path):
            raise RuntimeError(f"Configured chromedriver_path does not exist: {configured_path}")
        return configured_path

    return shutil.which("chromedriver")


def save_browser_diagnostics(driver, label):
    """Save URL/title/screenshot/page source for debugging browser state."""
    os.makedirs(DIAGNOSTICS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = os.path.join(DIAGNOSTICS_DIR, f"{timestamp}_{label}")

    print(f"[diagnostic] URL: {driver.current_url}")
    print(f"[diagnostic] Title: {driver.title}")

    screenshot_path = f"{base_path}.png"
    html_path = f"{base_path}.html"

    try:
        driver.save_screenshot(screenshot_path)
        print(f"[diagnostic] Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"[diagnostic] Failed to save screenshot: {e}")

    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"[diagnostic] HTML saved: {html_path}")
    except Exception as e:
        print(f"[diagnostic] Failed to save HTML: {e}")


def create_proxy_extension_v3(proxy_host, proxy_port, username=None, password=None):
    """Install plugin on the fly for proxy authentication"""
    manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 3,
    "name": "kanwas",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "webRequest",
        "webRequestAuthProvider"
    ],
    "host_permissions": [
        "<all_urls>"
    ],
    "background": {
        "service_worker": "background.js"
    },
    "minimum_chrome_version": "108"
}
"""
    background_js = """
var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: %s
        },
        bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
""" % (proxy_host, proxy_port)

    if username and password:
        background_js += """
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    { urls: ["<all_urls>"] },
    ['blocking']
);
""" % (username, password)

    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return pluginfile


class AccGen:
    def __init__(self, config):
        self.driver = None
        self.config = config
        self.proxy_host = config['proxy_host']
        self.proxy_port = config['proxy_port']
        self.username = config['username']
        self.password = config['password']
        self.chromedriver_path = config['chromedriver_path']
        self.api_key = config['api_key']

    def open_signup_page(self):
        chrome_options = Options()
        chrome_options.add_argument("--lang=en")
        chrome_options.add_argument("--headless=new")

        extension_path = ensure_nopecha_extension()
        
        if not self.driver:
            mode = self.config['mode']
    
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-extensions-except=" + extension_path)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            
            user_agent = fake_useragent.UserAgent().random
            chrome_options.add_argument(f'user-agent={user_agent}')
            
            chrome_options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            })
    
            if mode == 0:
                print("Not using proxy")
            elif mode == 1:
                print("Using proxy without authentication")
                proxy_auth_plugin_path = create_proxy_extension_v3(
                    self.proxy_host,
                    self.proxy_port
                )
                chrome_options.add_extension(proxy_auth_plugin_path)
            elif mode == 2:
                print("Using proxy with authentication")
                proxy_auth_plugin_path = create_proxy_extension_v3(
                    self.proxy_host,
                    self.proxy_port,
                    self.username,
                    self.password,
                )
                chrome_options.add_extension(proxy_auth_plugin_path)
    
            chrome_options.add_extension(extension_path)

            try:
                chromedriver_path = resolve_chromedriver_path(self.chromedriver_path)
                if chromedriver_path:
                    service = Service(executable_path=chromedriver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                else:
                    self.driver = webdriver.Chrome(options=chrome_options)
            except (NoSuchDriverException, WebDriverException) as e:
                raise RuntimeError(
                    "Unable to start Chrome WebDriver. Install a ChromeDriver that matches "
                    "your Chrome version and either add it to PATH or set chromedriver_path "
                    "in config.json."
                ) from e

            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            self.driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'Win32'})")
            self.driver.execute_script("Object.defineProperty(navigator, 'deviceMemory', {get: () => 8})")
            
            if self.api_key:
                self.driver.get(f"https://nopecha.com/setup#{self.api_key}")
                print("Using NopeCHA API key")
            else:
                self.driver.get("https://nopecha.com/setup")
                print("Using NopeCHA Free IP-based tier")
            
            time.sleep(2)
            self.driver.get('https://www.google.com')
            time.sleep(2)
            self.driver.get('https://signup.live.com/signup')
            time.sleep(3)
            self.handle_privacy_consent()
            save_browser_diagnostics(self.driver, "signup_loaded")

    def handle_privacy_consent(self):
        try:
            consent_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "同意并继续") or contains(text(), "Continue") or contains(text(), "同意")]'))
            )
            consent_button.click()
            print("Clicked consent button")
            time.sleep(2)
        except TimeoutException:
            print("No consent page found or already handled")

    def fill_signup_form(self):
        login, password, first_name, last_name, birth_date = generate_fake_data()
        email = login + "@outlook.com"
        print(f"Using email: {email}")

        print("Waiting for email input field...")
        for attempt in range(3):
            try:
                email_input = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "floatingLabelInput4"))
                )
                print("Found email input field")
                email_input.click()
                email_input.clear()
                email_input.send_keys(email)
                print("Email entered")
                time.sleep(1)
                break
            except TimeoutException:
                print(f"Attempt {attempt + 1}/3 failed to find email input. Retrying...")
                save_browser_diagnostics(self.driver, f"email_timeout_attempt_{attempt}")
                self.driver.refresh()
                time.sleep(3)
        else:
            raise TimeoutException("Failed to find email input after 3 attempts")
        
        print("Waiting for Next button...")
        next_button = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="primaryButton"]'))
        )
        print("Found Next button, clicking...")
        next_button.click()
        print("Clicked Next button")
        time.sleep(3)
        
        save_browser_diagnostics(self.driver, "after_next_click")

        print(f"Generated password: {password}")
        print("Waiting for password input field...")
        try:
            password_input = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable((By.ID, "floatingLabelInput13"))
            )
            password_input.click()
            password_input.clear()
            password_input.send_keys(password)
            print("Password entered")
            time.sleep(2)
        except TimeoutException:
            print("Password field not found. Checking for other page states...")
            save_browser_diagnostics(self.driver, "password_timeout")
            raise

        print("Waiting for Next button after password...")
        next_button_after_password = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="primaryButton"]'))
        )
        next_button_after_password.click()
        print("Clicked Next button after password")
        
        print("Waiting for page transition to name form...")
        for attempt in range(10):
            try:
                first_name_input = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "floatingLabelInput5"))
                )
                print("Found first name input field")
                break
            except TimeoutException:
                print(f"Waiting for name page... attempt {attempt + 1}/10")
                save_browser_diagnostics(self.driver, f"waiting_for_name_page_{attempt}")
                time.sleep(1)
        else:
            print("Failed to navigate to name page")
            save_browser_diagnostics(self.driver, "name_page_timeout")
            raise TimeoutException("Failed to navigate to name page")
        first_name_input.send_keys(first_name)

        print("Waiting for last name input field...")
        last_name_input = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "floatingLabelInput6"))
        )
        last_name_input.send_keys(last_name)

        next_button_after_name = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="primaryButton"]'))
        )
        next_button_after_name.click()
        time.sleep(2)

        print("Waiting for birth month select...")
        birth_month_select = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "floatingLabelInput7"))
        )
        Select(birth_month_select).select_by_value(str(birth_date.month))

        print("Waiting for birth day select...")
        birth_day_select = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "floatingLabelInput8"))
        )
        Select(birth_day_select).select_by_value(str(birth_date.day))

        print("Waiting for birth year input...")
        birth_year_input = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "floatingLabelInput9"))
        )
        birth_year_input.send_keys(str(birth_date.year))

        next_button_after_birth_date = WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="primaryButton"]'))
        )
        next_button_after_birth_date.click()

        try:
            phone_number_label = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "Phone number")]'))
            )
            print("SMS verification required. Please change your proxy.")
            self.driver.quit()
            return
        except:
            pass

        print('Trying to solve captcha ...')
        time.sleep(60)

        ok_button = WebDriverWait(self.driver, 300).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="primaryButton"]'))
        )

        print("Captcha solved! Account successfully generated.")

        with open('generated.txt', 'a') as f:
            if os.path.exists('generated.txt') and os.path.getsize('generated.txt') > 0:
                f.write("\n")
            f.write(f"Email: {email}\n")
            f.write(f"Password: {password}\n")
        print("Email and password saved to generated.txt")

    def create_account(self):
        while True:
            try:
                self.open_signup_page()
                self.fill_signup_form()
                break
            except TimeoutException:
                print("Timeout occurred. Restarting the account creation process ...")
                self.driver.get('https://signup.live.com/signup')


if __name__ == '__main__':
    config = load_config()
    if not config:
        exit(1)
    
    print("Checking NopeCHA status...")
    status = get_nopecha_status(config['api_key'])
    is_valid, message = validate_nopecha_status(status)
    
    if not is_valid:
        print(f"NopeCHA check failed: {message}")
        print("\nPossible solutions:")
        print("- Use a residential/home network (not VPN/proxy/VPS)")
        print("- Wait for free tier credits to refresh (every 23 hours)")
        print("- Configure a paid NopeCHA API key in config.json")
        print("Continuing without NopeCHA status verification...")
    
    if is_valid:
        print(f"NopeCHA status: {message}")
    
    print("Starting account creation...\n")
    
    try:
        acc_gen = AccGen(config)
        acc_gen.create_account()
    except RuntimeError as e:
        print(f"Error: {e}")
        exit(1)
