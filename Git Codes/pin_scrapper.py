# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# url = "https://www.pinterest.com/dalahla/recipe-database/"

driver = webdriver.Chrome(r"E:\Investment Plans\SOC Solutions\Client's Project\Musavir\recommendation_system\crawler\chromedriver_win32\chromedriver.exe")

# driver.get(url)

# time.sleep(5)
# a = driver.find_element_by_class_name("Yl- MIw Hb7")
# print(a)

# input("> ")
# driver.close()



#  Any infinity scroll URL
var = "analytics"
url = ["https://www.pinterest.com/dalahla/recipe-database/",\
    "https://www.pinterest.com/search/pins/?q=Cooking%20recipes&rs=srs&b_id=BEVvS7GA51eSAAAAAAAAAACYfDhqD7-Texxc0JYBf6SMAJgN0cRHdBiXckOY6B3rW-dHPflN4Dt3inCQk9_feXg&source_id=axKqlNsK",\
        "https://www.pinterest.com/search/pins/?q=Healthy%20recipes&rs=srs&b_id=BOZ0l8pe0yO_AAAAAAAAAAC257gGbCW6VaGxmMTGKHT0G1_I4Ja0FrpUmJ_D9V4mm82jo1Wcp2wZUnLi6IqfaU4&source_id=axKqlNsK",\
            "https://www.pinterest.com/search/pins/?q=Dinner%20recipes&rs=srs&b_id=BJwMr07aQLXPAAAAAAAAAAAvCcYJqBu9-m4vdjfI_PDN372p7v9HKaDGMOeEvtzrSaN9jmd_pJ9W&source_id=axKqlNsK",\
                "https://www.pinterest.com/search/pins/?q=Yummy%20food&rs=srs&b_id=BDEKQimtn_smAAAAAAAAAABjQje5V_G8fb9Xm6xgPpVr5u3ngGeZ3bqpY1i2ZOGkRb632KEyKA3_&source_id=axKqlNsK",\
                    "https://www.pinterest.com/search/pins/?q=Vegetarian%20recipes&rs=srs&b_id=BJf1ZDAZQQNEAAAAAAAAAADdB01hlxJ6ffpipo-Kki2xajcPJ1fTpKbzh05-z6I-e9pG8L9KX6K_JPuQz3z310g&source_id=axKqlNsK"] 
ScrollNumber = 20  # The depth we wish to load
sleepTimer = 2    # Waiting 1 second for page to load

#  Bluetooth bug circumnavigate
# options = webdriver.ChromeOptions() 
# options.add_experimental_option("excludeSwitches", ["enable-logging"])

# driver = webdriver.Chrome(options=options)  # path=r'to/chromedriver.exe'


for url_ite in range(len(url)):
    driver.get(url[url_ite])
    print("************************************DEALING: ", url[url_ite])
    input("Waiting...")
    for i in range(1,ScrollNumber):
        
        try:
            driver.execute_script("window.scrollTo(1,100000)")
            print("scrolling: ", i)
            time.sleep(sleepTimer)

            soup = BeautifulSoup(driver.page_source,'html.parser')
            links = []
            for link in soup.find_all('a'):
                # print("link: ", link)
                href = link.get('href')
                if "/pin/" in href:
                    if href not in links:
                        links.append(href)

            with open("pins_2.txt", "a", encoding="utf8", errors="ignore")as f:
                for each in links:
                    f.write(each + "\n")
        except Exception as e:
            print(str(e))
            break
driver.close()



# driver.get(url)
# # time.sleep(5)
# input("Waiting...")
# try:
#     soup = BeautifulSoup(driver.page_source,'html.parser')
#     links = []
#     for link in soup.find_all('a'):
#         # print("link: ", link)
#         href = link.get('href')
#         if "/pin/" in href:
#             if href not in links:
#                 links.append(href)

#     with open("pins_2.txt", "a", encoding="utf8", errors="ignore")as f:
#         for each in links:
#             f.write(each + "\n")
# except Exception as e:
#     print(str(e))
#     pass
# driver.close()