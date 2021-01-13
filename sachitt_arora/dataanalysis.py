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


def datacleaning(df):
     # removes the whitespace for comments and post info
    # cleaning and building the data table to be further used by the recommend function
    df['Post Info'] = df['Post Info'].str.replace('[{}]'.format(string.punctuation), '')
    df['Comments'] = df['Comments'].str.replace('[{}]'.format(string.punctuation), '')
    
    
    

    df['Comments'] = df['Comments'].apply(removestopwords)
    
    df['Post Info'] = df['Post Info'].apply(removestopwords)

    #remove most common words and least common words
    tenmostcomment = pd.Series(' '.join(df['Comments']).split()).value_counts()[:10] 
    tenmostcomment = list(tenmostcomment.index)
    df['Comments'] = df['Comments'].apply(lambda x: " ".join(x for x in x.split() if x not in tenmostcomment))

    tenleastcomment = pd.Series(' '.join(df['Comments']).split()).value_counts()[-10:]
    tenleastcomment = list(tenleastcomment.index)
    df['Comments'] = df['Comments'].apply(lambda x: " ".join(x for x in x.split() if x not in tenleastcomment))

    tenmost = pd.Series(' '.join(df['Post Info']).split()).value_counts()[:10] 
    tenmost = list(tenmost.index)
    df['Post Info'] = df['Post Info'].apply(lambda x: " ".join(x for x in x.split() if x not in tenmost))

    tenleast = pd.Series(' '.join(df['Post Info']).split()).value_counts()[-10:]
    tenleast = list(tenleast.index)
    df['Post Info'] = df['Post Info'].apply(lambda x: " ".join(x for x in x.split() if x not in tenleast))

     
    return df

def modifyTable(df):
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

    return df

def run():
    df = pd.read_csv("/Users/sachittarora/Documents/GitHub/level1_post_recommender_20/sachitt_arora/rawdata.csv")

    df = datacleaning(df)

    df = modifyTable(df)    

    df.to_csv("cleaneddata.csv")


run()