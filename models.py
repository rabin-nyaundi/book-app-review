from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(100), nullable=False, index=True)
    password =  db.Column(db.String(100), nullable=False)
    db.UniqueConstraint(email,username)
    
    def add_user(self, fname, lname, usern, email_ad, passw):
        user= Users(firstname=fname,lastname=lname,username=usern, email=email_ad, password=passw)
        db.session.add(user)
        db.session.commit()
        
        

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn =db.Column(db.String(255), unique=True, index=True, nullable=True)
    title =db.Column(db.String(255), nullable=False)
    author =db.Column(db.String(255), nullable=False)
    pub_year =db.Column(db.Text(255),  nullable=True)
    bk_review = db.relationship("Reviews", backref = "book", lazy = True)
    
    
    
    def add_book(self, isbn, title, author, pub_year):
        book = Books(isbn = isbn, title = title, author= author, pub_year=pub_year)
        db.session.add(book)
        db.session.commit()


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer)
    total_reviews = db.Column(db.Integer)
    avg_rating = db.Column(db.Integer)
    
