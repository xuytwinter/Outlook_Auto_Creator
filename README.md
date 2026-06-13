# Outlook account creator

Python script that automatically create Outlook account


## Features

- Automated Account Creation
- Auto captcha solve (funcaptcha)
- Checking if email is already taken before creating account
- Randomly generated email and password
- HTTP proxy support
- Error Handling
- **NopeCHA Free Tier Support**: No API key required for basic usage


## Installation

1. Clone outlook-account-creator repository from github:

```bash
  git clone https://github.com/xuytwinter/Outlook_Auto_Creator.git
```

2. Move to project directory: 

```bash
  cd Outlook_Auto_Creator
```

3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Open config.json file. It should be looking like that:

``` json
{
    "mode": 0,
    "proxy_host": "",
    "proxy_port": "",
    "username": "",
    "password": "",
    "chromedriver_path": "",
    "api_key": ""
}
```

2. **API Key Configuration**: The `api_key` field is optional:
   - Leave it empty or set to `"token_here"` to use NopeCHA's free IP-based tier (100 free solves/day)
   - Fill in your NopeCHA API key to use a paid subscription
3. **ChromeDriver Configuration**: The `chromedriver_path` field is optional:
   - Leave it empty to let Selenium Manager find or download ChromeDriver automatically
   - If Selenium Manager cannot access the internet, set it to the full path of a ChromeDriver matching your Chrome version, for example `C:\\tools\\chromedriver.exe`

**Note** - For the free tier, ensure you're using a residential/home network. VPNs, proxies, VPS, or data center IPs are not eligible for the free tier.


## Run the script

```bash
py main.py
```


### (Optional) proxy configuration

Default mode is `0` which means you won't use any proxy. If you want to use HTTP proxy with that tool you have to set it in the config file. Additionally, you have to change mode value to one of the following:

- `0` value - no proxy
- `1` value - proxy without auth
- `2` value - proxy with login and password auth

### Manual NopeCHA Status Check

To check if your IP is eligible for the free tier, run this command:

```powershell
Invoke-RestMethod "https://api.nopecha.com/v1/status"
```

Or using curl:
```bash
curl "https://api.nopecha.com/v1/status"
```

## Worth mention

- This script is dedicated for chrome browser
- Make sure you have added chromedriver to your path or set `chromedriver_path` in `config.json` to avoid issues
- The script will automatically check NopeCHA status before starting
- If the free tier is unavailable, you'll see a clear error message with possible solutions


## Tips

- If you noticed script detects SMS verification you should change your ip with proxy or wait some time.
- Nopecha sometimes is not able to do captcha correctly, especially while number of images to be processed is above norm (up to 5) you should consider changing your proxy or take a break then. If you want to check what's going on disable headless mode in `main.py` file.
- Free tier credits reset every 23 hours
- Common reasons for free tier ineligibility: VPN, proxy, VPS, data center IP


## Contributing

Contributions are always welcome! If you have ideas for new features or you have any troubles feel free to opening issues or create pull requests.

## License

[MIT](https://choosealicense.com/licenses/mit/)


# Disclaimer

This script is provided for educational and informational purposes only. It was created just for fun. The author is not responsible for any misuse or violation of terms of service resulting from the use of this script. Always stick to terms of service of website you're using.
