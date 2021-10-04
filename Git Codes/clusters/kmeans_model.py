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
    return pd.read_sql_query("SELECT recipe_title, recipe_ings FROM recipe_core", Connect().pointer()[1])

print("Reading Data")
data = recipe_titles_db()

recipies = data['recipe_ings'].to_list()
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

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(cleaned_recipies)
print("Learning Data")
true_k = 7
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

# order_centroids = model.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
print("Saving Models")
with open('models/classifier.pkl', 'wb') as fid:
    pickle.dump(model, fid)

with open('models/vectorizer.pkl', 'wb') as fid:
    pickle.dump(vectorizer, fid)

print("Done.")