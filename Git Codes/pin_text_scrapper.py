from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

# url = "https://www.pinterest.com/dalahla/recipe-database/"

driver = webdriver.Chrome(r"E:\Investment Plans\SOC Solutions\Client's Project\Musavir\recommendation_system\crawler\chromedriver_win32\chromedriver.exe")

url = "https://www.pinterest.com"

covered_pins = os.listdir("recepies_data")
covered_pins_li = [x.split(".")[0] for x in covered_pins]
# print(covered_pins_li)
pins = open("pins_2.txt", "r").read().split("\n")
i = 0
for pin in pins:
    try:
        if pin.split("/")[-2] not in covered_pins_li:
            pin_url = url + pin
            driver.get(pin_url)
            time.sleep(1.5)
            upload_field = driver.find_element_by_css_selector("div[itemtype='https://schema.org/Recipe']")
            
            # print(upload_field.text)
            with open("recepies_data/{}.txt".format(pin.split("/")[-2]), "w", encoding="utf8", errors="ignore")as f:
                f.write(upload_field.text)
            print("saved file: ", pin)
        else:
            print("Omiiting PIN: ", pin)
        
    except Exception as e:
        with open("wasted_pins.txt", "w", encoding="utf8", errors="ignore")as f:
            f.write(pin + "\n")
        print(str(e))
        pass
    print("Ite: ", i)
    i+=1
driver.close()