import requests
url = ('http://newsapi.org/v2/everything?q=uber&from=2020-05-06&to=2020-05-06&sortBy=popularity&apiKey=4ce944e3975f4c30a8f3e7ecbd542800')
response = requests.get(url)

json_file =  response.json()
#print(json_file['articles'])

title = []

for articles in json_file['articles']:
    title.append(articles['title'])

for titles in title:
    print(titles)