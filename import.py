import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = 'postgres://aysddxnojxlpgr:8ddf0bdada2c7aa154806809e296b7020525362dd4a0bebd551e6b4fc24325c9@ec2-34-200-15-192.compute-1.amazonaws.com:5432/d6n9remruboocm'

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
