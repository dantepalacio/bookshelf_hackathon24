from googlesearch import search

query = 'брифли читать краткий пересказ война и мир том 1'

for j in search(query, tld='co.in',num=10, stop=10, pause=2):
    print(j)