import pandas as pd



df = pd.read_csv("/Users/sachittarora/Documents/GitHub/level1_post_recommender_20/sachitt_arora/cleanedamazondata.csv")
categories = findcategories(df)

def findcategories(df):
  categories = []
  for i in df["Category"].unique():
    categories.append(i)

  return categories

  



