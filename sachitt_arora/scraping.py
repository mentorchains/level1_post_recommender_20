import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import csv
from lxml import html,etree
import pandas as pd



baseurl = "https://community.mycroft.ai/"
hreflist = []

titlelist = []
categorieslist = []
postinfolist = []
commentslist = []

def getLinks(url): 
    response = requests.get(url)
    data = response.content
    soup = BeautifulSoup(data, 'html.parser')
    alist = soup.findAll("a", {"class": "title raw-link raw-topic-link" })

    for alink in alist:
        hrefval = alink.get("href")
        hreflist.append(hrefval)


def getData(url):
    contentxpath = "//*[@id='post_1']/div/div[2]/div[2]/div"

    response = requests.get(url)
    data = response.content
    info = html.fromstring(data)
    tree = info.xpath(contentxpath)
    soup = BeautifulSoup(data, 'html.parser')

    #title
    titlehref = url.replace(baseurl, "/")
    title = soup.find("a", {"href": titlehref })
    title = title.text

    

    

    allcontent = soup.findAll("div", {"class": "post"})
    alltextinfo = []
    for i in allcontent:
        alltextinfo.append(i.text)

    #main post
    mainpostinfo = ""
    mainpostinfo += alltextinfo[0]


    #comments
   
    commentsinfo = ""
    alltextinfo.pop(0)
 
    for i in alltextinfo:
        commentsinfo += i


    #categories
    try:
        category = soup.find('span', {"class": "category-title"})
        category = category.text
    except:
        category = "None"
    
    
    
    titlelist.append(title.lower())
    categorieslist.append(category.lower())
    postinfolist.append(mainpostinfo.lower())
    commentslist.append(commentsinfo.lower())

    
    
def clearCSV():
    filename = "project.csv"

    f = open(filename, "w+")
    f.close()

def buildCSV():
    getLinks(baseurl)
    for i in hreflist:
        getData(i)

    datatable = pd.DataFrame(
    {
    'Title': titlelist,
    'Category': categorieslist,
    'Post Info': postinfolist,
    'Comments': commentslist,
    }
    )
    
    datatable.to_csv("project.csv")
