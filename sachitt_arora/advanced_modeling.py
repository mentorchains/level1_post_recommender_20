import pandas as pd
import numpy as np
from numpy import random
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

categories = ['general discussion', 'mimic', 'support', 'mycroft project', 'skill feedback', 'mark ii', 'skill suggestions', 'site feedback', 'adapt intent parser', 'languages', 'feature requests', 'machine learning', 'design', 'openstt']
global first 
first = True

def initializedf():
    global first
    
    df = pd.read_csv("/Users/sachittarora/Documents/GitHub/level1_post_recommender_20/sachitt_arora/amazondata.csv")
    df.drop(columns= ['Unnamed: 0'], inplace=True)

    # if first == True:

    #     for i in df['Category'].unique():
    #         categories.append(i)
    #     first = False

    return df

def multinomial():
    df = initializedf()
    
    x = df["All words"]
    y = df["Category"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state = 42)

    PL = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', MultinomialNB()),
              ])
    PL.fit(x_train, y_train)

    predictedy = PL.predict(x_test)

    print('accuracy %s' % accuracy_score(predictedy, y_test))
    res1 = accuracy_score(predictedy, y_test)
    print(classification_report(y_test, predictedy,target_names=categories))
    return res1

def sgdclassifier():
    df = initializedf()
    x = df["All words"]
    y = df["Category"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state = 42)

    PL = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
               ])

    PL.fit(x_train, y_train)

    predictedy = PL.predict(x_test)

    print('accuracy %s' % accuracy_score(predictedy, y_test))
    res2 = accuracy_score(predictedy, y_test)
    print(classification_report(y_test, predictedy,target_names=categories))
    return res2

def linearregression():
    df = initializedf()
    x = df["All words"]
    y = df["Category"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state = 42)

    PL = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', LogisticRegression(n_jobs=1, C=1e5)),
               ])
    PL.fit(x_train, y_train)

    predictedy = PL.predict(x_test)

    print('accuracy %s' % accuracy_score(predictedy, y_test))
    res3 = accuracy_score(predictedy, y_test)
    print(classification_report(y_test, predictedy,target_names=categories))
    return res3


def decisiontree():
    df = initializedf()
    x = df["All words"]
    y = df["Category"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state = 42)

    PL = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', DecisionTreeClassifier(random_state=0)),
               ])

    PL.fit(x_train, y_train)

    predictedy = PL.predict(x_test)

    print('accuracy %s' % accuracy_score(predictedy, y_test))
    res4 = accuracy_score(predictedy, y_test)
    print(classification_report(y_test, predictedy,target_names=categories))
    return res4



def findresults():
    res1 = multinomial()
    res2 = sgdclassifier()
    res3 = linearregression()
    res4 = decisiontree()

    res = pd.DataFrame({'Model': ['Naive Bayes MultinomialNB', 'Linear SVM', 'Logistic Regression', 'Decision Tree'],
                         'Accuracy': [res1, res2, res3, res4]})

    res.set_index('Model')
    res.sort_values(by='Accuracy')

    print(res)



def crossval():
    df = initializedf()
    x = df["All words"]
    y = df["Category"]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state = 42)

    PL = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', DecisionTreeClassifier(random_state=0)),
               ])
    cv_res = cross_val_score(PL, x_train, y_train, cv=10)
    mean_PL = np.mean(cv_res)
    print(mean_PL)



findresults()
#best accuracy 89% with decisiontree pipeline