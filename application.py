import os
from models import *
from werkzeug.security import generate_password_hash, check_password_hash


from flask import Flask, flash, session, render_template, request, url_for, redirect, g
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



app = Flask(__name__)
DATABASE_URL = 'postgres://owajnyzxapfjkj:11bc3ea7b5fcf8fe7f26231e5c614abfdb053e6c74b46d45e454747b694f799d@ec2-54-81-37-115.compute-1.amazonaws.com:5432/d2l50lkhkk3cn6'

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Check for environment variable
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SECRET_KEY"] = 'DNkWChBzTyb81CTXS2MU0A'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=['POST','GET'])
def index():
    # try:
    limit = request.form.get('books_display')
    
    # except ValueError:
    #     return "inavlid"
    
    if 'user_email' in session:
        user_email = session['user_email']
        
        books = db.execute("SELECT * FROM books LIMIT 10").fetchall()
        return render_template('index.html',limit=limit, books=books)
    
        
    
    # return 'You are not loged in'
    
    return render_template('login.html')


@app.route("/login", methods=['POST','GET'])
def login():
    session.pop("user_email", None)
    if request.method == 'POST':
        # return render_template('login.html')
    
        user_email = request.form.get('email')
        passwd = request.form.get('password')
    
        user = Users.query.filter_by(email=user_email).first()
        if not user:
            flash("Invalid username",'success')
            return render_template('login.html')
        
        if not check_password_hash(user.password, passwd):
            flash("Wrong password","success")
            return render_template('login.html')
    
        session['user_email'] = user.id
        flash("Logged in successfully",'success')
        return redirect(url_for('index'))
    
    if 'user_email' in session:
            user_email = session['user_email']
            return redirect(url_for('index'))
            
    return redirect(url_for('index'))

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    fname = request.form.get('firstname')
    lname = request.form.get('lastname')
    username = request.form.get('username')
    email = request.form.get('email')
    passwd = request.form.get('password')
    
    
    Users.add_user(id,fname, lname, username, email, generate_password_hash(passwd, method='sha256'))
    flash('Registration successful')
    return render_template('index.html')

 
    
@app.route("/logout", methods=['POST','GET'])  
def logout():
    session.pop("user_email", None) 
    return render_template('login.html')



@app.route("/books", methods=['POST','GET'])
def search_book():
    if request.method == "POST":
        isbn = request.form.get('search')
        book_title = request.form.get('search')
        
        book = db.execute("SELECT * FROM books WHERE isbn = :isbn",
                        {"isbn":isbn}).fetchone()

        
        # book = db.execute("SELECT * FROM books WHERE title = :title",
        #                 {"title":book_title}).fetchone()
        
        return render_template('books.html', book=book) 
    return redirect(url_for('index'))