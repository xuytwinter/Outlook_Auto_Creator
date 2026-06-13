# Outlook Auto Creator

[English](../README.md) | [中文](README.zh.md)

用于自动化创建 Outlook 账号的 Python 脚本。

> 请只在允许自动化的场景使用本项目，并遵守目标网站的服务条款。

## 功能

- 自动化 Outlook 注册流程。
- 通过 NopeCHA Chrome 扩展处理 Funcaptcha。
- 注册前检查邮箱是否可用。
- 随机生成邮箱、密码和个人资料。
- 支持可选 HTTP 代理。
- 失败时保存浏览器诊断文件。
- 支持 NopeCHA 按 IP 判断的免费额度。

## 快速开始

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

## 环境要求

1. Python 3.10 或更新版本。
2. 已安装 Google Chrome。
3. 已安装 Git。
4. 网络可以访问 Python 包源、Selenium Manager、Microsoft 注册页面和 NopeCHA。

## Python 环境

建议使用虚拟环境，避免本项目依赖影响系统 Python。

激活虚拟环境后检查 Python 和 pip：

```bash
python --version
pip --version
```

安装依赖：

```bash
pip install -r requirements.txt
```

依赖已写在 `requirements.txt`：Selenium、Faker、Requests、fake-useragent 和 urllib3。

## 配置

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

## Chrome 和 ChromeDriver

### 推荐方式

保持 `chromedriver_path` 为空：

```json
{
    "chromedriver_path": ""
}
```

Selenium 4.6 或更新版本自带 Selenium Manager。在电脑可以联网时，它可以自动查找或下载匹配的 ChromeDriver。

### 手动指定 ChromeDriver

如果 Selenium Manager 无法下载驱动，请从 Chrome for Testing 下载与你本机 Chrome 主版本一致的 ChromeDriver：

https://googlechromelabs.github.io/chrome-for-testing/

然后在 `config.json` 中写入绝对路径：

```json
{
    "chromedriver_path": "C:\\tools\\chromedriver-win64\\chromedriver.exe"
}
```

仓库中也包含一个 Windows 版 ChromeDriver，位于 `drivers/chromedriver-win64/`。只有当它和本机 Chrome 版本匹配时才建议使用。

## NopeCHA 配置

脚本会加载 `ext.crx` 这个 NopeCHA Chrome 扩展。如果文件不存在或需要更新，脚本会尝试从这里下载：

```text
https://nopecha.com/f/ext.crx
```

在 `config.json` 中，`api_key` 保持 `token_here` 或空字符串时，会使用按 IP 判断的免费额度：

```json
{
    "api_key": "token_here"
}
```

如果需要更稳定的识别效果，请替换为你的付费 NopeCHA API key。

免费额度注意事项：

- 请使用家庭住宅网络。
- 避免使用 VPN、代理、VPS 或数据中心 IP。
- 如果脚本提示免费额度不可用，请使用付费 API key，或切换到有效的住宅网络。

## 代理配置

`mode` 控制代理模式：

- `0`：不使用代理。
- `1`：HTTP 代理，无账号密码。
- `2`：HTTP 代理，带账号密码。

不使用代理：

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

无账号密码代理：

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

带账号密码代理：

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

## 运行

在项目根目录运行：

```bash
python main.py
```

如果浏览器步骤失败，脚本会在 `diagnostics/` 下保存截图和 HTML 诊断文件。该目录已被 Git 忽略。

## 一次成功检查表

运行前确认：

- `python --version` 显示 Python 3.10 或更新版本。
- `pip install -r requirements.txt` 已成功完成。
- Google Chrome 已安装并可以正常打开。
- `chromedriver_path` 为空，或指向真实存在的 ChromeDriver 文件。
- `ext.crx` 存在，或网络可以下载 `https://nopecha.com/f/ext.crx`。
- `api_key` 是有效付费 key、`token_here` 或空字符串。
- 代理字段和选择的 `mode` 匹配。

## 常见错误

### `ModuleNotFoundError`

在已激活的虚拟环境中重新安装依赖：

```bash
pip install -r requirements.txt
```

### ChromeDriver 启动失败

1. 更新 Google Chrome。
2. 保持 `chromedriver_path` 为空，让 Selenium Manager 再试一次。
3. 如果仍然失败，下载匹配版本的 ChromeDriver，并在 `config.json` 中写入绝对路径。

### NopeCHA 免费额度不可用

请使用家庭住宅网络，或配置付费 NopeCHA API key。

### PowerShell 无法激活 `.venv`

用普通用户打开 PowerShell 后执行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## 许可证

[MIT](https://choosealicense.com/licenses/mit/)

## 免责声明

本脚本仅用于教育和信息参考。因使用本脚本导致的任何滥用行为或违反服务条款的行为，作者不承担责任。
