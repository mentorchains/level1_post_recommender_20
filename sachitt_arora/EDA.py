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

def datacleaning(df):
     # removes the whitespace for comments and post info
    # cleaning and building the data table to be further used by the recommend function until line 170
    df['Post Info'] = df['Post Info'].str.replace('[{}]'.format(string.punctuation), '')
    df['Comments'] = df['Comments'].str.replace('[{}]'.format(string.punctuation), '')
    
    
    stopword = stopwords.words('english')

    df['Comments'] = df['Comments'].apply(lambda x: " ".join(x for x in x.split() if x not in stopword))
    df['Post Info'] = df['Post Info'].apply(lambda x: " ".join(x for x in x.split() if x not in stopword))
     
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
