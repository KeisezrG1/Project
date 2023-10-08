from flask import Flask, render_template, request
from pymongo import MongoClient


MONGO_URL = "mongodb+srv://KeisezrG:Shro0odRowdy@cluster0.a1fqnoh.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "library_management" 

app = Flask(__name__)
client = MongoClient(MONGO_URL)
db = client[DB_NAME]
books_collection = db["books"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_term = request.form["search_term"]
        search_results = search_books(search_term)
    else:
        search_results = []
    
    return render_template("index.html", search_results=search_results)

def search_books(search_term):
    query = {
        "$or": [
            {"title": {"$regex": search_term, "$options": "i"}},
            {"author": {"$regex": search_term, "$options": "i"}},
            {"publisher": {"$regex": search_term, "$options": "i"}},
        ]
    }
    results = books_collection.find(query)
    return results

if __name__ == "__main__":
    app.run(debug=True)
