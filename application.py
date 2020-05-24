import requests
from flask import Flask,flash, render_template, jsonify, request, session, url_for, redirect
from models import *

from werkzeug.security import generate_password_hash, check_password_hash

from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
DATABASE_URL = 'postgres://aysddxnojxlpgr:8ddf0bdada2c7aa154806809e296b7020525362dd4a0bebd551e6b4fc24325c9@ec2-34-200-15-192.compute-1.amazonaws.com:5432/d6n9remruboocm'

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
    
    if 'user_email' in session:
        user_email = session['user_email']
        
        books = db.execute("SELECT * FROM books LIMIT 10").fetchall()
        return render_template('index.html', session = session['user_email'], books=books)
    
        
    
    # return 'You are not loged in'
    
    return render_template('login.html')


@app.route("/login", methods=['POST','GET'])
def login():
    session.pop("user_email", None)
    
    if request.method == 'POST':
    
        user_email = request.form.get('email')
        passwd = request.form.get('password')
    
        user = Users.query.filter_by(email=user_email).first()
        if not user:
            flash("Wrong email address",'danger')
            return render_template('login.html')
        
        if not check_password_hash(user.password, passwd):
            flash("Wrong password","danger")
            return render_template('login.html')
    
        session['user_email'] = user.email
        return redirect(url_for('index'))
        flash("Logged in successfully",'success')
    
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
    
    if db.execute("SELECT * FROM users WHERE email = :email",
                  {"email":email}).fetchone():
        flash('User already exists! Go to login', 'danger')
        return render_template('signup.html')
    
    Users.add_user(id,fname, lname, username, email, generate_password_hash(passwd, method='sha256'))
    flash('Registration successful',"success")
    return render_template('signup.html')
    

 
    
@app.route("/logout", methods=['POST','GET'])  
def logout():
    session.pop("user_email", None) 
    
    return redirect(url_for('index'))


@app.route("/books", methods=['POST','GET'])
def search_book():
    if request.method == "POST":
        book = request.form.get('search')
        
        book_result = db.execute("SELECT * FROM books WHERE title LIKE :book OR isbn LIKE :book OR author LIKE :book LIMIT 10", 
                                 {"book": f"%{book}%"}).fetchall()
                   
        if not book_result:
            flash("No matches found for your search",'danger')
            
        return render_template('index.html', session = session['user_email'], book_result= book_result) 
    
    return redirect(url_for('index'))


@app.route("/<string:isbn>", methods=['POST','GET'])
def book(isbn):
    mykey = 'rjn0HQqCvwdTx3JCEorA'
    
    book_info = db.execute("SELECT * FROM books WHERE isbn = :isbn",
                            {"isbn" :isbn}).fetchone() 
    
    revw =  db.execute("SELECT * FROM reviews WHERE book_id = :book_id",
                              {"book_id": book_info.id}).fetchall()
    
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": mykey, "isbns": isbn})
    if res.status_code != 200:
        raise Exception ("Error: API unscuccessful")
    data = res.json()
    result  =  data['books'][0]
        
    # return render_template('book.html',session = session['user_email'], book_info= book_info,result = result)
            
    if request.method =='GET':
        if session.get('user_email') is None:
            return redirect(url_for('index'))
        
        return render_template('book.html',session = session['user_email'], book_info= book_info,result = result, revw=revw)

    if request.method == "POST":
        user =  db.execute("SELECT *  FROM users WHERE email = :email",
                              {"email":session['user_email']}).fetchone()
        book =  db.execute("SELECT * FROM books WHERE isbn = :isbn",
                           {"isbn":isbn}).fetchone()
        book_id = book.id
        user_id =  user.id
    
        if db.execute("SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id",
                      {"user_id":user.id ,"book_id":book_id}).fetchone():
            flash("You already submited a review for this book","danger")
            return render_template('book.html',session = session['user_email'], book_info= book_info,result = result)
            
        else:
            rating = request.form.get('rating')
            message =  request.form.get('message')
            
            Reviews.add_review(id,user_id, book_id,message,rating)   
            flash('Book review added','success') 
           
            revw =  db.execute("SELECT * FROM reviews WHERE book_id = :book_id",
                              {"book_id": book_id}).fetchall()
            
            return render_template('book.html',session = session['user_email'], book_info= book_info,result=result, revw=revw)

            