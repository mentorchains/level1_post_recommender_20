from bs4 import BeautifulSoup
import urllib.request
import requests

### scraping  ###
url = "https://sellercentral.amazon.com/forums/"
html = requests.get(url)
soup = BeautifulSoup(html.text,'html.parser')
t1 = soup.find_all('a')

href_list = []
for t2 in t1:
  t3 = t2.get('href')
  href_list.append(t3)
print(href_list)

original="https://sellercentral.amazon.com"
# complete URL
def geturl(incompletelist,completelist):
  original="https://sellercentral.amazon.com"
  for i in range(len(incompletelist)):
    completelist.append(original+incompletelist[i])

href_list_full=[]
geturl(href_list,href_list_full)
print(href_list_full)

nameofboard=[]
for i in range(len(href_list)):
  nameofboard.append(href_list[i].rpartition('/')[-1])
# dictionary for all subcategory in amazon service forum
dictamz = dict(zip(nameofboard,href_list_full))
# print(dictamz)

url = dictamz[nameofboard[1]]
#url = "https://sellercentral.amazon.com/forums/c/selling-on-amazon"
html = requests.get(url)
soup = BeautifulSoup(html.text,'html.parser')

### failure---01 (nothing in the player)
players = [elem.text for elem in soup.find_all('td')]
players_list = soup.find_all('td')
for player in players_list:
    print(player.text)
### failure---02 (no table)
import requests
from io import StringIO
import pandas as pd
import numpy as np

url = 'https://sellercentral.amazon.com/forums/c/selling-on-amazon'
pd.read_html(url)
