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
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from requests.exceptions import Timeout
from retrying import retry
from random import randint
from random import uniform
from time import sleep
import os
import sys
import re
import configparser
import argparse
from requests_html import HTMLSession
import art
import time
import sched
from urllib.parse import urljoin
from datetime import date, datetime
import tomlkit


sys.path.append(os.path.expanduser('~/.local/lib/python3.10'))
# =======================================================
# Variables
# =======================================================
item_pattern = 'https://www.gunbroker.com/item/'
login_url = "https://www.gunbroker.com/user/login?ReturnUrl=/"
min_ran = int(15)
max_ran = int(37)
# LONG_min_ran = 4.78
# LONG_max_rand = 11.1
item_file = os.path.join(os.curdir, 'item_store.toml')
scheduler = sched.scheduler(time.time, time.sleep)
# -------------------------------------------------------
# cfg = """
# [options]
# username = string(default=os.getenv('USERNAME'))
# password = string(default=os.getenv('PASSWORD'))
# itemID = string(default=os.getenv('ITEMID'))
# [domain]
# DOMAIN = string(default=os.getenv('DOMAIN'))
# SITEKEY = string(default=os.getenv('SITEKEY'))
# item_pattern = string(default='https://www.gunbroker.com/item/')
# login_url = string(default="https://www.gunbroker.com/user/login")
# [rand]
# min_ran = integer(0, 1, default=0.64)
# max_rand = integer(0, 2, default=1.27)
# LONG_min_ran = integer(0, 10, default=4.78)
# LONG_max_rand = integer(0, 20, default=11.1)
# """

# wait = WebDriverWait(driver, 67)
# driver.implicitly_wait(35)
# ---------------------------------------------------
# logging shit
# ---------------------------------------------------
# logging.getLogger('cfscrape').setLevel(logging.CRITICAL)

# -----------------------------------------------------
# Create cloudflare scraper isinstance
# -----------------------------------------------------
# scraper = cfscrape.create_scraper()

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


# -------------------------------------------------
#    ___      _                ____    __          
#   / _ \____(_)  _____ ____  / __/__ / /___ _____ 
#  / // / __/ / |/ / -_) __/ _\ \/ -_) __/ // / _ \
# /____/_/ /_/|___/\__/_/   /___/\__/\__/\_,_/ .__/
#                                           /_/    
# -------------------------------------------------
def driver_setup():
    profile = webdriver.FirefoxProfile()
    profile.add_extension("buster_captcha_solver.xpi")
    opts = Options()
    opts.add_argument(
        '--user-agent=Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'  # noqa: E501
    )
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--lang=en-US")
    opts.add_argument("--host-rules='MAP gunbroker.com 127.0.0.1:5000'")
    # opts.add_argument("--dns-prefetch-disable")
    opts.set_capability("javascript.enabled", True)
    # opts.set_preference("security.fileuri.strict_origin_policy", False)
    driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
    return driver


#  _____          __      __
# / ___/__ ____  / /_____/ /  ___ _
#/ /__/ _ `/ _ \/ __/ __/ _ \/ _ `/
#\___/\_,_/ .__/\__/\__/_//_/\_,_/
#        /_/
# -----------------------------------
# @retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
@retry(retry_on_exception=retry_on_timeout, stop_max_attempt_number=7)
def do_captcha(driver):
    driver.switch_to.default_content()
    iframes = driver.find_elements(by=By.TAG_NAME, value="iframe")
    driver.switch_to.frame(iframes[0])
    check_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
    time.sleep(3)
    action = ActionChains(driver)
    # human_like_mouse_move(action, check_box)
    check_box.click()
    time.sleep(3)
    action = ActionChains(driver)
    # human_like_mouse_move(action, check_box)
    # checkmark = driver.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
    # challenge = driver.find_element(By.ID, "rc-imageselect")
    driver.switch_to.default_content()
    driver.switch_to.frame(iframes[2])
    time.sleep(3)
    capt_btn = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@id="solver-button"]'))
    )
    time.sleep(3)
    capt_btn.click()
    time.sleep(3)
    try:
        alert_handler = WebDriverWait(driver, 20).until(
            EC.alert_is_present()
        )
        alert = driver.switch_to.alert
        time.sleep(3)
        alert.accept()
        time.sleep(3)
        do_captcha(driver)
    except NoSuchElementException:
        print("No Alert")
    driver.implicitly_wait(5)
    driver.switch_to.frame(iframes[0])


# ----------------------------------------------------
#  ___         _      ___      _   _
# | _ \_  _ __| |_   | _ )_  _| |_| |_ ___ _ _
# |  _/ || (_-< ' \  | _ \ || |  _|  _/ _ \ ' \
# |_|  \_,_/__/_||_| |___/\_,_|\__|\__\___/_||_|
# ----------------------------------------------------
def push_login(driver):
    login_btn = WebDriverWait(driver, 34).until(
        EC.element_to_be_clickable((By.ID, "btnLogin")))
    if login_btn and login_btn.is_displayed():
        login_btn.click()
        print("I clicked the Button, and it go boom!")
        return True
    return False


# ----------------------------------
#   __             _
#  / /  ___  ___ _(_)__
# / /__/ _ \/ _ `/ / _ \
#/____/\___/\_, /_/_//_/
#          /___/
# ----------------------------------
# @retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
# @retry(retry_on_exception=retry_on_timeout, stop_max_attempt_number=7)
# @retry(retry_on_exception=retry_on_NoSuchElement, stop_max_attempt_number=3)
def login(driver, username, password, itemid):
    driver.get(login_url)
    over_18 = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "ltkpopup-thanks"))
    )
    if over_18 and over_18.is_displayed():
        over_18.click()
    username_input = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "Username")))
    if username_input and username_input.is_displayed():
        username_input.send_keys(username)
    password_input = driver.find_element(By.ID, "Password")
    if password_input and password_input.is_displayed():
        password_input.send_keys(password)
    logged_in = False
    try:
        checkmark = driver.find_element(
            By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
        if checkmark and checkmark.is_displayed():
            do_captcha(driver)
    except NoSuchElementException:
        logged_in = push_login(driver)
    if logged_in:
        item_url = item_pattern + str(itemid)
        driver.get(item_url)
        return True


# ----------------------------------------------------------------
#  ___ _    _
# | _ |_)__| |
# | _ \ / _` |
# |___/_\__,_|
# ----------------------------------------------------------------
def do_snipe(username, password, itemid, high_bid):
    driver = driver_setup()
    logged_in = login(driver, username, password, itemid)
    if logged_in:
		item_url = item_pattern + str(itemid)
		driver.get(item_url)
		time.sleep(3)
		c_url = driver.current_url
		if c_url == "https://www.gunbroker.com/Errors":
			print("Item no longer exists")
			sys.exit(0)
		bid_input = WebDriverWait(driver, 12).until(
			EC.visibility_of_element_located((By.ID, "MaxBidAmount")))
		if bid_input and bid_input.is_displayed():
			bid_input.send_keys(high_bid)
		bid_button = driver.find_element(By.ID, "bidButton")
		bid_button.click()
		page_title = driver.find_element(By.Class, "page-title")
		confirm_page = page_title.text
		if confirm_page == 'Confirm Bid':
			confirm_button = driver.find_element(By.ID, "btnBid")
			confirm_button.click()
		else:
			print('unable to find confirmation button')
		success_div = driver.find_element(By.Class, "text-success")
		success_msg = success_div.text
		if success_msg == 'Successful':
			return True
		else:
			print("Bid confirmation was unsuccessful")
	else:
		print("Logging in failed")
		return False


# -------------------------------------------
#   ___     _     ___       _
#  / __|___| |_  |   \ __ _| |_ ___
# | (_ / -_)  _| | |) / _` |  _/ -_)
#  \___\___|\__| |___/\__,_|\__\___|
# --------------------------------------------
# strformat = %m/%d/%Y %I:%M %p
# --------------------------------------------
def get_end_date(end_time):
    date_num = re.findall(r'\d+', end_time)
    dnum_list = list(map(int, date_num))
    dn_yr = dnum_list[2]
    dn_mon = dnum_list[0]
    dn_day = dnum_list[1]
    dn_hr = dnum_list[3]
    raw_min = dnum_list[4]
    dn_min = int(raw_min) - 15
    da_pm = re.findall(r'PM', end_time)
    if da_pm:
        dn_hr = int(dn_hr) + 12
    time_out = datetime(dn_yr, dn_mon, dn_day, dn_hr, dn_min)
    return time_out


# ---------------------------------------------------------------
#   ___ _           _     ___
#  / __| |_  ___ __| |__ |_ _|_ _
# | (__| ' \/ -_) _| / /  | || ' \
#  \___|_||_\___\__|_\_\ |___|_||_|
# Setup time for sniper to checkin to ensure specs and params
# ---------------------------------------------------------------
def get_checkin_date(end_time):
	date_num = re.findall(r'\d+', end_time)
	cki_list = list(map(int, date_num))
	cki_yr = cki_list[2]
    cki_mon = cki_list[0]
    cki_day = cki_list[1]
    cki_hr = cki_list[3]
    raw_min = cki_list[4]
    end_min = int(raw_min) - 15
	cki_min = int(end_min) - 15
    cki_pm = re.findall(r'PM', end_time)
    if cki_pm:
        cki_hr = int(cki_hr) + 12
    check_in = datetime(cki_yr, cki_mon, cki_day, cki_hr, cki_min)


def do_check(itemid, startprice, end_ttime, high_bid):
	session = HTMLSession()
    item_url = urljoin(item_pattern, itemid)
    i_page = session.get(item_url)
    ckbid_element = i_page.html.find('#StartingBid', first=True)
    ckstart_price = ckbid_element.text
    ckend_element = i_page.html.find('#EndingDate', first=True)
    ckend_time = ckend_element.text
	calc_end = get_end_date(ckend_time)
	calc_check_time = time.mktime(calc_end.timetuple()) + calc_end.microsecond / 1E6
	if calc_check_time == end_ttime:
		if ckstart_price < high_bid:
			return check_good
		else:
			print('Price rose above acceptable specification')
			sys.exit(0)
		
	
def ques_snipe(check_good, username, password, itemid, high_bid):
	if check_good:
		do_snipe(username, password, itemid, high_bid)


# ----------------------------------------------------
#  ___      _               ___ _        _ _
# / __| ___| |_ _  _ _ __  / __| |_ __ _| | |__
# \__ \/ -_)  _| || | '_ \ \__ \  _/ _` | | / /
# |___/\___|\__|\_,_| .__/ |___/\__\__,_|_|_\_\
#                   |_|
# https://docs.python.org/3/library/sched.html
# TODO: Check sched in jupyter
# ---------------------------------------------------
def setup_stalk(username, password, itemid, high_bid):
	with open(item_file, 'r') as tmk:
		tomlo = tomlkit.load(item_file)
		end_time = tomlo[itemid]["Ending Time"]
		buy_now = tomlo[itemid]["Buy_Now"]
		start_price = tomlo[itemid]["Starting_Price"]
		if high_bid >= buy_now:
			print('Bid amount is equal or exceeds Buy Now price')
			print('Please use "Buy Now" to purchase the item')
			sys.exit(0)
		end_obid = get_end_date(end_time)
		end_ttime = time.mktime(end_obid.timetuple()) + end_obid.microsecond / 1E6
		check_in = get_checkin_date(end_time)
		check_time = time.mktime(check_in.timetuple()) + check_in.microsecond / 1E6
		check_good = scheduler.enterabs(check_time, 1,
			                            action=do_check(itemid, startprice, end_ttime, high_bid))
		sniped = scheduler.enterabs(end_ttime, 2,
			                        action=quest_snipe(check_good, username, password, itemid, high_bid))
		if sniped:
			print('Item sniped')


# ----------------------------------------------------
#             _ _         _             _
# __ __ ___ _(_) |_ ___  | |_ ___ _ __ | |
# \ V  V / '_| |  _/ -_) |  _/ _ \ '  \| |
#  \_/\_/|_| |_|\__\___|  \__\___/_|_|_|_|
# ----------------------------------------------------
def write_toml(itemid, buy_now, start_price, end_time):
    store = tomlkit.document()
    store.add(tomlkit.comment('Do not edit this file by hand'))
    store.add(tomlkit.comment('This file stores data collected '
                              'from scraping the item'))
    store.add(tomlkit.nl())
    store.add('Title', 'GunBroker Sniper: Item Storage')
    itemid = tomlkit.table()
    itemid.add('itemid', itemid)
	itemid.add('Buy_Now', buy_now)
    itemid.add('Starting_Price', start_price)
    itemid.add('Ending_Time', end_time)
    store[itemid] = itemid
    write_toml = open(item_file, "w+", encoding="utf-8")
    write_toml.write(store.as_string())
    write_toml.close()
    return True


# ----------------------------------------------------------------
#  ___                          ___       __
# / __| __ _ _ __ _ _ __  ___  |_ _|_ _  / _|___
# \__ \/ _| '_/ _` | '_ \/ -_)  | || ' \|  _/ _ \
# |___/\__|_| \__,_| .__/\___| |___|_||_|_| \___/
#                  |_|
# ----------------------------------------------------------------
def scrape_info(itemid):
    session = HTMLSession()
    item_url = urljoin(item_pattern, itemid)
    i_page = session.get(item_url)
	# buy_now = i_page.html.xpath('/html/body/div[1]/div[1]/div[5]/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]')
	if bn_element = i_page.html.find('div.item-info-wrapper:nth-child(3) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)'):
		buy_now_raw = bn_element.tex
		buy_now = buy_now_raw.replace('$', '')
	else:
		buy_now = '0'
    bid_element = i_page.html.find('#StartingBid', first=True)
    start_price_raw = bid_element.text
    end_element = i_page.html.find('#EndingDate', first=True)
    end_time = end_element.text
	start_price = start_price_raw.replace('$', '')
    toml_write = write_toml(itemi, buy_now, start_price, end_time)
    if toml_write:
        print("Successfully added item to store")
    else:
        print("Whoops!")
    return True


# ----------------------------------------------------
def browser_close(driver):
    # os.chdir("../")
    driver.close()
    # driver.quit()


# -----------------------------------------------------------------
#  __  __      _
# |  \/  |__ _(_)_ _
# | |\/| / _` | | ' \
# |_|  |_\__,_|_|_||_|
# -----------------------------------------------------------------
def __main__():
    art.tprint("GunBroker Sniper", font="rnd-small")
    conf_file = os.path.join(os.curdir, 'config.ini')
    # conf_path = os.path.realpath(conf_file)
    prog = os.path.basename(__file__)

    ##################
    # ArgParse Setup #
    ##################
    p_arg = argparse.ArgumentParser(
        prog=prog,
        usage='%(prog)s.py  [--create|--stalk] and --config',
        description='An auction sniper for gunbroker',
        epilog='Please support Armin Sabastien\'s captcha buster: '
        ' https://github.com/dessant/buster',
        conflict_handler='resolve'
        )
    # Arguments for argparse
    p_arg.add_argument('-f', '--config', help='path to configuration file')
    p_arg.add_argument('-c', '--create', action='store_true',
                       help='Setup the snipe')
    p_arg.add_argument('-s', '--stalk', action='store_true',
                       help='Stalk item to snipe')

    ##################
    # parse the args #
    ##################
    args = p_arg.parse_args()

    #################
    # config parser #
    #################
    config = configparser.ConfigParser()
    config.read(conf_file)

    #################
    # get variables #
    #################
    username = config['default']['username']
    password = config['default']['password']
    itemid = config['default']['itemid']
	high_bid = config['default']['high_bid']

    ######
    # go #
    ######
    if args.create:
        scrape_info(itemid)
    if args.stalk:
        setup_stalk(username, password, itemid, high_bid)


# get things rolling
if __name__ == "__main__":
    __main__()
