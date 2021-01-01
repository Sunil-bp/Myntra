import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#If you are using Chrome version 87, please download ChromeDriver 87.0.4280.88
CORE = "https://www.myntra.com/"
local_dir =  os.path.dirname(os.path.realpath(__file__))
DRIVER_PATH = os.path.join(local_dir,"chromedriver.exe")

if os.path.exists(DRIVER_PATH):
    print("driver found")

options = Options()
options.headless = True
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument('user-agent={0}'.format(user_agent))

driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get(CORE)
print(driver.title)
with open("index.html",'w', encoding="utf-8") as f:
    f.write(driver.page_source)
print ("Headless Chrome Initialized")

cookies = driver.get_cookies()
s = requests.Session()
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])

driver.quit()


for cookie in s.cookies:
    print(cookie.__dict__)
    print()


print("end")

