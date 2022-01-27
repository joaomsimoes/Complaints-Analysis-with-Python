import datetime
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.manifold import TSNE
import pandas as pd
import streamlit as st


def date_parser(date_string):
    """convert string portuguese dates to datetime"""

    mapping = {'janeiro': '01', 'fevereiro': '02', 'março': '03',
               'abril': '04', 'maio': '05', 'junho': '06',
               'julho': '07', 'agosto': '08', 'setembro': '09',
               'outubro': '10', 'novembro': '11', 'dezembro': '12', 'zembro': '12'}

    # Some dates are like this "9 de agosto 2018 (editada a 13 de agosto 2018)"
    # So I build a regex expression to remove the second part of the string
    date_info = re.sub("\(.*?\)", '', date_string)
    try:
        day, month_pt, year = date_info.lower().replace('de', '').split()
        month = mapping[month_pt]
        date_iso = '{}-{:02d}-{:02d}'.format(year, int(month), int(day))
        date_object = datetime.datetime.strptime(date_iso, '%Y-%m-%d')

        return date_object

    except:
        pass


nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')


def stop_words(brand):
    """download the portuguese stopwords from the nltk library"""
    # Add stopwords that are important to our context
    new_stopwords = ['tarde', 'venho', 'noite', 'dia', 'ja', 'pois', 'ser', 'ter', 'tendo', 'nao',
                     'porque', 'fiz', 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro',
                     'outubro', 'novembro', 'dezembro', 'ate', 'talvez', 'aqui', 'portanto', 'estar', 'iria', 'ia',
                     'eis', 'vem', 'ir', 'preciso', 'sido', 'acerca', 'seguinte', 'domingos', 'gostaria']
    stopwords.extend(new_stopwords)
    # Add the brand as a stopword
    stopwords.extend([brand])

    return stopwords


def tfidf_vect(df, column='comment', stopwords=None, min_df=None, max_df=None, n_gram=None):
    """use the TFIDF Vectorizer from SKlearn to create a vector matrix from our text
    Returns:
        tfidf: dataframe with tokens as index and a column with the TFIDF value
        tfidf_text: the model
        vectors_text: sparse matrix
    """
    tfidf_text = TfidfVectorizer(use_idf=True, min_df=min_df, max_df=max_df,
                                 stop_words=stopwords, ngram_range=(n_gram, n_gram))
    # Fit and transform to our data
    # vectors_text is going to be used later in the NMF algorithm
    vectors_text = tfidf_text.fit_transform(df[column])
    # Create a pandas df to store the tokens and the corresponding TFIDF value
    # we transpose the vectors_text to store each value in a row
    # index the tokens with get_feature_names() method
    tfidf = pd.DataFrame(vectors_text[0].T.todense(), index=tfidf_text.get_feature_names(), columns=["TF-IDF"])
    # Sort from the more important to least important
    tfidf = tfidf.sort_values('TF-IDF', ascending=False)

    return tfidf, tfidf_text, vectors_text


@st.cache
def topic(vectors_text=None, n_components=4):
    """Finds 4 topics with the NMF algorithm
    Returns:
         nmf_text_model: object referring to NMF
        w_text_matrix: topics as columns and documents as rows
    """
    # Initiate our NMF model, the number of components is arbitrary, but it is possible to find the best balance
    # with "w_text_matrix.sum(axis=0)/w_text_matrix.sum()*100.0". For this project I simplified to 4 topics
    nmf_text_model = NMF(n_components=n_components, random_state=42)
    w_text_matrix = nmf_text_model.fit_transform(vectors_text)

    return nmf_text_model, w_text_matrix


@st.cache
def tsne_topics(w_text_matrix):
    """Dimensionality reduction with tsne
    Returns:
         tsne_embedding: df with columns x, y and hue
    """
    tsne = TSNE(random_state=42)
    tsne_embedding = tsne.fit_transform(w_text_matrix)
    tsne_embedding = pd.DataFrame(tsne_embedding, columns=['x', 'y'])
    tsne_embedding['hue'] = w_text_matrix.argmax(axis=1)
    tsne_embedding['hue'] = tsne_embedding['hue'].map({0: 'Tópico 1',
                                                       1: 'Tópico 2',
                                                       2: 'Tópico 3',
                                                       3: 'Tópico 4'})

    return tsne_embedding
