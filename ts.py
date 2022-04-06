# xss scanner
import requests
import re
import sys
import argparse
import time
import os
import urllib3

def main() {
    parser = argparse.ArgumentParser(description='XSS Scanner')
    parser.add_argument('-u', '--url', help='URL to scan', required=True)
    parser.add_argument('-f', '--file', help='File containing payloads', required=True)
    parser.add_argument('-o', '--output', help='Output file', required=True)
    args = parser.parse_args()

    url = args.url
    file = args.file
    output = args.output

    if not url.startswith('http'):
        url = 'http://' + url

    if not url.endswith('/'):
        url = url + '/'

    if not os.path.exists(file):
        print('File does not exist')
        sys.exit(1)

    if os.path.exists(output):
        print('Output file already exists')
        sys.exit(1)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    with open(file, 'r') as f:
        payloads = f.readlines()

    with open(output, 'w') as f:
        for payload in payloads:
            payload = payload.strip()
            print('Testing payload: ' + payload)
            try:
                r = requests.get(url + payload, verify=False)
                if r.status_code == 200:
                    print('Found XSS: ' + payload)
                    f.write(payload + '\n')
            except:
                pass
            time.sleep(1)
}
