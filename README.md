# Sites Monitoring Utility

**check_sites_health.py** takes domain names from input file and 
checks if the site is responding plus provide Domain Registry Expiry Date.
To run program you need module **python-whois>=0.6.5** to be installed in your system,
you can download it from [PyPi](https://pypi.python.org/pypi/python-whois/0.6.5)


# Sample usage and output
*python check_sites_health.py  --urls=sites_url.txt*
```
site sokolovdp.info is alive, expiry date is 2018-03-21 17:14:03 
site sokolovdp.github.io is alive, expiry date is unknown
```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
