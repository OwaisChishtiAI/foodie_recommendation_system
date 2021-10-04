import mysql.connector
import pandas as pd
import os

class Connect:
    def __init__(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="foodie_db",
        )
        self.db = mydb
        self.cursor = self.db.cursor()
        print("[INFO] Connected to Data base.")
    
    def pointer(self):
        return (self.cursor, self.db)

    def close(self):
        self.cursor.close()
        self.db.close()

base_url = "https://www.pinterest.com/pin/"
pins_imgs = pd.read_csv("pin_images.csv")
pins_titles = pd.read_csv("pin_titles.csv")

def db_insert(data, connect):
    sql = "INSERT INTO recipe_core (recipe_pin, recipe_ings, recipe_img, recipe_url, recipe_title) VALUES (%s, %s, %s, %s, %s);"
    print("SQL: ", sql, data)
    cursor, db = connect.pointer()
    cursor.execute(sql, data)
    db.commit()
    connect.close()

non_en_pins = ['29836416272469246', '695243261222217731']

total_length = len(pins_imgs['pin_id'])
for i in range(len(pins_imgs['pin_id'])):
    data = []
    if str(pins_imgs['pin_id'][i]) not in non_en_pins:
        data.append(str(pins_imgs['pin_id'][i]))
        print(pins_imgs['pin_id'][i])
        data.append(open("recepies_data/{}.txt".format(str(pins_imgs['pin_id'][i]))).read())
        data.append(pins_imgs['pin_image'][i])
        data.append(base_url + str(pins_imgs['pin_id'][i]))
        title = pins_titles.loc[pins_titles['pin_id'] == str(pins_imgs['pin_id'][i])]['pin_image'].values
        if title:
            data.append(title[0])
        else:
            continue
        data = tuple(data)
        connect = Connect()
        db_insert(data, connect)
        print("{0}/{1}".format(i, total_length))