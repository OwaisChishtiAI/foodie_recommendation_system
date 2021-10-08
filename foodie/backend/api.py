import mysql.connector
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from datetime import datetime
from dateutil import parser
import random

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
        self.cursor = self.db.cursor(buffered=True)
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
    print(titles[:5])
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
    username = request.form.to_dict()['username']
    print("RECIPE DETAILS AND RECOM SET #####################################", recipe_title)
    details = recipe_details_db(recipe_title, connect)
    connect = Connect()
    user_clicks_db(recipe_title, username, connect)
    return jsonify({"details" : details})

def recipe_details_db(recipe_title, connect):
    sql = "SELECT * FROM recipe_core WHERE recipe_title = '{}'".format(recipe_title)
    cursor, db = connect.pointer()
    cursor.execute(sql)
    details = cursor.fetchone()
    print("RECIPE: ", details)
    connect.close()
    return details

def user_clicks_db(recipe_title, username, connect):
    sql = "SELECT cluster_id FROM recipe_core WHERE recipe_title = '{}'".format(recipe_title)
    cursor, db = connect.pointer()
    cursor.execute(sql)
    cluster_id = cursor.fetchone()[0]
    # connect.close()
    sql2 = "SELECT list_of_clusters FROM user_clicks WHERE username = '{}'".format(username)
    cursor.execute(sql2)
    list_of_clusters = cursor.fetchone()[0]
    list_of_clusters = list_of_clusters + str(cluster_id)
    sql3 = "UPDATE user_clicks SET list_of_clusters = '{0}' WHERE username = '{1}'".format(list_of_clusters, username)
    cursor.execute(sql3)
    db.commit()

    clusters = [int(x) for x in list_of_clusters]
    cluster = max(clusters)
    sql4 = "UPDATE user_clicks SET recommended = '{0}' WHERE username = '{1}'".format(cluster, username)
    cursor.execute(sql4)
    db.commit()
    connect.close()
    print("[INFO] Recommendation SET TO: ", cluster)
    # return details

@app.route("/get_recommendations", methods=['POST'])
def get_recommendations_fn():
    connect = Connect()
    username = request.form.to_dict()['username']
    print("GET RECOMS #####################################", username)
    recommendations = get_recommendations_db(username, connect)
    return jsonify({"recommendations" : recommendations})

def get_recommendations_db(username, connect):
    sql = "SELECT recommended FROM user_clicks WHERE username = '{}'".format(username)
    cursor, db = connect.pointer()
    cursor.execute(sql)
    cluster_id = cursor.fetchone()[0]
    print("USER CLUSTER ID ", cluster_id)
    if cluster_id:
        sql2 = "SELECT recipe_img, recipe_title FROM recipe_core WHERE cluster_id = {}".format(cluster_id)
        cursor.execute(sql2)
        recommendations = cursor.fetchall()
        connect.close()
        # print(recommendations)
        recommendations = [random.choice(recommendations) for _ in range(5)]
        recommendations_li = []
        for each in recommendations:
            recommendations_li.append(list(each))
        return recommendations_li
    else:
        print("USER HAS NO RECOMMENDATIONS FOR NOW.")
    return ""

@app.route("/del_favourites", methods=['POST'])
def del_favourites_fn():
    connect = Connect()
    username = request.form.to_dict()['username']
    print("DEL FAVS #####################################", username)
    del_favourites_db(username, connect)
    return "200"

def del_favourites_db(username, connect):
    sql = "UPDATE favourites SET fav1='', fav2='', fav3='', fav4='', fav5='' WHERE username = '{}'".format(username)
    print(sql)
    cursor, db = connect.pointer()
    cursor.execute(sql)
    db.commit()
    connect.close()

@app.route("/add_favourites", methods=['POST'])
def add_favourites_fn():
    connect = Connect()
    data = request.form.to_dict()
    print("ADD FAVS #####################################", data)
    details = add_favourites_db(data, connect)
    return details

def add_favourites_db(data, connect):
    sql = "SELECT fav1, fav2, fav3, fav4, fav5 FROM favourites WHERE username = '{}'".format(data["username"])
    cursor, db = connect.pointer()
    cursor.execute(sql)
    details = cursor.fetchone()
    
    fav_number = 'undefined'
    for i in range(len(details)):
        if not details[i]:
            fav_number = i+1
            break
    if fav_number == "undefined":
        details = "404"
    else:
        print("AVAILABLE FAV INDEX", fav_number)
        sql2 = "UPDATE favourites SET fav{0} = '{1}' WHERE username = '{2}'".format(fav_number, data['recipe_title'], data["username"])
        cursor.execute(sql2)
        db.commit()
        details = "200"
    connect.close()
    return details

@app.route("/get_favourites", methods=['POST'])
def get_favourites_fn():
    connect = Connect()
    data = request.form.to_dict()
    print("GET FAVS #####################################", data)
    details = get_favourites_db(data, connect)
    return jsonify({"favs" : details})

def get_favourites_db(data, connect):
    sql = "SELECT fav1, fav2, fav3, fav4, fav5 FROM favourites WHERE username = '{}'".format(data["username"])
    cursor, db = connect.pointer()
    cursor.execute(sql)
    details_li = []
    details = cursor.fetchone()
    connect.close()
    for each in details:
        if each:
            details_li.append(each)
    return details_li

def login_db(data, connect):
    username = data['username']
    password = data['password']
    sql = "SELECT register_id FROM register WHERE username = '{0}' AND password = '{1}'".format(username, password)
    print("@@@@@@@@@@@@@", (sql))
    cursor, db = connect.pointer()
    cursor.execute(sql)
    register_id = cursor.fetchall()
    if register_id:
        sql2 = sql = "SELECT username FROM favourites WHERE username = '{}'".format(username)
        cursor.execute(sql2)
        exists = cursor.fetchone()
        print("USER EXISTS IN LOGIN")
        if not exists:
            sql3 = "INSERT INTO favourites (username) VALUES (%s);"
            cursor.execute(sql3, (username,))
            db.commit()
            print("USER SAVED IN FAVS")
        else:
            print("USER ALREADY EXISTS IN FAVS")

        sql4 = "SELECT username FROM user_clicks WHERE username = '{}'".format(username)
        cursor.execute(sql4)
        exists = cursor.fetchone()
        if not exists:
            sql5 = "INSERT INTO user_clicks (username, list_of_clusters, recommended) VALUES (%s, %s, %s);"
            cursor.execute(sql5, (username,"",""))
            db.commit()
            print("USER SAVED IN USER CLICKS")
        else:
            print("USER ALREADY EXISTS IN USER CLICKS")

    else:
        print("USER NOT FOUND")
    connect.close()
    return register_id

@app.route("/post_comments", methods=['POST'])
def post_comments_fn():
    connect = Connect()
    data = request.form.to_dict()
    print("POST COMMENTS DATA#####################################", data)
    status = post_comments_db(data, connect)
    if status:
        return "200"
    else:
        return "404"

def post_comments_db(data, connect):
    sql = "INSERT INTO recipe_review (recipe_title, review, user_email, user_name) VALUES (%s, %s, %s, %s);"
    vals = (data['recipe'], data['comment_msg'], data['comment_email'], data['comment_name'])
    print("@@@@@@@@@@@@@", (sql, vals))
    cursor, db = connect.pointer()
    cursor.execute(sql, vals)
    db.commit()
    connect.close()
    return True

@app.route("/get_comments", methods=['POST'])
def get_comments_fn():
    connect = Connect()
    recipe = request.form.to_dict()['recipe']
    print("GET COMMENTS DATA#####################################", recipe)
    reviews = get_comments_db(recipe, connect)
    if reviews:
        return jsonify({'reviews': reviews})
    else:
        return ""

def get_comments_db(recipe, connect):
    sql = "SELECT user_name, review FROM recipe_review WHERE recipe_title = '{}'".format(recipe)
    print("@@@@@@@@@@@@@", sql)
    cursor, db = connect.pointer()
    cursor.execute(sql)
    reviews = cursor.fetchall()
    connect.close()
    print("REVIEWS: ", reviews)
    if reviews:
        if len(reviews) > 3:
            reviews = reviews[:3]
        return reviews
    return ""

if __name__ == "__main__":
    try:
        # connect = Connect()
        app.run('0.0.0.0', debug=True)
    except Exception as e:
        print("[Exception] ", str(e))
    # connect = Connect()
    # get_recommendations_db("sowais672@gmail.com", connect)