import sqlite3
import logging
import pandas as pd
import numpy as np
from numpy import random
import gensim
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from bs4 import BeautifulSoup

from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib 


def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"newlinechar", "", text)
    text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    text = BeautifulSoup(text, "lxml").text # HTML decoding
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(ps.stem(word) for word in text.split() if word not in STOPWORDS) # delete stopwors from text
    return text

con = sqlite3.connect('dataset.db')
cur = con.cursor()
cur.execute("SELECT parent, subreddit from parent_reply")
#cur.execute("SELECT comment, subreddit from parent_reply where (subreddit = 'depression') OR (subreddit = 'cripplingalcoholism') OR (subreddit = 'GetMotivated')")
#cur.execute("SELECT comment, subreddit from parent_reply where (subreddit = 'depression') OR (subreddit = 'cripplingalcoholism')")
row = cur.fetchone()
post = []
tag = []
my_tags = ['irritate', 'depression', 'alcoholism', 'suicude', 'abuse', 'psychotherapy']
while row is not None:
    post.append(row[0])
    tag.append(row[1])
    row = cur.fetchone()

df = pd.DataFrame(list(zip(post, tag)), columns=['post', 'tags'])
print(df['post'].apply(lambda x: len(x.split(' '))).sum())

# my_tags = ['GetMotivated', 'HealthAnxiety', 'psychotherapy', 'Anxiety', 'socialanxiety', 'depression', 'mentalhealth', 'DontPanic', 'BodyAcceptance', 'cripplingalcoholism', 'alcoholism', 'selfharm', 'SuicideWatch', 'stopdrinking', 'survivorsofabuse', 'rapecounseling', 'Psychiatry', 'OCD', 'whatsbotheringyou']

plt.figure(figsize=(10,4))
df.tags.value_counts().plot(kind='bar');

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))
ps = PorterStemmer()

df['post'] = df['post'].apply(clean_text)

df['post'].apply(lambda x: len(x.split(' '))).sum()

X = df.post
y = df.tags
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)


############################# LINEAR SUPPORT VECTOR MACHINE #############################

# ACCURACY 59%

sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
               ])
sgd.fit(X_train, y_train)

# Save the model as a pickle in a file
joblib.dump(sgd, 'models/final_model.pkl')

"""
y_pred = sgd.predict(X_test)

print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred,target_names=my_tags))

df2 = pd.read_csv('Psych_data.csv')
df2.dropna(inplace=True)

# df2['Answer'] = df2['Answer'].apply(clean_text)
# df2['Question'] = df2['Question'].apply(clean_text)

test = sgd.predict(df2['Answer'])
test = list(test)

test2 = sgd.predict(df2['Question'])
test2 = list(test2)

mismatch = 0
for i in range(len(test)):
    if test[i] != test2[i]:
        mismatch += 1

accuracy = (len(test)-mismatch)/len(test)
print(accuracy)
"""