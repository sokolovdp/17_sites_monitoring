import sys
import requests
import subprocess
import os


MAX_RESPONSE_TIMEOUT = 7  # max response timeout to get answer from site
user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/59.0.3071.104 Safari/537.36"}
temp_file = "temp_domain_info.txt"


def load_urls4check(path: "str file name") -> "list of urls":
    with open(path, mode='r') as f:
        lines = [name.strip() for name in f.readlines()]
    return lines


def is_server_respond_with_200(url: "str url") -> "bool":
    try:
        response = requests.get("http://"+url, headers=user_agent, timeout=MAX_RESPONSE_TIMEOUT)
        if response.ok:  # response.status_code == 200
            return True
        else:
            return False
    except requests.exceptions.Timeout:
        return False


def get_domain_expiration_date(domain_name: "str") -> "list":
    command_line = 'whois.exe -nobanner {} > {}'.format(domain_name, temp_file)
    result = subprocess.run(command_line, shell=True)
    if result.returncode == 0:   # no errors
        with open(temp_file, mode='r') as f:
            lines = [line.strip() for line in f.readlines()]
        date_line = [line for line in lines if "Registry Expiry Date:" in line]
        os.remove(temp_file)
        return date_line


def main(urls_list: "list"):
    for url in urls_list:
        if is_server_respond_with_200(url):
            print("site {} is alive,".format(url), end=" ")
        else:
            print("site {} is dead ".format(url), end=" ")
        expiry_date = get_domain_expiration_date(url)
        if expiry_date:
            print(expiry_date[0])
        else:
            print("Registry Expiry Date: NOT FOUND")

if __name__ == '__main__':
    urls = load_urls4check(sys.argv[1:][0])
    main(urls)
