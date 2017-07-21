import sys
import requests
import subprocess
import os


MAX_RESPONSE_TIMEOUT = 7
HEADERS = {"USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/59.0.3071.115 Safari/537.36",
           "ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "CONNECTION": "keep-alive",
           "ACCEPT_ENCODING": "gzip, deflate, br",
           "ACCEPT_LANGUAGE": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4"}
TEMPORARY_FILE = "temp_domain_info.txt"


def load_urls4check(path: str) -> list:
    with open(path, mode='r') as urls_file:
        url_lines = [url.strip() for url in urls_file.readlines()]
    return url_lines


def is_server_responding_with_ok(url: str) ->bool:
    try:
        response = requests.get("http://"+url, headers=HEADERS, timeout=MAX_RESPONSE_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return False
    else:
        return True


def get_domain_expiration_date(domain_name: str) -> list:
    shell_command_line = 'whois.exe -nobanner {} > {}'.format(domain_name, TEMPORARY_FILE)
    run_result = subprocess.run(shell_command_line, shell=True)
    if run_result.returncode == 0:
        with open(TEMPORARY_FILE, mode='r') as temp_file:
            lines = [line.strip() for line in temp_file.readlines()]
        date_line = [line for line in lines if "Registry Expiry Date:" in line]
        os.remove(TEMPORARY_FILE)
        return date_line


def main(urls_list: list):
    for url in urls_list:
        if is_server_responding_with_ok(url):
            print("domain {} is alive,".format(url), end=" ")
        else:
            print("domain {} is not active ".format(url), end=" ")
        expiry_date = get_domain_expiration_date(url)
        if expiry_date:
            print(expiry_date[0])
        else:
            print("Registry Expiry Date: NOT FOUND")

if __name__ == '__main__':
    if not os.path.exists(sys.argv[1]):
        print("invalid file path {}".format(sys.argv[1]))
    else:
        main(load_urls4check(sys.argv[1]))
