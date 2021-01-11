
import csv
from rake_nltk import Rake
import nltk
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sachitt_arora.EDA import datacleaning, modifyTable




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
    df = pd.read_csv("/Users/sachittarora/Documents/GitHub/level1_post_recommender_20/sachitt_arora/project.csv")

    df = datacleaning(df)

    df = modifyTable(df)    

    recommendedposts = recommend(recommendtitle, df)

    print(recommendedposts)
    

run("Konnex domotica integrator")