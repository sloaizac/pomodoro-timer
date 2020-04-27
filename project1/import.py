import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    file = open("books.csv", "r")
    reader =  csv.reader(file, delimiter=',')
    next(reader)
    for line in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": line[0], "title": line[1], "author": line[2], "year": line[3]})
        print(f"adden{line}")
    db.commit()


if __name__ == "__main__":
    main()