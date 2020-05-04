# import section
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
  import env 

#mongodb
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ["MONGO_URI"]
app.config['MONGO_DBNAME'] = os.environ['MONGO_DBNAME']
mongo = PyMongo(app)

#Home Page
@app.route('/')
def homepage():
    return render_template("pages/index.html", TitlePage="Home")

#viewfilms page
@app.route('/movies/view', methods=['GET'])
def viewmovies():
    movies = mongo.db.movies.find().sort( { "title", 1 } )
    reviews = mongo.db.reviews.find()

#add lookup code $lookup { from: "reviews", look for review.title == movie.title, show all reviews with same title} 

    print(movies, reviews)
    return render_template("pages/viewfilms.html", movies=movies, reviews=reviews, TitlePage="Find A Movie")

#Leave review page
@app.route('/review/add')
def addreview():
    movies = mongo.db.movies.find()
    reviews =  mongo.db.reviews
    reviews.insert_one(request.form.to_dict())
    print(movies)
    return render_template("pages/addreview.html", movies=movies, reviews=reviews, TitlePage="Leave A Review")

#login page   
@app.route('/login')
def login():
    return render_template("pages/login.html", TitlePage="Login")
    
#user home page
@app.route('/dashboard')
def userhome():
    return render_template("pages/userhome.html", TitlePage="Admin")

#View All Reviews
@app.route('/review/view', methods=['GET','POST'])
def viewreviews():
    #reviews=mongo.db.reviews.find()
    #mongo.db.reviews.remove({'_id': ObjectId(reviews_id)})
    #print(reviews)
    return render_template("pages/viewallreviews.html", TitlePage="View Reviews")

#Edit films
@app.route('/movies/edit', methods=["GET"])
def editmovies():
    movies = mongo.db.movies.find()
    print(movies)
    return render_template("pages/edit.html", movies=movies)

#Add Movie
@app.route('/movies/add', methods=['POST'])
def addmovies():
    return render_template("pages/addfilm.html")

@app.route('/insertmovie', methods=['POST'])
def insertmovie():
    movies =  mongo.db.movies
    movies.insert_one(request.form.to_dict())
    return redirect(url_for('viewmovies'))    


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=(os.environ.get('PORT')),
            debug=True)