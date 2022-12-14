#!/usr/bin/env python

# Copyright (C) 2022  anoduck

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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

# import numpy as np
# import scipy.interpolate as si

from selenium import webdriver
# from selenium.webdriver import Firefox
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# import crono
# import logging
# from threading import Thread
# import requests
from requests.exceptions import Timeout
# import shutil
# import hashlib
# import urllib.parse
# import asyncio
# from furl import furl
from retrying import retry
from random import randint
from random import uniform
from time import sleep
import os
import sys
# import cfscrape
# from proxy_randomizer import RegisteredProviders
import configparser

from configobj import ConfigObj
import art
import time
import click
import tomlkit
import cfscrape

sys.path.append(os.path.expanduser('~/.local/lib/python3.10'))
# =======================================================
# Variables
# =======================================================
item_pattern = 'https://www.gunbroker.com/item/'
login_url = "https://www.gunbroker.com/user/login"
min_ran = 15.3
max_ran = 37.1
# LONG_min_ran = 4.78
# LONG_max_rand = 11.1
item_file = os.path.join(os.curdir, 'item_store.toml')
# -------------------------------------------------------
cfg = """
[options]
username = string(default=os.getenv('USERNAME'))
password = string(default=os.getenv('PASSWORD'))
itemID = string(default=os.getenv('ITEMID'))
[domain]
DOMAIN = string(default=os.getenv('DOMAIN'))
SITEKEY = string(default=os.getenv('SITEKEY'))
item_pattern = string(default='https://www.gunbroker.com/item/')
login_url = string(default="https://www.gunbroker.com/user/login")
[rand]
min_ran = integer(0, 1, default=0.64)
max_rand = integer(0, 2, default=1.27)
LONG_min_ran = integer(0, 10, default=4.78)
LONG_max_rand = integer(0, 20, default=11.1)
"""

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


def retry_requests_timeout(exception):
    """Return True if RequestTimeoutException"""
    return isinstance(exception, Timeout)


# @retry(retry_on_exception=retry_on_timeout, stop_max_attempt_number=7)
# @retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
# @retry(retry_on_exception=retry_requests_timeout, stop_max_attempt_number=5)
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
    # opts.profile()
    # opts.profile.add_extension("buster_captcha_solver-1.3.1.xpi")
    opts.set_preference("security.fileuri.strict_origin_policy", False)
    # prefs.set_capability("browser.download.folderList", 2)
    # opts.set_capability("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
    # opts.set_capability("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
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
#     # profile._install_extension(addon="./buster_captcha_solver-1.3.1.xpi", unpack=False)
    profile.add_extension("buster_captcha_solver-1.3.1.xpi")
#     profile.set_preference("security.fileuri.strict_origin_policy", False)
#     profile.update_preferences()


#    ___                      ____    __
#   / _ \_______ __ ____ __  / __/__ / /___ _____
#  / ___/ __/ _ \\ \ / // / _\ \/ -_) __/ // / _ \
# /_/  /_/  \___/_\_\\_, / /___/\__/\__/\_,_/ .__/
#                   /___/                  /_/
# -------------------------------------------------
@retry(retry_on_exception=retry_requests_timeout, stop_max_attempt_number=5)
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
    return PROXY


# -------------------------------------------------
#    ___      _                ____    __          
#   / _ \____(_)  _____ ____  / __/__ / /___ _____ 
#  / // / __/ / |/ / -_) __/ _\ \/ -_) __/ // / _ \
# /____/_/ /_/|___/\__/_/   /___/\__/\__/\_,_/ .__/
#                                           /_/    
# -------------------------------------------------
def driver_setup():
    setup_profile()
    # proxy_setup()
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
# def human_like_mouse_move(action, start_element):
#     points = [[6, 2], [3, 2], [0, 0], [0, 2]];
#     points = np.array(points)
#     x = points[:, 0]
#     y = points[:, 1]

#     t = range(len(points))
#     ipl_t = np.linspace(0.0, len(points) - 1, 100)

#     x_tup = si.splrep(t, x, k=1)
#     y_tup = si.splrep(t, y, k=1)

#     x_list = list(x_tup)
#     xl = x.tolist()
#     x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

#     y_list = list(y_tup)
#     yl = y.tolist()
#     y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

#     x_i = si.splev(ipl_t, x_list)
#     y_i = si.splev(ipl_t, y_list)

#     startElement = start_element

#     action.move_to_element(startElement);
#     action.perform();

#     c = 5  # change it for more move
#     i = 0
#     for mouse_x, mouse_y in zip(x_i, y_i):
#         action.move_by_offset(mouse_x, mouse_y);
#         action.perform();
#         # self.log("Move mouse to, %s ,%s" % (mouse_x, mouse_y))
#         i += 1
#         if i == c:
#             break;


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
    wait_between(min_ran, max_rand)
    action = ActionChains(driver)
    # human_like_mouse_move(action, check_box)
    check_box.click()
    wait_between(min_ran, max_rand)
    action = ActionChains(driver)
    # human_like_mouse_move(action, check_box)
    # checkmark = driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
    # challenge = driver.find_element(By.ID, "rc-imageselect")
    driver.switch_to.default_content()
    driver.switch_to.frame(iframes[2])
    wait_between(LONG_min_ran, LONG_max_rand)
    capt_btn = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@id="solver-button"]'))
    )
    wait_between(LONG_min_ran, LONG_max_rand)
    capt_btn.click()
    wait_between(LONG_min_ran, LONG_max_rand)
    try:
        alert_handler = WebDriverWait(driver, 20).until(
            EC.alert_is_present()
        )
        alert = driver.switch_to.alert
        wait_between(min_ran, max_rand)
        alert.accept()
        wait_between(a=min_ran, b=max_rand)
        do_captcha()
    except NoSuchElementException:
        print("No Alert")
    driver.implicitly_wait(5)
    driver.switch_to.frame(iframes[0])


#     _
#  __| |___ ___ _ __  __ _ _ _ __ _ _ __
# / _` / -_) -_) '_ \/ _` | '_/ _` | '  \
# \__,_\___\___| .__/\__, |_| \__,_|_|_|_|
#              |_|   |___
# def resolve_captcha():
	# deep_trans()

		
#   __             _
#  / /  ___  ___ _(_)__
# / /__/ _ \/ _ `/ / _ \
#/____/\___/\_, /_/_//_/
#          /___/
# ------------------------
@retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
@retry(retry_on_exception=retry_on_timeout, stop_max_attempt_number=7)
@retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
def login(username, password, itemid):
    driver.get(login_url)
    wait_between(a=min_ran, b=max_ran)
    over_18 = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "ltkpopup-thanks"))
        )
    if over_18 and over_18.is_displayed():
        over_18.click()
    cookie_message = WebDriverWait(driver, 34).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    if cookie_message and cookie_message.is_displayed():
        cookie_message.click()
    time.sleep(randint(a=min_ran, b=max_ran))
    try:
        username_input = driver.find_element(By.ID, "Username")
        if username_input and username_input.is_displayed():
            username_input.send_keys(username)
    except NoSuchElementException:
        print("Login element not found")
    try:
        password_input = driver.find_element(By.ID, "Password")
        if password_input and password_input.is_displayed():
            password_input.send_keys(password)
    except NoSuchElementException:
        print("Password element not found")
    login_btn = driver.find_element(By.ID, "btnLogin")
    wait_between(a=min_ran, b=max_ran)
    checkmark = driver.find_element(
        By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
    if checkmark and checkmark.is_displayed():
        try:
            do_captcha()
        except StaleElementReferenceException:
            print("Caught Stale Captcha Element")
    else:
        login_btn.click()
        item_url = item_pattern + str(itemid)
        driver.get(item_url)
    return True


def write_toml(itemid, start_price, end_time):
    with tomlkit as tk:
        store = tk.document(item_file)
        store.add(tk.comment('Do not edit this file by hand'))
        store.add(tk.comment('This file stores data collected '
                             ' from scraping the item'))
        store.add(tk.nl())
        store.add("title", "GunBroker Sniper: Item Storage")
        item = tk.table()
        item.add("itemid", itemid)
        item.add("Starting Price", start_price)
        item.add("Ending Time", start_price)
        store.add("item", item)
    return True


# ----------------------------------------------
#   ___  ___ _____ ___    ___ _____ ___ __  __
#  / __|/ _ \_   _/ _ \  |_ _|_   _| __|  \/  |
# | (_ | (_) || || (_) |  | |  | | | _|| |\/| |
#  \___|\___/ |_| \___/  |___| |_| |___|_|  |_|
# ----------------------------------------------
def goto_item(itemid):
    item_url = item_pattern + str(itemID)
    driver.get(item_url)
    wait_between(a=min_ran, b=max_ran)
    c_url = driver.current_url
    if c_url == "https://www.gunbroker.com/Errors":
        print("Item no longer exists")
        sys.exit(0)
    more_outta = '/html/body/div[11]/div/div/div/div/div[1]/a'
    get_more = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.xpath, more_outta))
        )
    if get_more and get_more.is_displayed():
        get_more.click()
    bid_element = driver.find_element(By.ID, "StartingBid")
    start_price = bid_element.text()
    end_element = driver.find_element(By.ID, "EndingDate")
    end_time = end_element.text()
    toml_write = write_toml(itemid, start_price, end_time)
    if toml_write:
        print("Successfully added item to store")
    else:
        print("Whoops!")
    return True


# --------------------------------------
#    ___           ____     ___
#   / _ |_______ _/  ____  / ____
#  / __ / __/ _ `_/ // _ \/ _/ _ \
# /_/ |_\__/\_, /___/_//_/_/ \___/
#            /_/
# --------------------------------------
def info_acq():
    goto_item()
    min_bid = driver.find_element(By.ID, "StartingBid")
    end_time = driver.find_element(By.ID, "EndingDate")


# def cron_man():
    # crono.on(end_time)


# ----------------------------------------------------
def browser_close():
    # os.chdir("../")
    driver.close()
    # driver.quit()



def __main__():
    art.tprint("GunBroker Sniper", font="rnd-medium")
    conf_file = os.path.join(os.curdir, 'config.ini')
    # conf_path = os.path.realpath(conf_file)
    config = configparser.ConfigParser()
    config.read(conf_file)
    username = config['default']['username']
    password = config['default']['password']
    itemid = config['default']['itemid']
    # spec = cfg.split("\n")
    # if not os.path.isfile(conf_file):
    #     config = ConfigObj(conf_file, configspec=spec)
    #     config.filename = conf_file
    #     validator = ConfigObj.validate
    #     config.validate(validator, copy=True)
    #     config.write()
    #     print("Configuration file written to " + conf_path)
    #     sys.exit()
    # else:
    #     config = ConfigObj(conf_file, configspec=spec)
    driver_setup()
    logged_in = login(username, password, itemid)
    if logged_in:
        got_item = goto_item(itemid)
        if got_item:
            print('Hooray it worked!')
    else:
        print("Whoops!")
    # browser_close()


# get things rolling
if __name__ == "__main__":
    __main__()
