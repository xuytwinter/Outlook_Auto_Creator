# Outlook Auto Creator

[English](README.md) | [中文](i18n/README.zh.md)

Python script for automating Outlook account creation.

> Use this project only where automation is allowed and follow the terms of service of the websites you access.

## Features

- Automated Outlook signup flow.
- Funcaptcha solving through the NopeCHA Chrome extension.
- Email availability check before registration.
- Random email, password, and profile data generation.
- Optional HTTP proxy support.
- Browser diagnostics when a step fails.
- NopeCHA free IP-based tier support.

## Quick Start

### Windows PowerShell

```powershell
git clone https://github.com/xuytwinter/Outlook_Auto_Creator.git
cd Outlook_Auto_Creator

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

python main.py
```

### macOS / Linux

```bash
git clone https://github.com/xuytwinter/Outlook_Auto_Creator.git
cd Outlook_Auto_Creator

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python main.py
```

## Requirements

1. Python 3.10 or newer.
2. Google Chrome installed.
3. Git installed.
4. Internet access for Python packages, Selenium Manager, Microsoft signup, and NopeCHA.

## Python Environment

Use a virtual environment so this project's packages do not affect your system Python.

Check Python and pip after activating the virtual environment:

```bash
python --version
pip --version
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies are listed in `requirements.txt`: Selenium, Faker, Requests, fake-useragent, and urllib3.

## Configuration

Edit `config.json` before running:

```json
{
    "mode": 0,
    "proxy_host": "",
    "proxy_port": "",
    "username": "",
    "password": "",
    "chromedriver_path": "",
    "api_key": "token_here"
}
```

## Chrome and ChromeDriver

### Recommended

Leave `chromedriver_path` empty:

```json
{
    "chromedriver_path": ""
}
```

With Selenium 4.6 or newer, Selenium Manager can find or download the correct ChromeDriver automatically when the machine has internet access.

### Manual ChromeDriver

If Selenium Manager cannot download the driver, download a ChromeDriver that matches your Chrome major version from Chrome for Testing:

https://googlechromelabs.github.io/chrome-for-testing/

Then set the absolute path in `config.json`:

```json
{
    "chromedriver_path": "C:\\tools\\chromedriver-win64\\chromedriver.exe"
}
```

This repository also includes a Windows ChromeDriver under `drivers/chromedriver-win64/`. Use it only if it matches your installed Chrome version.

## NopeCHA Setup

The script uses the NopeCHA Chrome extension from `ext.crx`. If the file is missing or needs to be refreshed, the script tries to download it from:

```text
https://nopecha.com/f/ext.crx
```

In `config.json`, keep `api_key` as `token_here` or an empty string to use the free IP-based tier:

```json
{
    "api_key": "token_here"
}
```

For more reliable solving, replace it with your paid NopeCHA API key.

Free tier notes:

- Use a residential or home network.
- Avoid VPNs, proxies, VPS, and data center IPs.
- If the script says the free tier is unavailable, use a paid API key or switch to a valid residential network.

## Proxy Configuration

`mode` controls proxy behavior:

- `0`: no proxy.
- `1`: HTTP proxy without username and password.
- `2`: HTTP proxy with username and password.

No proxy:

```json
{
    "mode": 0,
    "proxy_host": "",
    "proxy_port": "",
    "username": "",
    "password": "",
    "chromedriver_path": "",
    "api_key": "token_here"
}
```

Proxy without authentication:

```json
{
    "mode": 1,
    "proxy_host": "127.0.0.1",
    "proxy_port": "7890",
    "username": "",
    "password": "",
    "chromedriver_path": "",
    "api_key": "token_here"
}
```

Proxy with authentication:

```json
{
    "mode": 2,
    "proxy_host": "proxy.example.com",
    "proxy_port": "8080",
    "username": "proxy_user",
    "password": "proxy_password",
    "chromedriver_path": "",
    "api_key": "token_here"
}
```

## Run

Run from the project root:

```bash
python main.py
```

When browser steps fail, the script saves diagnostic screenshots and HTML files under `diagnostics/`. This folder is ignored by Git.

## One-Time Checklist

Before running, confirm:

- `python --version` shows Python 3.10 or newer.
- `pip install -r requirements.txt` completed without errors.
- Google Chrome is installed and can open normally.
- `chromedriver_path` is empty, or points to a real ChromeDriver file.
- `ext.crx` exists, or the network can download `https://nopecha.com/f/ext.crx`.
- `api_key` is a valid paid key, `token_here`, or an empty string.
- Proxy fields match the selected `mode`.

## Common Errors

### `ModuleNotFoundError`

Install dependencies inside the activated virtual environment:

```bash
pip install -r requirements.txt
```

### ChromeDriver Startup Failure

1. Update Google Chrome.
2. Keep `chromedriver_path` empty and let Selenium Manager try again.
3. If that still fails, download a matching ChromeDriver and set its absolute path in `config.json`.

### NopeCHA Free Tier Unavailable

Use a residential or home network, or configure a paid NopeCHA API key.

### PowerShell Cannot Activate `.venv`

Run PowerShell as your normal user and execute:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Disclaimer

This script is provided for educational and informational purposes only. The author is not responsible for any misuse or violation of terms of service resulting from the use of this script.
