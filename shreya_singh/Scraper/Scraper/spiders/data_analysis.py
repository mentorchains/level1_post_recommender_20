import pandas as pd

# Importing dataset
df=pd.read_csv('dataset.csv') 

#lowercase dataset
df['comments'] = df['comments'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['comments'].head()

#remove punctuation
df['comments'] = df['comments'].str.replace('[^\w\s]','')
df['comments'].head()

#download stopwords
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('english')

#remove stopwords
df['comments'] = df['comments'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
df['comments'].head()

# lists top ten most common words 
freq = pd.Series(' '.join(df['comments']).split()).value_counts()[:10]
#print(freq)

# removes top ten most common words
df_data = df.copy()
freq = list(freq.index)
df['comments'] = df['comments'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
df['comments'].head()

#lists top ten least common words 
freq = pd.Series(' '.join(df['comments']).split()).value_counts()[-10:]
#print (freq)

#removes top ten least common words
freq = list(freq.index)
df['comments'] = df['comments'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
df['comments'].head()

#spellcheck?
from textblob import TextBlob
#df['comments'][:5].apply(lambda x: str(TextBlob(x).correct()))

#tokenization
df['comments'] = df.apply(lambda row: nltk.word_tokenize(row['comments']), axis=1)

#lemmatization 
nltk.download('wordnet')

from textblob import Word
df['comments'] = df['comments'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x]))
df['comments'].head()

print(df['comments'])

df.to_csv('cleaned.csv')