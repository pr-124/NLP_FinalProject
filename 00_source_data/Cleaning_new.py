import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.corpus import stopwords
import warnings
import nltk
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
import html
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from textblob import TextBlob
#read data 
train_data =pd.read_parquet('/Users/pr158admin/Desktop/NLP/Project/NLP_FinalProject/00_source_data/train-00000-of-00001.parquet')
test_data =pd.read_parquet('/Users/pr158admin/Desktop/NLP/Project/NLP_FinalProject/00_source_data/test-00000-of-00001.parquet')


def clean_data(tweets_df, remove_stopwords=False):
    """Clean the data by removing URLs, converting to lowercase and removing @s and #s from the tweet"""
    tweets_df['text_new']=tweets_df['text'].astype('str')
    warnings.filterwarnings("ignore")

    #replace nan with empty string
    tweets_df["text_new"] = tweets_df["text_new"].fillna('')

    # remove all URLs from the text
    tweets_df["text_new"] = tweets_df["text_new"].str.replace(r"http\S+", "")

    # remove all mentions from the text and replace with generic flag
    tweets_df["text_new"] = tweets_df["text_new"].str.replace(r"@\S+", "")

    # remove all hashtags from the text
    tweets_df["text_new"] = tweets_df["text_new"].str.replace(r"#", "")

    # lowercase all text
    tweets_df["text_new"] = tweets_df["text_new"].str.lower()
    
    #remove punctuations, numbers and words with length of two characters
    string1 = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    def remove_punct(text):
        text  = "".join([char for char in text if char not in string1])
        text = re.sub('[0-9]+', '', text)
        text= re.sub(r'\b\w{1,2}\b', '', text)
        return text
    tweets_df["text_new"] = tweets_df["text_new"].apply(lambda x: remove_punct(x))

    # removing word lengths less than 3 
    #tweets_df.text_new.str.replace(r'\b(\w{1,3})\b', '')

    #tweets_df.text_new.apply(lambda txt: ''.join(TextBlob(txt).correct()))

    

    if remove_stopwords:
        # remove stopwords
        nltk.download("stopwords")
        stop_words = set(stopwords.words("english"))
        tweets_df["text_new"] = tweets_df["text_new"].apply(
            lambda x: " ".join([word for word in x.split() if word not in stop_words])
        )

    
    # checking for uncommon words
    fdist = FreqDist(tweets_df["text_new"])
    tweets_df["uncommon"] = tweets_df["text_new"].apply(lambda x: ' '.join([item for item in x if fdist[item] >= 1 ]))
    assert (tweets_df["uncommon"]=="").all()
    #tokenisation
    tweets_df["text_new"].apply(word_tokenize)
    tweets_df["text_new"] = tweets_df["text_new"].str.split()




    return tweets_df



cleaned_train = clean_data(train_data,remove_stopwords=True)
cleaned_test = clean_data(test_data,remove_stopwords=True)


#stemming 


ps = nltk.PorterStemmer()
def stemming(text):
    text = [ps.stem(word) for word in text]
    return text

cleaned_train["text_new"] = cleaned_train["text_new"].apply(lambda x: stemming(x))

cleaned_test["text_new"] = cleaned_test["text_new"].apply(lambda x: stemming(x))



#lemmetisation 

wn = nltk.WordNetLemmatizer()

def lemmatizer(text):
    text = [wn.lemmatize(word) for word in text]
    return text
cleaned_train['text_new'] = cleaned_train['text_new'].apply(lambda x: lemmatizer(x))
cleaned_test['text_new'] = cleaned_test['text_new'].apply(lambda x: lemmatizer(x))

cleaned_train=cleaned_train.drop(['date','id','username','text','uncommon'], axis=1)
cleaned_test=cleaned_test.drop(['date','id','username','text','uncommon'], axis=1)

cleaned_train.to_csv('cleaned_train.csv', index=False)
cleaned_test.to_csv('cleaned_test.csv', index=False)

