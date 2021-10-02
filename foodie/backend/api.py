import mysql.connector
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from datetime import datetime
from dateutil import parser

app = Flask(__name__)
CORS(app)

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

@app.route("/register", methods=['POST'])
def register_fn():
    connect = Connect()
    data = request.form.to_dict()
    print("RESGISTER DATA#####################################", data)
    status = register_db(data, connect)
    if status:
        return "200"
    else:
        return "404"

def register_db(data, connect):
    keys = ""
    vals = []
    for key, val in data.items():
        keys = keys + key + ", "
        vals.append(val)
    vals = tuple(vals)
    print(keys)
    sql = "INSERT INTO register ({0}) VALUES (%s, %s);".format(keys[:-2])
    print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql, vals)
    db.commit()
    connect.close()
    return True

@app.route("/login", methods=['POST'])
def login_fn():
    connect = Connect()
    data = request.form.to_dict()
    print("LOGIN DATA#####################################", data)
    register_id = login_db(data, connect)
    if register_id:
        return "200"
    else:
        return "404"

@app.route("/recipe_titles", methods=['POST'])
def recipe_titles_fn():
    connect = Connect()
    print("RECIPE TITLES #####################################")
    titles = recipe_titles_db(connect)
    return jsonify({"recipies" : titles})

def recipe_titles_db(connect):
    sql = "SELECT recipe_title FROM recipe_core"
    cursor, db = connect.pointer()
    cursor.execute(sql)
    titles = cursor.fetchall()
    connect.close()
    titles_li = []
    for each in titles:
        titles_li.append(each[0])
    return titles_li

@app.route("/recipe_details", methods=['POST'])
def recipe_details_fn():
    connect = Connect()
    recipe_title = request.form.to_dict()['recipe']
    print("RECIPE DETAILS #####################################", recipe_title)
    details = recipe_details_db(recipe_title, connect)
    return jsonify({"details" : details})

def recipe_details_db(recipe_title, connect):
    sql = "SELECT * FROM recipe_core WHERE recipe_title = '{}'".format(recipe_title)
    cursor, db = connect.pointer()
    cursor.execute(sql)
    details = cursor.fetchone()
    connect.close()
    return details

def login_db(data, connect):
    username = data['username']
    password = data['password']
    sql = "SELECT register_id FROM register WHERE username = '{0}' AND password = '{1}'".format(username, password)
    print("@@@@@@@@@@@@@", (sql))
    cursor, db = connect.pointer()
    cursor.execute(sql)
    register_id = cursor.fetchall()
    connect.close()
    return register_id

if __name__ == "__main__":
    try:
        # connect = Connect()
        app.run('0.0.0.0', debug=True)
    except Exception as e:
        print("[Exception] ", str(e))