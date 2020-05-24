import os, requests
from models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = 'postgres://aysddxnojxlpgr:8ddf0bdada2c7aa154806809e296b7020525362dd4a0bebd551e6b4fc24325c9@ec2-34-200-15-192.compute-1.amazonaws.com:5432/d6n9remruboocm'

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

mykey = 'rjn0HQqCvwdTx3JCEorA'
# secret = 'cQvqoQA7cOGx2XIQe6ApOqBZQBXGMMwVkTDBuRnxKEM

def main():
    book_isbn = db.execute("SELECT isbn FROM books LIMIT 1").fetchall()
    for isbn in book_isbn:

        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": mykey, "isbns": isbn})
        if res.status_code != 200:
            raise Exception ("Error: API unscuccessful")

        data = res.json()
        print(data)
        # g_isbn = data["books"][0]['isbn']
        # g_reviews = data["books"][0]['work_reviews_count']
        # g_rating = data["books"][0]['average_rating']
        
        # db.execute("INSERT INTO reviews (book_isbn, total_reviews, avg_rating) VALUES( :isbn, :total_reviews, :avg_rating)",
        #            {"isbn" : g_isbn,  "total_reviews" :g_reviews, "avg_rating" : g_rating})
        # print("Successful")
        # print(f"Inserted {g_rating} and {g_reviews} into reviews table successfully")
        # db.commit()

        # print(g_rating, g_reviews)
        print("*******")
        # print(isbn_list)
    print(data)
    
if __name__ == "__main__":
    main()
    