import pandas as pd
import requests

from app import db, app
from app.models import Book

csv_file_path = 'Books.csv' 
df = pd.read_csv(csv_file_path, nrows=2000)

url = 'http://127.0.0.1:5000/admin'

new_books = []

for index, row in df.iterrows():
    data = {
        'book_title': row['Book-Title'],
        'author': row['Book-Author'],
        'year': row['Year-Of-Publication'],
        'publisher': row['Publisher'],
        'book_cover': row['Image-URL-M']
    }

    book = Book(name=data['book_title'],# type: ignore
            rating=0.0, # type: ignore
            year=data['year'],# type: ignore
            book_cover=data['book_cover'],# type: ignore
            publisher=data['publisher'],# type: ignore
            author=data['author'])# type: ignore
    
    new_books.append(book)

with app.app_context():
    db.session.add_all(new_books)
    db.session.commit()

    
    # response = requests.post(url, data=data)

    # if response.status_code == 200:
    #     print(f"Book '{row['Book-Title']}' successfully sent.")
    # else:
    #     print(f"Failed to send book '{row['Book-Title']}'. Status code: {response.status_code}")
