from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib
import re
import random,time
import pandas as pd
from os import listdir

import PhantomJS_Nature
import mysql.connector
import pandas as pd

# Libraries for text preprocessing
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
#nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="akl8H_/nsjw",
  database="questionid"
)

dataset=[]

mycursor = mydb.cursor()

for year in range(1980,2000):

    mycursor.execute("select p.abstract from paper_full p where p.year='"+str(year)+"'")
    # mycursor.execute("select p.abstract from paper p where p.year='1960' and p.abstract like 'p'")
    # mycursor.execute("select p.abstract from paper p where p.year='1960' and p.abstract like '%sup>%'")
    tresultSet = mycursor.fetchall()


    def cleanhtml(raw_html):
      cleanr = re.compile('<.*?>')
      cleantext = re.sub(cleanr, '', raw_html)
      return cleantext

    abstracts = [cleanhtml(w[0]) for w in tresultSet]

    ##Creating a list of stop words and adding custom stopwords
    stop_words = set(stopwords.words("english"))


    corpus = []
    for a in abstracts:
        #Remove punctuations
        text=cleanhtml(a)

        text = re.sub('[^a-zA-Z]', ' ', a)

        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)

        ##Convert to list from string
        text = text.split()

        ##Stemming
        ps=PorterStemmer()
        #Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in
                stop_words]
        text = " ".join(text)

        corpus.append(text)


    #Word cloud
    from os import path
    from PIL import Image
    from wordcloud import *
    import matplotlib.pyplot as plt
    #% matplotlib inline
    wordcloud = WordCloud(
                            width=1200, height=600,
                              background_color='white',
                              stopwords=stop_words,
                              max_words=200,
                              # max_font_size=100,
                              random_state=42
                             ).generate(str(corpus))
    print(wordcloud)
    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
    fig.savefig(str(year)+".png", dpi=1200, bbox_inches='tight')
