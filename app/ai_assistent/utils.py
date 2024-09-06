import re

from googlesearch import search

def google_search(query):
    briefly_query = query + ' читать краткий пересказ брифли'
    response = search(briefly_query, tld='co.in',num=10, stop=10, pause=2)
    print(list(response)[0])


def split_text_overlap(text, max_fragment_length, overlap_length):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    fragments = []
    current_fragment = ""

    for sentence in sentences:
        if len(current_fragment) + len(sentence) <= max_fragment_length:
            current_fragment += sentence
        else:
            if current_fragment:
                fragments.append(current_fragment)

            current_fragment = sentence[:overlap_length]
            overlap = sentence[overlap_length:]
            while len(overlap) > max_fragment_length:
                fragments.append(current_fragment)
                current_fragment = overlap[:overlap_length]
                overlap = overlap[overlap_length:]

    if current_fragment:
        fragments.append(current_fragment)

    return fragments


if __name__ == "__main__":
    google_search('судьба человека')