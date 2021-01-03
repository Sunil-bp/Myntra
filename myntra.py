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
import sqlite3

# If you are using Chrome version 87, please download ChromeDriver 87.0.4280.88
CORE = "https://www.myntra.com/"
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
PRODUCT_URL = "https://www.myntra.com/gateway/v2/product/"


class Myntra:
    """
       Allows interaction with the Myntra  service through a programmatic
       interface.
    """

    def __init__(self,size=None,product_url=None,product_id=None):
        """
        Constructs and returns an :class:`Myntra <Myntra>`. This
        will use a cookie jar stored, by default, picked in the home directory.
        """
        self.local_dir = os.path.dirname(os.path.realpath(__file__))
        self._pickle_path = os.path.join(self.local_dir, "_myntra_cookies.p")
        self.product_list = {}

        if os.path.exists(self._pickle_path):
            print("Loading cookies from file")
            self.__cookies = pickle.load(open(self._pickle_path, "rb"))
        else:
            self.__cookies = self._get_cookies()

        self.session = requests.Session()

        for cookie in self.__cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        with open("config.json", "r") as f:
            config = json.load(f)
        self.header = config


        #set database move to function later
        #check all tables  and if needed

        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(tables)
        tables = [item for t in tables for item in t]
        print(tables)

        if len(tables) !=3:
            if "PRODUCT" not in tables:
                print("Crating product tables")
                conn.execute('''CREATE TABLE PRODUCT
                         (ID INT PRIMARY KEY     NOT NULL,
                         PRODUCT_NAME           TEXT    NOT NULL,
                         PRODUCT_ID             INT     NOT NULL,
                         PRODUCT_URL            CHAR(200)   NULL,
                         SIZE                   CHAR(50)    NOT NULL,
                         IMAGE_URL              CHAR(200)  NOT NULL,
                         articleType            CHAR(50)    NOT NULL,
                         subCategory            CHAR(50)    NOT NULL,
                         masterCategory         CHAR(50)    NOT NULL,
                         gender                 CHAR(50)    NOT NULL,
                         brand                  CHAR(50)    NOT NULL
                         );''')

                print("Created product table")
            print(tables)
            if "SIZE" not in tables:
                print("Crating size tables")
                conn.execute('''CREATE TABLE SIZE
                                     (SIZE_ID    INT PRIMARY KEY     NOT NULL,
                                     PRODUCT_ID             INT    NOT NULL,
                                     SIZE                   CHAR(50)     NOT NULL,
                                      FOREIGN KEY(PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID)
                                     );''')


                print("Created size table")

            if "PRICE" not in tables:
                print("Crating PRICE tables")
                conn.execute('''CREATE TABLE PRICE
                                     (PRICE_ID    INT PRIMARY KEY     NOT NULL,
                                     PRODUCT_ID             INT    NOT NULL,
                                     SIZE_ID                  INT     NOT NULL,
                                     PRICE                 INT   NOT NULL,
                                     Date timestamp,
                                      FOREIGN KEY(PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID)
                                      FOREIGN KEY(SIZE_ID) REFERENCES SIZE(SIZE_ID)
                                     );''')

                print("Created PRICE table")


        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(tables)

        cursor.close()
        conn.close()
        wait  = input("hello")


        self.add_product(size,product_url,product_id)



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

    def get_products_info(self):
        for product  in self.product_list:
            self.get_product_info(product)

    def get_product_info(self, id):
        '''
         Handles getting data from rest end point
        :return:
        '''
        try:
            response = self.session.get(PRODUCT_URL + str(id), timeout=10, headers=self.header)
        except  requests.exceptions.ReadTimeout as e:
            print("Reloading cookies ")
            for cookie in self._get_cookies():
                self.session.cookies.set(cookie['name'], cookie['value'])
            response = self.session.get(PRODUCT_URL + str(id), timeout=10, headers=self.header)

        print(response.status_code)
        product_data = response.json()
        if response:
            print(f"\nProduct name {product_data.get('style').get('name')}")
            self.product_list[id]["name"]= product_data.get('style').get('name')
            print(f"Product price {product_data.get('style').get('mrp')}")
            self.product_list[id]["price"]= product_data.get('style').get('mrp')

            for size in product_data.get('style').get('sizes'):
                print(f"\nsize is {size.get('label')}  ", end="")
                for seller in size.get('sizeSellerData'):
                    print(seller.get('discountedPrice'), end="", sep="   ")
                    self.product_list[id][size.get('label')] =seller.get('discountedPrice')

    def add_product(self,size=None, product_url=None, product_id=None):
        if size not in ['m','s','l','xl','xxl','M','S','L','XL','XXL',"Onesize"]:
            # print("Please provide a valid size ")
            size = "All"
        if product_id:
            self.product_list[product_id] = {"ID":product_id,
                                               "size":size}
        elif product_url:
            product_id = product_url.split("/")[-2]
            self.product_list[product_id] = {"ID": product_id,
                                             "size": size}


    def products_trcked(self):
        for product in self.product_list:
            pprint( self.product_list.get(product))



myntra = Myntra()
myntra.products_trcked()
products = ["12681772", "12692600", "1364628", "1376577", "10016983", "11165778", "12707640"]
myntra.add_product(size="m",product_url="https://www.myntra.com/deodorant/spykar/spykar-men-ynr-body-deodorant-150-ml/11820384/buy")
myntra.products_trcked()
myntra.add_product(product_id=12681772)
myntra.get_products_info()
myntra.products_trcked()
