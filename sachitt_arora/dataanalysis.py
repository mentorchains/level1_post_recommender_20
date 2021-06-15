import csv
from rake_nltk import Rake
import nltk
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import string
import time as time
import warnings 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def removestopwords(info):

    stopword = stopwords.words('english')
    info = ' '.join(x for x in str(info).split() if x not in stopword)
    return info


def datacleaning(df,stops):
     # removes the whitespace for Reply Comments and Leading Comment
    # cleaning and building the data table to be further used by the recommend function
    df['Leading Comment'] = df['Leading Comment'].str.replace('[{}]'.format(string.punctuation), '')
    df['Reply Comments'] = df['Reply Comments'].str.replace('[{}]'.format(string.punctuation), '')
    
    df['Leading Comment'] = df['Leading Comment'].str.replace(r'\d+','')
    df['Reply Comments'] = df['Reply Comments'].str.replace(r'\d+','')
    
    if stops == False:
        df['Reply Comments'] = df['Reply Comments'].apply(removestopwords)
        df['Leading Comment'] = df['Leading Comment'].apply(removestopwords)


    #remove most common words and least common words
        tenmostcomment = pd.Series(' '.join(df['Reply Comments']).split()).value_counts()[:10] 
        tenmostcomment = list(tenmostcomment.index)
        df['Reply Comments'] = df['Reply Comments'].apply(lambda x: " ".join(x for x in x.split() if x not in tenmostcomment))

        tenleastcomment = pd.Series(' '.join(df['Reply Comments']).split()).value_counts()[-10:]
        tenleastcomment = list(tenleastcomment.index)
        df['Reply Comments'] = df['Reply Comments'].apply(lambda x: " ".join(x for x in x.split() if x not in tenleastcomment))

        tenmost = pd.Series(' '.join(df['Leading Comment']).split()).value_counts()[:10] 
        tenmost = list(tenmost.index)
        df['Leading Comment'] = df['Leading Comment'].apply(lambda x: " ".join(x for x in x.split() if x not in tenmost))

        tenleast = pd.Series(' '.join(df['Leading Comment']).split()).value_counts()[-10:]
        tenleast = list(tenleast.index)
        df['Leading Comment'] = df['Leading Comment'].apply(lambda x: " ".join(x for x in x.split() if x not in tenleast))

     
    return df

def modifyTable(df, stops):
    df['Key Words'] = ''
    rake = Rake()
    #adding key words
    for index, row in df.iterrows():
        
        rake.extract_keywords_from_text(str(row['Reply Comments']) + str(row['Leading Comment']))   
        keywordscores = rake.get_word_degrees()  
        keylist = list(keywordscores.keys()) 
        
        df["Key Words"][index] = keylist

    #adding all of the words into sentences 
    df["All words"] = ''

    if stops == False:
        cols = ["Category", "Key Words"]
    elif stops == True:
        cols = ["Category", "Leading Comment", "Reply Comments"]

    randomlist = []
    for index, row in df.iterrows():
        words = ''

        for col in cols:
            if col == "Category" or col == "Leading Comment" or col == "Reply Comments":
                words += str(row[col]) + " "
            elif col == "Key Words":
                for i in row[col]:
                    words += i + " "
        words.strip()
        df["All words"][index] = words

    return df

def runclean():
    #fully cleaned data
    df = pd.read_csv("/Users/sachittarora/Documents/GitHub/level1_post_recommender_20/sachitt_arora/amazondata.csv")
    df = datacleaning(df, False)
    df = modifyTable(df, False)    
    df.to_csv("cleanedamazondata.csv")

def runmessy():
    #this creates it with stopwords to be used in md3
    df = pd.read_csv("/Users/sachittarora/Documents/GitHub/level1_post_recommender_20/sachitt_arora/rawdata.csv")
    df = datacleaning(df, True)
    df = modifyTable(df, True)    
    df.to_csv("semicleanamazondata.csv")


runclean()

