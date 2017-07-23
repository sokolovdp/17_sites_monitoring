import sys
import argparse

import requests
from whois import whois

MAX_RESPONSE_TIMEOUT = 7
HEADERS = {"USER-AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/59.0.3071.115 Safari/537.36",
           "ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "CONNECTION": "keep-alive",
           "ACCEPT_ENCODING": "gzip, deflate, br",
           "ACCEPT_LANGUAGE": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4"}


def load_urls4check(path: str) -> list:
    try:
        with open(path, mode='r') as urls_file:
            url_lines = [url.strip() for url in urls_file.readlines()]
        return url_lines
    except IOError:
        raise argparse.ArgumentTypeError("invalid file path {}".format(path))


def is_server_responding_with_ok(http_url: str) -> bool:
    try:
        return requests.get(http_url, headers=HEADERS, timeout=MAX_RESPONSE_TIMEOUT).ok
    except requests.exceptions.RequestException:
        return False


def is_url_alive(url: str) -> bool:
    return is_server_responding_with_ok("http://" + url) or is_server_responding_with_ok("https://" + url)


def get_domain_expiration_date(domain_name: str) -> str:
    expiration_date = whois(domain_name).expiration_date
    return str(expiration_date) if bool(expiration_date) else "unknown"


def main(urls_list: list):
    for url in urls_list:
        url_status = "alive" if is_url_alive(url) else "dead"
        expiry_date = get_domain_expiration_date(url)
        print("domain {} is {}, expiry date is {}".format(url, url_status, expiry_date))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="check if domain urls are alive, plus provides registry expiry date")
    parser.add_argument("--urls", dest="urls", action="store", required=True, type=load_urls4check,
                        help="  file with list of urls")
    args = parser.parse_args(sys.argv[1:])
    main(args.urls)
