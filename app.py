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
    return render_template("pages/index.html")

#viewfilms page
@app.route('/viewfilms')
def viewfilms():
    films=mongo.db.films.find()
    print(films)
    return render_template("pages/viewfilms.html", films=films)

#viewreviews page
@app.route('/viewreviews')
def viewreviews():
    reviews=mongo.db.reviews.find()
    print(reviews)
    return render_template("pages/viewreviews.html", reviews=reviews)


#addreviews page
@app.route('/addreviews', methods=['GET'])
def addreviews():
    return render_template("pages/addreviews.html")

@app.route('/insertreview', methods=['POST'])
def insertreview():
    reviews =  mongo.db.reviews
    reviews.insert_one(request.form.to_dict())
    return redirect(url_for('viewreviews'))

#addfilm page
@app.route('/addfilm', methods=['GET'])
def addfilm():
    return render_template("pages/addfilm.html")

@app.route('/insertfilm', methods=['POST'])
def insertfilm():
    films =  mongo.db.films
    films.insert_one(request.form.to_dict())
    return redirect(url_for('viewfilms'))

#login page   
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get['username'] != 'admin' or request.form.get['password'] != 'password':
            error = 'Invalid Username or Password. Please try again.'
        else:
            return redirect(url_for('userhome'))
    return render_template("pages/login.html", error=error)
    
#user home page
@app.route('/userhome', methods=['GET'])
def userhome():
    return render_template("pages/userhome.html")

#Edit films   
@app.route('/editfilms')
def editfilms():
    films=mongo.db.films.find()
    print(films)
    return render_template("pages/filmlisting.html", films=films)

@app.route('/updatefilm/<film_id>', methods=["POST"])
def update_film(film_id):
    films=mongo.db.films
    films.update( {'_id': ObjectId(film_id)},
    {
        'film_name':request.form.get('film_name'),
        'film_director': request.form.get('film_director'),
        'film_description': request.form.get('film_description'),
        'film_genre':request.form.get('film_genre')
       # 'film_year':request.form.get('film_year')
       # 'film_age':request.form.get('film_age')
       # 'film_poster':request.form.get('film_poster')
    })
    return redirect(url_for('editfilms'))

#Delete films   
@app.route('/deletefilms')
def deletefilms():
    films=mongo.db.films.find()
    print(films)
    return render_template("pages/deletefilms.html", films=films)

@app.route('/delete_film/<films_id>')
def delete_film(task_id):
    mongo.db.films.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('deletefilms'))


#Delete reviews
@app.route('/deletereviews')
def deletereviews():
    reviews=mongo.db.reviews.find()
    print(reviews)
    return render_template("pages/deletereviews.html", reviews=reviews)

@app.route('/delete_review/<review_id>')
def delete_review(reviews_id):
    mongo.db.reviews.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('deletereviews'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=(os.environ.get('PORT')),
            debug=True)