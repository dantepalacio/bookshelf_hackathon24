import requests
from bs4 import BeautifulSoup


def save_to_file(text, filename='parser_result.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def parse_book(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p', class_=False)
        paragraphs = paragraphs[:-4]
        
        all_text = "\n".join([p.get_text() for p in paragraphs])

        # print(all_text)

        save_to_file(all_text, 'p_result.txt')
        return all_text

    else:
        print(f"jopa: {response.status_code}")