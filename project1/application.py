import os

import requests
from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
 
app = Flask(__name__, template_folder='./views')
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SECRET_KEY"] ="my75secret84key20"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def generate_password(password):
    return generate_password_hash(password)

def check_password(pwhash, password):
    return check_password_hash(pwhash, password)

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['addReview', 'home']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['register', 'login', 'index']:
        return redirect(url_for('home'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    err = []
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get("username")
    password = request.form.get("password")
    if len(username) < 4:
        err.append("username should have 4 caracters at minimum")
    if len(password) < 6:
        err.append("very short password")
    if request.form.get("confirm-password") != password:
        err.append("passwords not coincide")
    if len(err) > 0:
        return render_template('register.html', errors=err)
    
    pwhash = generate_password(password)
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", 
    {"username": username, "password": pwhash})
    db.commit()
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    err = []
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get("username")
    password = request.form.get("password")
    if password == "" or username == "":
        err.append("all required fields")
    res = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
    if res is not None: 
        validate = check_password(res['password'], password)
        if validate == False:
            err.append('incorrect password')
    else:
        err.append("user not found")        
    if len(err) > 0:
        return render_template('login.html', errors=err)
    session['username'] = res['username']
    session['id'] = res['id']
    return render_template('home.html')
    
@app.route("/logout", methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('id')
    return redirect(url_for('login'))

@app.route("/home", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/search", methods=['POST'])
def search():
    parameters = "%" + request.form.get("parameters") + "%"
    res = db.execute("SELECT * FROM books WHERE lower(isbn) LIKE :parameters OR lower(title) LIKE :parameters OR lower(author) LIKE :parameters", {"parameters": parameters.lower()})
    return render_template('result-list.html', list=res)

@app.route("/<int:id>", methods=['GET'])
def get_book(id):
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id" : id}).fetchone()
    reviews = db.execute("SELECT reviews.*, users.id, users.username FROM reviews INNER JOIN users ON book_id = :id AND users.id = user_id", {"id": id}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "jq6iP1GCZCdCzG2Au6bQ", "isbns": book['isbn']})
    rev_count =  res.json()
    av_rating = rev_count['books'][0]['average_rating']
    num_rating = rev_count['books'][0]['ratings_count']
    return render_template('book-page.html', book=book, average_rating=av_rating, number_rating=num_rating, reviews=reviews)

@app.route("/add-review/<id>", methods=['POST'])
def addReview(id):
    err = []
    rating = int(request.form.get('star'))
    opinion = request.form.get('review')
    try:
        db.execute("INSERT INTO reviews (user_id, book_id, rating, opinion) VALUES (:user_id, :book_id, :rating, :opinion)", 
        {"user_id": session['id'], "book_id": id, "rating": rating, "opinion": opinion})
        db.commit()
    except:
        err.append("Already you commented this book")
    return redirect(url_for('get_book', id=id,  errors=err))

# api 

@app.route("/api/<isbn>")
def api_book(isbn):
    book =  db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is not None:
        res = db.execute("SELECT COUNT(*), SUM(rating) FROM reviews WHERE book_id = :id", {"id": book['id']}).fetchone()
        score = 0
        if res[0] != 0:
            score = res[1]/res[0]
        return jsonify({
            "title": book['title'],
            "author": book['author'],
            "year": book['year'],
            "isbn": book['isbn'],
            "review_count": res[0],
            "average_score": score
        }), 200
    return jsonify({"error":"Not found"}), 404



