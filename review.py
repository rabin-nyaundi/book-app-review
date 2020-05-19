import os, requests
from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = 'postgres://owajnyzxapfjkj:11bc3ea7b5fcf8fe7f26231e5c614abfdb053e6c74b46d45e454747b694f799d@ec2-54-81-37-115.compute-1.amazonaws.com:5432/d2l50lkhkk3cn6'

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

mykey = 'rjn0HQqCvwdTx3JCEorA'
# secret = 'cQvqoQA7cOGx2XIQe6ApOqBZQBXGMMwVkTDBuRnxKEM

isbn_list =[]
def main():
    book_isbn = db.execute("SELECT isbn FROM books LIMIT 10").fetchall()
    for isbn in book_isbn:

        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": mykey, "isbns": isbn})
        if res.status_code != 200:
            raise Exception ("Error: API unscuccessful")
        data = res.json()
        
        total_reviews = data.books["author.show"]
        # avg_rating = data["average_rating"]
        # isbn_list.append(data)
        
        print(data)
        print("*******")
        # print(isbn_list)
    # print(data)
    
if __name__ == "__main__":
    main()
    