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


#If you are using Chrome version 87, please download ChromeDriver 87.0.4280.88
CORE = "https://www.myntra.com/"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
PRODUCT_URL = "https://www.myntra.com/gateway/v2/product/"
PRODUCT_LIST = ["12681772","12692600","1364628","1376577","10016983","11165778","12707640"]



class Myntra:
    """
       Allows interaction with the Myntra  service through a programmatic
       interface.
    """

    def __init__(self):
        """
        Constructs and returns an :class:`Myntra <Myntra>`. This
        will use a cookie jar stored, by default, picked in the home directory.
        """
        self.local_dir = os.path.dirname(os.path.realpath(__file__))
        self._pickle_path =  os.path.join(self.local_dir, "_myntra_cookies.p")

        if os.path.exists(self._pickle_path):
            print("Loading cookies from file")
            self.cookies = pickle.load(open(self._pickle_path, "rb"))

            # Check cookie validity
            expiry = min([c.get('expiry',99991098568) for c in self.cookies])
            if datetime.datetime.now().timestamp() > expiry:
                print("Cookies have expired ")
                self.cookies = self._get_cookies()

        self.session = requests.Session()

        for cookie in self.cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        with open("config.json", "r") as f:
            config = json.load(f)
        self.header = config

    def _get_cookies(self):
        '''
        Use selenium to load cookies if expired

        :return:
        '''
        _driver_path = os.path.join(self.local_dir, "chromedriver.exe")
        if not os.path.exists(_driver_path):
            raise Exception("Unable to find Driver file")

        # setting chrome driver options
        _options = Options()
        _options.headless = True
        _options.add_argument('user-agent={0}'.format(USER_AGENT))
        self.driver = webdriver.Chrome(_driver_path, options=_options)

        ##get all cookie
        self.driver.get(CORE)
        print(self.driver.title)
        print("Headless Chrome Initialized")
        pickle.dump(self.driver.get_cookies(), open("_myntra_cookies.p", "wb"))
        self.cookies = self.driver.get_cookies()
        self.driver.quit()
        return self.cookies

    def get_product_info(self,id):
        '''
         Handles getting data from rest end point
        :return:
        '''
        response = self.session.get(PRODUCT_URL + id, timeout=10, headers=self.header)
        print(response.status_code)
        # with open("product_" + id + ".json", "w") as f:
        #     json.dump(response.json(), f)

        product_data = (response.json())
        if response:
            print(f"\nproduct name {product_data.get('style').get('name')}")
            print(f"product price {product_data.get('style').get('mrp')}")
            for size in product_data.get('style').get('sizes'):
                print(f"\nsize is {size.get('label')}  ", end="")
                for seller in size.get('sizeSellerData'):
                    print(seller.get('discountedPrice'), end="", sep="   ")



myntra = Myntra()
print("Calling product end point with r"
      "equests")
for item in PRODUCT_LIST:
    myntra.get_product_info(item)

