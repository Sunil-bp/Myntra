"""
This module implements an API for interacting with Myntra website.
"""

import os
import requests
import json
from pprint import pprint
import datetime
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# If you are using Chrome version 87, please download ChromeDriver 87.0.4280.88
CORE = "https://www.myntra.com/"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
PRODUCT_URL = "https://www.myntra.com/gateway/v2/product/"
PRODUCT_LIST = ["12681772", "12692600", "1364628", "1376577", "10016983", "11165778", "12707640"]


class Myntra:
    """
       Allows interaction with the Myntra  service through a programmatic
       interface.
    """

    def __init__(self, products=list()):
        """
        Constructs and returns an :class:`Myntra <Myntra>`. This
        will use a cookie jar stored, by default, picked in the home directory.
        """
        self.local_dir = os.path.dirname(os.path.realpath(__file__))
        self._pickle_path = os.path.join(self.local_dir, "_myntra_cookies.p")
        self.product_list = []

        if os.path.exists(self._pickle_path):
            print("Loading cookies from file")
            self.__cookies = pickle.load(open(self._pickle_path, "rb"))

            # Check cookie validity
            expiry = min([c.get('expiry', 99991098568) for c in self.__cookies])
            print(expiry)
            print(datetime.datetime.now().timestamp())
            if datetime.datetime.now().timestamp() > expiry:
                print("Cookies have expired ")
                self.__cookies = self._get_cookies()

        self.session = requests.Session()

        for cookie in self.__cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        print("Updated cookies are ")
        expiry = min([c.get('expiry', 99991098568) for c in self.__cookies])
        print(expiry)
        with open("config.json", "r") as f:
            config = json.load(f)
        self.header = config
        self.add_product(products)



    def _get_cookies(self):
        '''
        Use selenium to load cookies if expired

        :return: cookies dict
        '''
        _driver_path = os.path.join(self.local_dir, "chromedriver.exe")
        if not os.path.exists(_driver_path):
            raise Exception("Unable to find Driver file")

        # setting chrome driver options
        _options = Options()
        _options.headless = True
        _options.add_argument("--incognito")
        _options.add_argument('user-agent={0}'.format(USER_AGENT))
        self.driver = webdriver.Chrome(_driver_path, options=_options)

        ##get all cookie
        self.driver.get(CORE)
        print(self.driver.title)
        print("Headless Chrome Initialized")
        pickle.dump(self.driver.get_cookies(), open("_myntra_cookies.p", "wb"))
        _cookies = self.driver.get_cookies()
        self.driver.quit()
        return _cookies

    def get_product_info(self, id):
        '''
         Handles getting data from rest end point
        :return:
        '''
        response = self.session.get(PRODUCT_URL + id, timeout=10, headers=self.header)
        print(response.status_code)
        product_data = response.json()
        if response:
            print(f"\nProduct name {product_data.get('style').get('name')}")
            print(f"Product price {product_data.get('style').get('mrp')}")
            for size in product_data.get('style').get('sizes'):
                print(f"\nsize is {size.get('label')}  ", end="")
                for seller in size.get('sizeSellerData'):
                    print(seller.get('discountedPrice'), end="", sep="   ")

    def add_product(self, products):
        if type(products) == type("str") or type(products) == type(12):
            self.product_list.append(products)
        else:
            for product in products:
                self.product_list.append(product)

    def products_trcked(self):
        for product in self.product_list:
            print(product)

myntra = Myntra("123")
myntra.products_trcked()
myntra.add_product(1233)
myntra.products_trcked()

# print("Calling product end point with r"
#       "equests")
# for item in PRODUCT_LIST:
#     myntra.get_product_info(item)
