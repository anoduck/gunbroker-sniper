#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time
import requests
import shutil
import hashlib
import urllib.parse
from furl import furl
from retrying import retry
# import pytest
from random import randint
# import argparse
import os
# import wget
# import platform
import sys
import cfscrape

# =======================================================
# Variables
# =======================================================

# Scrolling window
# -----------------
current_scrolls = 0
old_height = 0
total_scrolls = 2500
scroll_time = 20

total_scrolls = int(total_scrolls)
scroll_time = int(scroll_time)

# Item Url
item_pattern = "https://www.gunbroker.com/item/"

#login url
login_url = "https://www.gunbroker.com/user/login"

# ------------------------------------------------------
# Setup Browser
cm_path = "~/bin/cm"
down_dir = str(os.getcwd())

use_selenoid = True
if use_selenoid:
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        desired_capabilities={
            "browserName": "firefox",
            "browserVersion": "95.0",
            "browserSize": "1920x1080",
            "enableVNC": True,
            "enableVideo": False
        }
    )
else:
    driver = webdriver.Firefox(
        # executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        executable_path="/home/vassilios/bin/geckodriver")

opts = Options()
opts.add_argument(
    '--user-agent=Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'  # noqa: E501
)
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--lang=en-US")
opts.add_argument("--dns-prefetch-disable")
opts.set_capability("javascript.enabled", True)
# prefs.set_capability("browser.download.folderList", 2)
opts.set_capability("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
opts.set_capability("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

# For requests library
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}  # noqa: E501

wait = WebDriverWait(driver, 67)
driver.implicitly_wait(35)


def retry_on_timeout(exception):
    """ Return True if exception is Timeout """
    return isinstance(exception, TimeoutException)


def retry_on_NoSuchElement(exception):
    """ Return True if exception is NoSuchElement """
    return isinstance(exception, NoSuchElementException)


# @retry(retry_on_exception=retry_on_timeout, stop_max_attempt_number=7)
# @retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
