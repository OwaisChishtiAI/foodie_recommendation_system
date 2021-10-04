import mysql.connector
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import pickle

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

def recipe_titles_db():
    return pd.read_sql_query("SELECT recipe_id, recipe_ings FROM recipe_core", Connect().pointer()[1])

def update_db(recipe_id, cluster_id):
    sql = "UPDATE recipe_core SET cluster_id = {0} WHERE recipe_id = {1}".format(cluster_id, recipe_id)
    print("SQL: ", sql)
    connect = Connect()
    cursor, db = connect.pointer()
    cursor.execute(sql)

    db.commit()
    connect.close()


def transform(recipies):
    print("Tranforming Data")
    cleaned_recipies = []
    for each in recipies:
        cleaned_recipies.append(each.replace("\n", " "))

    ps = PorterStemmer()

    X = []
    for i in range(len(cleaned_recipies)):
        sa = cleaned_recipies[i].split()
        sa = [ps.stem(word) for word in sa if not word in set(stopwords.words('english'))]
        sa = ' '.join(sa)
        X.append(sa)
    print("Loading Vectorizer.")
    with open('models/vectorizer.pkl', 'rb') as fid:
        vectorizer = pickle.load(fid)

    X = vectorizer.transform(X)
    return X

def predict_cluster(recipe):
    with open('models/classifier.pkl', 'rb') as fid:
        model = pickle.load(fid)
    print("Predicting.")
    predicted = model.predict(recipe)
    return predicted

print("Reading Data")
data = recipe_titles_db()
# prep = transform([data['recipe_ings'].to_list()[0]])
# pred = predict_cluster(prep)
# print(pred)
for i in range(len(data['recipe_ings'])):
    prep = transform([data['recipe_ings'][i]])
    pred = predict_cluster(prep)
    update_db(data['recipe_id'][i], pred[0])