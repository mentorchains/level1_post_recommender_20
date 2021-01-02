import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import csv
from lxml import html,etree
from rake_nltk import Rake
import nltk
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import string
import time as time
import warnings 


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


def recommend(recommendtitle, df):
    recommendations = []
    ival = 0

    count = CountVectorizer()
    countmatrix = count.fit_transform(df['All words'])
    cosinesimilarity = cosine_similarity(countmatrix, countmatrix)

    #find index of the recommend title
    for index, row in df.iterrows():
        if df["Title"][index] == recommendtitle:
            ival = index
    #use index to find the cosinesimilarity of the index
    scores = pd.Series(cosinesimilarity[ival]).sort_values(ascending = False)
    top10 = list(scores.iloc[1:11].index)  
    
    for i in top10:  
        recommendations.append(list(df['Title'])[i])

    
    return recommendations

def run(recommendtitle):
    df = pd.read_csv("project.csv")

    # removes the whitespace for comments and post info
    # cleaning and building the data table to be further used by the recommend function until line 170
    df['Post Info'] = df['Post Info'].str.replace('[{}]'.format(string.punctuation), '')
    df['Comments'] = df['Comments'].str.replace('[{}]'.format(string.punctuation), '')
    
    
    df['Key Words'] = ''
   
    rake = Rake()
    #adding key words
    for index, row in df.iterrows():
        
        rake.extract_keywords_from_text(row['Comments'] + row['Post Info'])   
        keywordscores = rake.get_word_degrees()  
        keylist = list(keywordscores.keys()) 
        
        df["Key Words"][index] = keylist

    #adding all of the words into sentences 
    df["All words"] = ''

    cols = ["Category", "Key Words"]
    randomlist = []
    for index, row in df.iterrows():
        words = ''

        for col in cols:
            if col == "Category":
                words += row[col] + " "
            elif col == "Key Words":
                for i in row[col]:
                    words += i + " "
        words.strip()
        df["All words"][index] = words

    #calling recommend function
    recommendedposts = recommend(recommendtitle, df)

    print(recommendedposts)
    

run("Konnex domotica integrator")