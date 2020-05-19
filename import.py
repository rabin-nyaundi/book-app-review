import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = 'postgres://owajnyzxapfjkj:11bc3ea7b5fcf8fe7f26231e5c614abfdb053e6c74b46d45e454747b694f799d@ec2-54-81-37-115.compute-1.amazonaws.com:5432/d2l50lkhkk3cn6'

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open('books.csv')
    reader = csv.reader(f)
    
    for isbn, title, author, year, in reader:
        if db.execute("INSERT INTO books (isbn,title, author, pub_year) VALUES(:isbn, :title, :author, :pub_year)",
                   {"isbn" : isbn, "title": title, "author": author,"pub_year": year}):
            print("Successful")
        
        print(f"Added {isbn}, {title}, {author} and {year} to books table")
    db.commit()
    
if __name__ =="__main__":
    main()    
