# Environment Setup / 环境配置

This guide is written so a fresh machine can clone the project, install the runtime, configure Chrome, and run the script without guessing.

这份文档的目标是让一台新电脑可以按顺序完成克隆、安装、Chrome 配置和运行，尽量一次成功。

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

## Required Software / 必装软件

### English

1. Python 3.10 or newer.
2. Google Chrome installed.
3. Git.
4. Internet access for Microsoft signup, NopeCHA, Python packages, and Selenium Manager.

### 中文

1. Python 3.10 或更新版本。
2. 已安装 Google Chrome。
3. 已安装 Git。
4. 网络可以访问 Microsoft 注册页面、NopeCHA、Python 包源和 Selenium Manager。

## Python Environment / Python 环境

Always use a virtual environment. It keeps this project's packages separate from the system Python.

建议始终使用虚拟环境，避免本项目依赖污染系统 Python。

After activation, verify Python and pip:

激活虚拟环境后，检查 Python 和 pip：

```bash
python --version
pip --version
```

Install dependencies:

安装依赖：

```bash
pip install -r requirements.txt
```

The required packages are listed in `requirements.txt`: Selenium, Faker, Requests, fake-useragent, and urllib3.

依赖已写在 `requirements.txt`：Selenium、Faker、Requests、fake-useragent 和 urllib3。

## Chrome and ChromeDriver / Chrome 和 ChromeDriver

### Recommended: leave `chromedriver_path` empty

The default `config.json` leaves `chromedriver_path` empty:

```json
{
    "chromedriver_path": ""
}
```

With Selenium 4.6 or newer, Selenium Manager can locate or download the correct driver automatically. This is the easiest path when the machine has internet access.

推荐保持 `config.json` 里的 `chromedriver_path` 为空。Selenium 4.6 或更新版本自带 Selenium Manager，可以自动查找或下载匹配的驱动。有网络时这是最省事的方式。

### Manual ChromeDriver path

If Selenium Manager cannot download the driver, download a ChromeDriver that matches your Chrome major version from Chrome for Testing:

https://googlechromelabs.github.io/chrome-for-testing/

Then set an absolute path in `config.json`, for example:

```json
{
    "chromedriver_path": "C:\\tools\\chromedriver-win64\\chromedriver.exe"
}
```

如果 Selenium Manager 无法下载驱动，请从 Chrome for Testing 下载与你本机 Chrome 主版本一致的 ChromeDriver，然后在 `config.json` 写入绝对路径。

The repository also contains a Windows ChromeDriver under `drivers/chromedriver-win64/`. Use it only if it matches your installed Chrome version.

仓库里也带了一个 Windows 版 ChromeDriver，路径在 `drivers/chromedriver-win64/`。只有当它和你本机 Chrome 版本匹配时才建议使用。

## NopeCHA Setup / NopeCHA 配置

The script uses the NopeCHA Chrome extension from `ext.crx`. If the file is missing or outdated, the script tries to download a fresh copy from:

```text
https://nopecha.com/f/ext.crx
```

脚本会加载 `ext.crx` 这个 NopeCHA 浏览器扩展。如果文件不存在或需要更新，脚本会尝试从上面的地址下载。

In `config.json`:

在 `config.json` 中：

```json
{
    "api_key": "token_here"
}
```

Use `token_here` or an empty string to use the free IP-based tier. For more reliable solving, replace it with your paid NopeCHA API key.

`api_key` 保持 `token_here` 或空字符串时，会使用按 IP 判断的免费额度。想更稳定就填入付费 NopeCHA API key。

Free tier notes:

免费额度注意事项：

- Use a residential/home network.
- Avoid VPNs, proxies, VPS, and data center IPs.
- If the script says the free tier is unavailable, use a paid API key or change to a valid residential network.

## Proxy Configuration / 代理配置

`config.json` controls proxy mode:

`config.json` 里用 `mode` 控制代理：

```json
{
    "mode": 0,
    "proxy_host": "",
    "proxy_port": "",
    "username": "",
    "password": ""
}
```

Modes:

模式说明：

- `0`: no proxy.
- `1`: HTTP proxy without username and password.
- `2`: HTTP proxy with username and password.

Example without authentication:

无账号密码代理示例：

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

Example with authentication:

带账号密码代理示例：

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

The script creates diagnostic files under `diagnostics/` when browser steps fail. This folder is ignored by Git.

如果浏览器步骤失败，脚本会在 `diagnostics/` 下保存诊断文件。该目录已被 Git 忽略。

## One-Time Checklist / 一次成功检查表

Before running, confirm:

运行前确认：

- `python --version` shows Python 3.10 or newer.
- `pip install -r requirements.txt` completed without errors.
- Google Chrome is installed and can open normally.
- `chromedriver_path` is empty, or points to a real `chromedriver.exe`.
- `ext.crx` exists, or the network can download `https://nopecha.com/f/ext.crx`.
- `api_key` is set to a valid paid key, `token_here`, or an empty string.
- Proxy fields match the selected `mode`.

## Common Errors / 常见错误

### `ModuleNotFoundError`

Install dependencies inside the activated virtual environment:

在已激活的虚拟环境里重新安装依赖：

```bash
pip install -r requirements.txt
```

### ChromeDriver startup failure

If ChromeDriver fails to start:

如果 ChromeDriver 启动失败：

1. Update Google Chrome.
2. Keep `chromedriver_path` empty and let Selenium Manager try again.
3. If that still fails, download a matching ChromeDriver and set its absolute path in `config.json`.

### NopeCHA free tier unavailable

Use a residential/home network or configure a paid NopeCHA API key.

请使用家庭住宅网络，或配置付费 NopeCHA API key。

### PowerShell cannot activate `.venv`

Run PowerShell as your normal user and execute:

如果 PowerShell 无法激活虚拟环境，执行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## Notes / 备注

Use this project only where automation is allowed and follow the terms of service of the websites you access.

请只在允许自动化的场景使用本项目，并遵守目标网站的服务条款。
