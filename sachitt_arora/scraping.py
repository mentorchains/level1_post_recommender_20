import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import csv
from lxml import html,etree
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time



baseurl = "https://community.mycroft.ai"
hreflist = []
titlelist = []
categorieslist = []
postinfolist = []
commentslist = []
PATH = "/Users/sachittarora/Downloads/chromedriver 2"


chromeoptions=webdriver.ChromeOptions()
chromeoptions.add_argument("--headless")          
wd=webdriver.Chrome(PATH,options=chromeoptions)
wd.implicitly_wait(2)
wd.get(baseurl)


def getLinks(url): 
    
    

    for i in range(200): 
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
        

    info = wd.execute_script('return document.body.innerHTML')
    soup = BeautifulSoup(''.join(info), 'html.parser')
   
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
    
    try:
        allcontent = soup.findAll("div", {"class": "post"})
        alltextinfo = []
        for i in allcontent:
            alltextinfo.append(i.text)

        #title
        title = url.replace(baseurl, "")
        title = title[3:]
        title = title.replace("-", " ")
        ind = title.index("/")
        title = title[:ind]

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

        
    except:
        return

    
    
def clearCSV():
    filename = "project.csv"

    f = open(filename, "w+")
    f.close()

def buildCSV():
    getLinks(baseurl)
    for i in hreflist:
        print(i)
        getData(baseurl + i)

    datatable = pd.DataFrame(
    {
    'Title': titlelist,
    'Category': categorieslist,
    'Post Info': postinfolist,
    'Comments': commentslist,
    }
    )
    
    datatable.to_csv("rawdata.csv")

clearCSV()
buildCSV()


