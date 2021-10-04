from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
import pickle

# url = "https://www.pinterest.com/dalahla/recipe-database/"

driver = webdriver.Chrome(r"E:\Investment Plans\SOC Solutions\Client's Project\Musavir\recommendation_system\crawler\chromedriver_win32\chromedriver.exe")

base_url = "https://www.pinterest.com/pin/"
pins = os.listdir("recepies_data")
ft = True
df = {"pin_id":[], "pin_image":[]}
total_pins = len(pins)
i = 1
for each in pins:
    print("{0}/{1}".format(i, total_pins))
    driver.get(base_url + each.split(".")[0])
    time.sleep(1.5)
    if ft:
        class_name = input("class_name: ")
        ft = False
    # print("************************************DEALING: ", url[url_ite])
    # input("Waiting...")
        
    try:
        image = driver.find_elements_by_xpath("//div[@class='{}']/img".format(class_name))
        print(image)
        df['pin_id'].append(each.split(".")[0])
        df['pin_image'].append(image[0].get_attribute("src"))
        print(each.split(".")[0], image[0].get_attribute("src"))
        # break
        i+=1
    except Exception as e:
        print(str(e))
        # break

a_file = open("images.pkl", "wb")
pickle.dump(df, a_file)
a_file.close()
df = pd.DataFrame(df)
try:
    df.to_csv("pin_images.csv", index=False)
except Exception as e:
    print(str(e))
    df.to_csv("pin_images.csv")
print("Saved DataFrame")
driver.close()
