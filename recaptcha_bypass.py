# https://github.com/teal33t/captcha_bypass
# Dont use this code for spy.

import unittest
import sys
import time

import numpy as np
import scipy
import scipy.interpolate as si
import os
import cfscrape

from datetime import datetime
from time import sleep, time
from random import uniform, randint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Randomization Related
MIN_RAND = 0.64
MAX_RAND = 1.27
LONG_MIN_RAND = 4.78
LONG_MAX_RAND = 11.1

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

# Variables for running gunbroker test on this shit
scraper = cfscrape.create_scraper()

# Update this list with proxybroker http://proxybroker.readthedocs.io
PROXY = [
    {"host": "34.65.217.248", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.15, "error_rate": 0.0},
    {"host": "198.46.160.38", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.36, "error_rate": 0.0},
    {"host": "18.162.100.154", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.62, "error_rate": 0.0},
    {"host": "18.210.69.172", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.22, "error_rate": 0.0},
    {"host": "204.12.202.198", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.3, "error_rate": 0.0},
    {"host": "23.237.100.74", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.32, "error_rate": 0.0},
    {"host": "206.189.192.5", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.63, "error_rate": 0.0},
    {"host": "23.237.173.109", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.4, "error_rate": 0.0},
    {"host": "167.71.83.150", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.41, "error_rate": 0.0},
    {"host": "34.93.171.222", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.92, "error_rate": 0.0},
    {"host": "157.245.67.128", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.61, "error_rate": 0.0},
    {"host": "18.162.89.135", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.71, "error_rate": 0.0},
    {"host": "198.98.55.168", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.65, "error_rate": 0.0},
    {"host": "157.245.124.217", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.7, "error_rate": 0.0},
    {"host": "129.146.181.251", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.76, "error_rate": 0.0},
    {"host": "134.209.188.111", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.78, "error_rate": 0.0},
    {"host": "68.183.191.140", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.82, "error_rate": 0.0},
    {"host": "35.192.138.9", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.29, "error_rate": 0.0},
    {"host": "157.245.207.112", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.85, "error_rate": 0.0},
    {"host": "68.183.191.248", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.87, "error_rate": 0.0},
    {"host": "165.22.54.37", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.88, "error_rate": 0.0},
    {"host": "71.187.28.75", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.34, "error_rate": 0.0},
    {"host": "157.245.205.81", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.92, "error_rate": 0.0},
    {"host": "45.76.255.157", "port": 808,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.45, "error_rate": 0.0},
    {"host": "157.245.197.92", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 1.01, "error_rate": 0.0},
    {"host": "159.203.87.130", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.47, "error_rate": 0.0},
    {"host": "50.195.185.171", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 1.03, "error_rate": 0.0},
    {"host": "144.202.20.56", "port": 808,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.51, "error_rate": 0.0},
    {"host": "157.230.250.116", "port": 8080,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 1.14, "error_rate": 0.0},
    {"host": "104.196.70.154", "port": 3128,
     "geo": {"country": {"code": "US", "name": "United States"}, "region": {"code": "Unknown", "name": "Unknown"},
             "city": "Unknown"}, "types": [{"type": "HTTPS", "level": ""}], "avg_resp_time": 0.64, "error_rate": 0.0}
]

index = int(uniform(0, len(PROXY)))
PROXY = PROXY[index]["host"] + ":" + str(PROXY[index]["port"])


class SyncMe(unittest.TestCase):
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

    # number = None
    headless = False
    options = None
    profile = None
    capabilities = None

    # Setup options for webdriver
    def setUpOptions(self):
        self.options = webdriver.FirefoxOptions()
        # self.options.add_option('useAutomationExtension', False)
        self.options.headless = self.headless

    # Setup profile with buster captcha solver
    def setUpProfile(self):
        self.profile = webdriver.FirefoxProfile()
        self.profile._install_extension("buster_captcha_solver_for_humans-0.7.2-an+fx.xpi", unpack=False)
        self.profile.set_preference("security.fileuri.strict_origin_policy", False)
        self.profile.update_preferences()

    # Enable Marionette, An automation driver for Mozilla's Gecko engine
    def setUpCapabilities(self):
        self.capabilities = webdriver.DesiredCapabilities.FIREFOX
        self.capabilities['marionette'] = True

    # Setup proxy
    def setUpProxy(self):
        self.log(PROXY)
        self.capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY
        }

    # Setup settings
    def setUp(self):
        self.setUpProfile()
        self.setUpOptions()
        self.setUpCapabilities()
        self.setUpProxy()  # comment this line for ignore proxy

        # On Linux?
        # https://github.com/mozilla/geckodriver/issues/1756
        binary = FirefoxBinary('/usr/lib/firefox-esr/firefox-esr')
        self.driver = webdriver.Firefox(options=self.options, capabilities=self.capabilities,
                                        firefox_profile=self.profile, executable_path='./geckodriver_linux',
                                        firefox_binary=binary)
        # self.driver = webdriver.Firefox(options=self.options, capabilities=self.capabilities, firefox_profile=self.profile, executable_path='./geckodriver_macOS')

    # Simple logging method
    def log(s, t=None):
        now = datetime.now()
        if t == None:
            t = "Main"
        print("%s :: %s -> %s " % (str(now), t, s))

    # Use time.sleep for waiting and uniform for randomizing
    def wait_between(self, a, b):
        rand = uniform(a, b)
        sleep(rand)

    # Using B-spline for simulate humane like mouse movments
    def human_like_mouse_move(self, action, start_element):
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
            self.log("Move mouse to, %s ,%s" % (mouse_x, mouse_y))
            i += 1
            if i == c:
                break;

    def do_captcha(self, driver):

        driver.switch_to.default_content()
        self.log("Switch to new frame")
        iframes = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])

        self.log("Wait for recaptcha-anchor")
        check_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))

        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)

        action = ActionChains(driver);
        self.human_like_mouse_move(action, check_box)

        self.log("Click")
        check_box.click()

        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)

        self.log("Mouse movements")
        action = ActionChains(driver);
        self.human_like_mouse_move(action, check_box)

        self.log("Switch Frame")
        driver.switch_to.default_content()
        iframes = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(iframes[2])

        self.log("Wait")
        self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

        self.log("Find solver button")
        capt_btn = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="solver-button"]'))
        )

        self.log("Wait")
        self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

        self.log("Click")
        capt_btn.click()

        self.log("Wait")
        self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

        try:
            self.log("Alert exists")
            alert_handler = WebDriverWait(driver, 20).until(
                EC.alert_is_present()
            )
            alert = driver.switch_to.alert
            self.log("Wait before accept alert")
            self.wait_between(MIN_RAND, MAX_RAND)

            alert.accept()

            self.wait_between(MIN_RAND, MAX_RAND)
            self.log("Alert accepted, retry captcha solver")

            self.do_captcha(driver)
        except:
            self.log("No alert")

        self.log("Wait")
        driver.implicitly_wait(5)
        self.log("Switch")
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])

    # Main function
    # def test_run(self):
    #     driver = self.driver
    #     number = self.number
    #
    #     self.log("Start get")
    #     driver.get('https://sync.me')
    #     self.log("End get")
    #
    #     self.log("Send phone")
    #
    #     # sync.me seems to have moved away from IDs
    #     # phone_input = driver.find_element_by_xpath('//*[@id="mobile-number"]')
    #     phone_input = driver.find_element_by_xpath('//input[@placeholder="Search any phone number"]')
    #     phone_input.send_keys(number)
    #
    #     self.log("Wait")
    #     self.wait_between(MIN_RAND, MAX_RAND)
    #
    #     search_btn = WebDriverWait(driver, 20).until(
    #             # EC.presence_of_element_located((By.ID ,"submit"))
    #             EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "SearchNumber_searchNumber__find")]'))
    #             )
    #
    #     self.log("Wait")
    #     self.wait_between(MIN_RAND, MAX_RAND)
    #     search_btn.click()
    #
    #     self.log("Wait")
    #     self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)
    #
    #
    #     self.do_captcha(driver)
    #
    #     self.log("Done")

    def login(self):

        driver = self.driver
        self.log("Fetch URL")
        driver.get(login_url)
        self.log("End Fetch")

        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)

        self.log("Sending Click")
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        self.log("click sent")

        self.log("Inserting Username")
        try:
            driver.find_element(By.ID, "Username").send_keys(username)
        except NoSuchElementException:
            print("Login element not found")

        self.log("Inserting Password")
        driver.find_element(By.ID, "Password").send_keys(password)
        self.log("Wait")
        self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

        self.do_captcha(driver)

        self.log("Wait")
        self.wait_between(MIN_RAND, MAX_RAND)

        self.log("Login")
        driver.find_element(By.ID, "btnLogin").click()

        self.log("wait")
        self.wait_between(MIN_RAND, MAX_RAND)

        self.log("Opening Item Page")
        itemUrl = item_pattern + str(itemID)
        driver.get(itemUrl)
        self.log("Opened Item Page")

    def tearDown(self):
        self.wait_between(21.13, 31.05)


if __name__ == "__main__":
    SyncMe.login()
    # if len(sys.argv) > 0:
    #     SyncMe.number = sys.argv.pop()
    # else:
    #     print("Must have number to check")
    #     exit(0)
    unittest.main()
