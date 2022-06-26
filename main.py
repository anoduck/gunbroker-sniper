#!/usr/bin/env python

# =======================================================================================================================================
#   /$$$$$$                      /$$$$$$$                      /$$
#  /$$__  $$                    | $$__  $$                    | $$
# | $$  \__/ /$$   /$$ /$$$$$$$ | $$  \ $$  /$$$$$$   /$$$$$$ | $$   /$$  /$$$$$$   /$$$$$$
# | $$ /$$$$| $$  | $$| $$__  $$| $$$$$$$  /$$__  $$ /$$__  $$| $$  /$$/ /$$__  $$ /$$__  $$
# | $$|_  $$| $$  | $$| $$  \ $$| $$__  $$| $$  \__/| $$  \ $$| $$$$$$/ | $$$$$$$$| $$  \__/
# | $$  \ $$| $$  | $$| $$  | $$| $$  \ $$| $$      | $$  | $$| $$_  $$ | $$_____/| $$
# |  $$$$$$/|  $$$$$$/| $$  | $$| $$$$$$$/| $$      |  $$$$$$/| $$ \  $$|  $$$$$$$| $$
#  \______/  \______/ |__/  |__/|_______/ |__/       \______/ |__/  \__/ \_______/|__/

# ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗
# ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
# ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
# ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
# ███████║██║ ╚████║██║██║     ███████╗██║  ██║
# ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
# ========================================================================================================================================

import numpy as np
import scipy.interpolate as si

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import logging
from threading import Thread
import requests
import shutil
import hashlib
import urllib.parse
from furl import furl
from retrying import retry
from random import randint
from random import uniform
from time import sleep
import os
import cfscrape
from proxy_randomizer import RegisteredProviders
from recaptcha_buster_bypass import SyncMe

# from configparser import ConfigParser

# =======================================================
# Variables
# =======================================================
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

itemID = os.getenv('ITEMID')

DOMAIN = os.getenv('DOMAIN')
SITEKEY = os.getenv('SITEKEY')

# Item Url
item_pattern = "https://www.gunbroker.com/item/"

# login url
login_url = "https://www.gunbroker.com/user/login"

# Randomization Related
MIN_RAND = 0.64
MAX_RAND = 1.27
LONG_MIN_RAND = 4.78
LONG_MAX_RAND = 11.1

# wait = WebDriverWait(driver, 67)
# driver.implicitly_wait(35)
# ---------------------------------------------------
# logging shit
# ---------------------------------------------------
# logging.getLogger('cfscrape').setLevel(logging.CRITICAL)

# -----------------------------------------------------
# Create cloudflare scraper isinstance
# -----------------------------------------------------
scraper = cfscrape.create_scraper()

driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
# For requests library
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}  # noqa: E501
# -------------------------------------------
# Setup retry
# -------------------------------------------
#  ____     ___  ______  ____   __ __ 
# |    \   /  _]|      ||    \ |  |  |
# |  D  ) /  [_ |      ||  D  )|  |  |
# |    / |    _]|_|  |_||    / |  ~  |
# |    \ |   [_   |  |  |    \ |___, |
# |  .  \|     |  |  |  |  .  \|     |
# |__|\_||_____|  |__|  |__|\_||____/ 

def retry_on_timeout(exception):
    """ Return True if exception is Timeout """
    return isinstance(exception, TimeoutException)


def retry_on_NoSuchElement(exception):
    """ Return True if exception is NoSuchElement """
    return isinstance(exception, NoSuchElementException)

def retry_on_StaleElement(exception):
    """ Return True if exception is StaleElementReferenceException """
    return isinstance(exception, StaleElementReferenceException)

# @retry(retry_on_exception=retry_on_timeout, stop_max_attempt_number=7)
# @retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)


# =============================================================================
# Begin
# -----------------------------------------------------------------------------

# ----------------------------------------------------------
#    ____    __              ____       __  _
#   / __/__ / /___ _____    / __ \___  / /_(_)__  ___  ___
#  _\ \/ -_) __/ // / _ \  / /_/ / _ \/ __/ / _ \/ _ \(_-<
# /___/\__/\__/\_,_/ .__/  \____/ .__/\__/_/\___/_//_/___/
#                 /_/          /_/
# ----------------------------------------------------------
def setup_options():
    opts = Options()
    opts.add_argument(
        '--user-agent=Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'  # noqa: E501
    )
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--lang=en-US")
    opts.add_argument("--host-rules='MAP gunbroker.com 127.0.0.1:5000'")
    opts.add_argument("--dns-prefetch-disable")
    opts.set_capability("javascript.enabled", True)
    # prefs.set_capability("browser.download.folderList", 2)
    opts.set_capability("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
    opts.set_capability("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    # opts.capabilities['proxy'] = {
    #     "proxyType": "MANUAL",
    #     "httpProxy": PROXY,
    #     "ftpProxy": PROXY,
    #     "sslProxy": PROXY
    # }


# ---------------------------------
# Setup firefox_profile
# ---------------------------------
def setup_profile():
    profile = webdriver.FirefoxProfile()
    profile._install_extension("./buster_captcha_solver-1.3.1.xpi", unpack=False)
    profile.set_preference("security.fileuri.strict_origin_policy", False)
    profile.update_preferences()


#    ___                      ____    __
#   / _ \_______ __ ____ __  / __/__ / /___ _____
#  / ___/ __/ _ \\ \ / // / _\ \/ -_) __/ // / _ \
# /_/  /_/  \___/_\_\\_, / /___/\__/\__/\_,_/ .__/
#                   /___/                  /_/
# -------------------------------------------------
def proxy_setup():
    rp = RegisteredProviders()
    rp.parse_providers()
    PROXY = rp.get_random_proxy()
    opts = Options()
    my_proxy = {
        "proxyType": "MANUAL",
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY
    }
    opts.set_capability(name='proxy', value=my_proxy)


# -------------------------------------------------
#    ___      _                ____    __          
#   / _ \____(_)  _____ ____  / __/__ / /___ _____ 
#  / // / __/ / |/ / -_) __/ _\ \/ -_) __/ // / _ \
# /____/_/ /_/|___/\__/_/   /___/\__/\__/\_,_/ .__/
#                                           /_/    
# -------------------------------------------------
def driver_setup():
    setup_profile()
    proxy_setup()
    setup_options()



# __      __    _ _     ___     _
# \ \    / /_ _(_) |_  | _ )___| |___ __ _____ ___ _ _
#  \ \/\/ / _` | |  _| | _ Y -_)  _\ V  V / -_) -_) ' \
#   \_/\_/\__,_|_|\__| |___|___|\__|\_/\_/\___\___|_||_|
# ------------------------------------------------------
def wait_between(a, b):
    rand = uniform(a, b)
    sleep(rand)


#   __  ___                    __  ___                            __
#  /  |/  /__  __ _____ ___   /  |/  /__ _  _____ __ _  ___ ___  / /____
# / /|_/ / _ \/ // (_-</ -_) / /|_/ / _ \ |/ / -_)  ' \/ -_) _ \/ __(_-<
#/_/  /_/\___/\_,_/___/\__/ /_/  /_/\___/___/\__/_/_/_/\__/_//_/\__/___/
# -----------------------------------------------------------------------
# Using B-spline for simulate humane like mouse movments
def human_like_mouse_move(action, start_element):
    points = [[6, 2], [3, 2], [0, 0], [0, 2]];
    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]

    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)

    x_tup = si.splrep(t, x, k=1)
    y_tup = si.splrep(t, y, k=1)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)

    startElement = start_element

    action.move_to_element(startElement);
    action.perform();

    c = 5  # change it for more move
    i = 0
    for mouse_x, mouse_y in zip(x_i, y_i):
        action.move_by_offset(mouse_x, mouse_y);
        action.perform();
        # self.log("Move mouse to, %s ,%s" % (mouse_x, mouse_y))
        i += 1
        if i == c:
            break;


#  _____          __      __
# / ___/__ ____  / /_____/ /  ___ _
#/ /__/ _ `/ _ \/ __/ __/ _ \/ _ `/
#\___/\_,_/ .__/\__/\__/_//_/\_,_/
#        /_/
# -----------------------------------
# @retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
@retry(retry_on_exception=retry_on_timeout, stop_max_attempt_number=7)
def do_captcha():
    driver.switch_to.default_content()
    iframes = driver.find_elements(by=By.TAG_NAME, value="iframe")
    driver.switch_to.frame(iframes[0])
    check_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
    wait_between(MIN_RAND, MAX_RAND)
    action = ActionChains(driver)
    human_like_mouse_move(action, check_box)
    check_box.click()
    wait_between(MIN_RAND, MAX_RAND)
    action = ActionChains(driver)
    human_like_mouse_move(action, check_box)
    # checkmark = driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
    challenge = driver.find_element(By.ID, "rc-imageselect")
    if challenge and challenge.is_displayed():
        driver.switch_to.default_content()
        driver.switch_to.frame(iframes[2])
        wait_between(LONG_MIN_RAND, LONG_MAX_RAND)
        capt_btn = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="solver-button"]'))
        )
        wait_between(LONG_MIN_RAND, LONG_MAX_RAND)
        capt_btn.click()
        wait_between(LONG_MIN_RAND, LONG_MAX_RAND)
        try:
            alert_handler = WebDriverWait(driver, 20).until(
                EC.alert_is_present()
            )
            alert = driver.switch_to.alert
            wait_between(MIN_RAND, MAX_RAND)
            alert.accept()
            wait_between(MIN_RAND, MAX_RAND)
            do_captcha()
        except NoSuchElementException:
            print("No Alert")
        driver.implicitly_wait(5)
        driver.switch_to.frame(iframes[0])


#   __             _
#  / /  ___  ___ _(_)__
# / /__/ _ \/ _ `/ / _ \
#/____/\___/\_, /_/_//_/
#          /___/
# ------------------------
@retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
@retry(retry_on_exception=retry_on_timeout, stop_max_attempt_number=7)
@retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
def login(username, password):
    driver.get(login_url)
    wait_between(a=MIN_RAND, b=MAX_RAND)
    cookie_message = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookie_message.click()
    try:
        username_input = driver.find_element(By.ID, "Username")
        username_input.send_keys(username)
    except NoSuchElementException:
        print("Login element not found")
    try:
        password_input = driver.find_element(By.ID, "Password")
        password_input.send_keys(password)
    except NoSuchElementException:
        print("Password element not found")
    wait_between(a=MIN_RAND, b=MAX_RAND)
    if cookie_message and cookie_message.is_displayed():
        cookie_message.click()
    try:
        do_captcha()
    except StaleElementReferenceException:
        print("Caught Stale Captcha Element")
    if cookie_message and cookie_message.is_displayed():
        cookie_message.click()
    driver.find_element(By.ID, "btnLogin").click()
    itemUrl = item_pattern + str(itemID)
    driver.get(itemUrl)


# ----------------------------------------------------
def browser_close():
    # os.chdir("../")
    driver.close()
    # driver.quit()


def __main__():
    driver_setup()
    login(username, password)
    # browser_close()


# get things rolling
if __name__ == "__main__":
    __main__()
