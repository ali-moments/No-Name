#pip install beautifulsoup4
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

notfound = True
textToSearch = 'hello world'
query = sys.argv[1].strip("\"").replace(" ","+")
url = "https://www.youtube.com/results?search_query=" + query
response = urlopen(url)
html = response.read()
soup = BeautifulSoup(html,"lxml")
for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
	if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
		found = False
		print(f"https://www.youtube.com{vid['href']}")

if found:
	print("No results found")
