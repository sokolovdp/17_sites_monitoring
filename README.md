# Sites Monitoring Utility

**check_sites_health.py** takes domain names from input file and 
checks if the site is responding plus provide Domain Registry Expiry Date.
To run program you need utility **whois.exe** to be installed in your system,
you can download it from [MS TechNet](https://technet.microsoft.com/ru-ru/sysinternals/whois.aspx)


# Sample usage and output
*python check_sites_health.py sites_url.txt*
```
site sokolovdp.info is alive, Registry Expiry Date: 2018-03-21T17:14:03Z
site sokolovdp.github.io is alive, Registry Expiry Date: NOT FOUND
```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
