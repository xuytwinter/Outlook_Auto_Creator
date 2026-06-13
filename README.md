# Outlook Auto Creator

Python script for automating Outlook account creation.

用于自动化创建 Outlook 账号的 Python 脚本。

> Use this project only where automation is allowed and follow the terms of service of the websites you access.
>
> 请只在允许自动化的场景使用本项目，并遵守目标网站的服务条款。

## Features / 功能

- Automated Outlook signup flow.
- Funcaptcha solving through the NopeCHA Chrome extension.
- Email availability check before registration.
- Random email, password, and profile data generation.
- Optional HTTP proxy support.
- Browser diagnostics when a step fails.
- NopeCHA free IP-based tier support.

- 自动化 Outlook 注册流程。
- 通过 NopeCHA Chrome 扩展处理 Funcaptcha。
- 注册前检查邮箱是否可用。
- 随机生成邮箱、密码和个人资料。
- 支持可选 HTTP 代理。
- 失败时保存浏览器诊断文件。
- 支持 NopeCHA 按 IP 判断的免费额度。

## Quick Start / 快速开始

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

## Requirements / 环境要求

### English

1. Python 3.10 or newer.
2. Google Chrome installed.
3. Git installed.
4. Internet access for Python packages, Selenium Manager, Microsoft signup, and NopeCHA.

### 中文

1. Python 3.10 或更新版本。
2. 已安装 Google Chrome。
3. 已安装 Git。
4. 网络可以访问 Python 包源、Selenium Manager、Microsoft 注册页面和 NopeCHA。

## Python Environment / Python 环境

Use a virtual environment so this project's packages do not affect your system Python.

建议使用虚拟环境，避免本项目依赖影响系统 Python。

Check Python and pip after activating the virtual environment:

激活虚拟环境后检查 Python 和 pip：

```bash
python --version
pip --version
```

Install dependencies:

安装依赖：

```bash
pip install -r requirements.txt
```

Dependencies are listed in `requirements.txt`: Selenium, Faker, Requests, fake-useragent, and urllib3.

依赖已写在 `requirements.txt`：Selenium、Faker、Requests、fake-useragent 和 urllib3。

## Configuration / 配置

Edit `config.json` before running:

运行前编辑 `config.json`：

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

## Chrome and ChromeDriver / Chrome 和 ChromeDriver

### Recommended / 推荐方式

Leave `chromedriver_path` empty:

保持 `chromedriver_path` 为空：

```json
{
    "chromedriver_path": ""
}
```

With Selenium 4.6 or newer, Selenium Manager can find or download the correct ChromeDriver automatically when the machine has internet access.

Selenium 4.6 或更新版本自带 Selenium Manager。在电脑可以联网时，它可以自动查找或下载匹配的 ChromeDriver。

### Manual ChromeDriver / 手动指定 ChromeDriver

If Selenium Manager cannot download the driver, download a ChromeDriver that matches your Chrome major version from Chrome for Testing:

如果 Selenium Manager 无法下载驱动，请从 Chrome for Testing 下载与你本机 Chrome 主版本一致的 ChromeDriver：

https://googlechromelabs.github.io/chrome-for-testing/

Then set the absolute path in `config.json`:

然后在 `config.json` 中写入绝对路径：

```json
{
    "chromedriver_path": "C:\\tools\\chromedriver-win64\\chromedriver.exe"
}
```

This repository also includes a Windows ChromeDriver under `drivers/chromedriver-win64/`. Use it only if it matches your installed Chrome version.

仓库中也包含一个 Windows 版 ChromeDriver，位于 `drivers/chromedriver-win64/`。只有当它和本机 Chrome 版本匹配时才建议使用。

## NopeCHA Setup / NopeCHA 配置

The script uses the NopeCHA Chrome extension from `ext.crx`. If the file is missing or needs to be refreshed, the script tries to download it from:

脚本会加载 `ext.crx` 这个 NopeCHA Chrome 扩展。如果文件不存在或需要更新，脚本会尝试从这里下载：

```text
https://nopecha.com/f/ext.crx
```

In `config.json`, keep `api_key` as `token_here` or an empty string to use the free IP-based tier:

在 `config.json` 中，`api_key` 保持 `token_here` 或空字符串时，会使用按 IP 判断的免费额度：

```json
{
    "api_key": "token_here"
}
```

For more reliable solving, replace it with your paid NopeCHA API key.

如果需要更稳定的识别效果，请替换为你的付费 NopeCHA API key。

Free tier notes / 免费额度注意事项：

- Use a residential or home network.
- Avoid VPNs, proxies, VPS, and data center IPs.
- If the script says the free tier is unavailable, use a paid API key or switch to a valid residential network.

- 请使用家庭住宅网络。
- 避免使用 VPN、代理、VPS 或数据中心 IP。
- 如果脚本提示免费额度不可用，请使用付费 API key，或切换到有效的住宅网络。

## Proxy Configuration / 代理配置

`mode` controls proxy behavior:

`mode` 控制代理模式：

- `0`: no proxy / 不使用代理。
- `1`: HTTP proxy without username and password / HTTP 代理，无账号密码。
- `2`: HTTP proxy with username and password / HTTP 代理，带账号密码。

No proxy / 不使用代理：

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

Proxy without authentication / 无账号密码代理：

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

Proxy with authentication / 带账号密码代理：

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

## Run / 运行

Run from the project root:

在项目根目录运行：

```bash
python main.py
```

When browser steps fail, the script saves diagnostic screenshots and HTML files under `diagnostics/`. This folder is ignored by Git.

如果浏览器步骤失败，脚本会在 `diagnostics/` 下保存截图和 HTML 诊断文件。该目录已被 Git 忽略。

## One-Time Checklist / 一次成功检查表

Before running, confirm:

运行前确认：

- `python --version` shows Python 3.10 or newer.
- `pip install -r requirements.txt` completed without errors.
- Google Chrome is installed and can open normally.
- `chromedriver_path` is empty, or points to a real ChromeDriver file.
- `ext.crx` exists, or the network can download `https://nopecha.com/f/ext.crx`.
- `api_key` is a valid paid key, `token_here`, or an empty string.
- Proxy fields match the selected `mode`.

## Common Errors / 常见错误

### `ModuleNotFoundError`

Install dependencies inside the activated virtual environment:

在已激活的虚拟环境中重新安装依赖：

```bash
pip install -r requirements.txt
```

### ChromeDriver startup failure / ChromeDriver 启动失败

1. Update Google Chrome.
2. Keep `chromedriver_path` empty and let Selenium Manager try again.
3. If that still fails, download a matching ChromeDriver and set its absolute path in `config.json`.

1. 更新 Google Chrome。
2. 保持 `chromedriver_path` 为空，让 Selenium Manager 再试一次。
3. 如果仍然失败，下载匹配版本的 ChromeDriver，并在 `config.json` 中写入绝对路径。

### NopeCHA free tier unavailable / NopeCHA 免费额度不可用

Use a residential or home network, or configure a paid NopeCHA API key.

请使用家庭住宅网络，或配置付费 NopeCHA API key。

### PowerShell cannot activate `.venv` / PowerShell 无法激活 `.venv`

Run PowerShell as your normal user and execute:

用普通用户打开 PowerShell 后执行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## License / 许可证

[MIT](https://choosealicense.com/licenses/mit/)

## Disclaimer / 免责声明

This script is provided for educational and informational purposes only. The author is not responsible for any misuse or violation of terms of service resulting from the use of this script.

本脚本仅用于教育和信息参考。因使用本脚本导致的任何滥用行为或违反服务条款的行为，作者不承担责任。
