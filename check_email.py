import requests
from urllib.parse import urlparse, parse_qs, urlunparse
import re
import codecs
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_email(email):
    url = "https://signup.live.com/signup"

    with requests.Session() as s:
        s.verify = False
        
        response = s.get(url, allow_redirects=False)

        if response.status_code == 302:
            redirect_url = response.headers['Location']
            parsed_url = urlparse(redirect_url)
            uaid = parse_qs(parsed_url.query).get('uaid', [''])[0]
            first_canary = f"https://signup.live.com/signup?lic=1&uaid={uaid}"
            second_response = s.get(first_canary)

            match = re.search(r'"apiCanary":"(.*?)"', second_response.text)
            if match:
                api_canary_encoded = match.group(1)
                api_canary = codecs.decode(api_canary_encoded, 'unicode_escape')
            else:
                print("Could not find 'apiCanary' in the response")
                return {'isAvailable': True}

            try:
                amsc = second_response.cookies.get('amsc')

                headers = {
                    'cookie': f'amsc={amsc}',
                    'canary': api_canary,
                    'authority': 'signup.live.com',
                    'accept': 'application/json',
                    'content-type': 'application/json; charset=utf-8',
                    'origin': 'https://signup.live.com',
                } if amsc else {
                    'canary': api_canary,
                    'authority': 'signup.live.com',
                    'accept': 'application/json',
                    'content-type': 'application/json; charset=utf-8',
                    'origin': 'https://signup.live.com',
                }

            except Exception as e:
                print("Error:", e)
                return {'isAvailable': True}

            data = {
                "evts": [
                    {
                        "perf": {
                            "data": {
                                "navigation": {
                                    "type": 0,
                                    "redirectCount": 0
                                },
                            },
                        }
                    }
                ],
                "cm": {
                    "hst": "signup.live.com",
                    "av": None
                },
            }

            data_string = json.dumps(data)
            ClientEvents = s.post("https://signup.live.com/API/ClientEvents", headers=headers, data=data_string)

            json_data = {
                'pageApiId': 200639,
                'clientDetails': [],
                'userAction': '',
                'source': 'PageView',
                'clientTelemetryData': {
                    'category': 'PageLoad',
                    'pageName': '200639',
                    'eventInfo': {
                        'timestamp': 1712713102844,
                    },
                },
                'uiflvr': 1001,
            }

            data_string = json.dumps(json_data)
            ReportClientEvent = s.post("https://signup.live.com/API/ReportClientEvent", headers=headers, data=data_string)

            json_data = {
                'signInName': email,
            }

            data_string = json.dumps(json_data)
            CheckAvailableSigninNames = s.post("https://signup.live.com/API/CheckAvailableSigninNames", headers=headers, data=data_string)

            response_dict = json.loads(CheckAvailableSigninNames.text)
            return response_dict
        
        return {'isAvailable': True}