import pandas as pd
import requests

csv_file_path = 'Books.csv' 
df = pd.read_csv(csv_file_path, nrows=2000)

url = 'http://127.0.0.1:5000/admin'

for index, row in df.iterrows():
    data = {
        'book_title': row['Book-Title'],
        'author': row['Book-Author'],
        'year': row['Year-Of-Publication'],
        'publisher': row['Publisher'],
        'book_cover': row['Image-URL-M']
    }
    
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print(f"Book '{row['Book-Title']}' successfully sent.")
    else:
        print(f"Failed to send book '{row['Book-Title']}'. Status code: {response.status_code}")
