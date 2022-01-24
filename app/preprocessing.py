import datetime
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import pandas as pd
import spacy

nlp = spacy.load('pt_core_news_sm', disable=['parser', 'ner'])


def date_parser(date_string):
    """convert dates have convert """

    mapping = {'janeiro': '01', 'fevereiro': '02', 'março': '03',
               'abril': '04', 'maio': '05', 'junho': '06',
               'julho': '07', 'agosto': '08', 'setembro': '09',
               'outubro': '10', 'novembro': '11', 'dezembro': '12', 'zembro': '12'}

    date_info = re.sub("\(.*?\)", '', date_string)
    date_info = date_info.lower().replace('de', '').split()
    try:
        day, month_pt, year = date_info
        month = mapping[month_pt]
        date_iso = '{}-{:02d}-{:02d}'.format(year, int(month), int(day))
        date_object = datetime.datetime.strptime(date_iso, '%Y-%m-%d')

        return date_object

    except:
        pass


nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

def stop_words():
    """download the portuguese stopwords from the nltk library"""

    new_stopwords = ['tarde', 'venho', 'noite', 'dia', 'ja', 'pois', 'ser', 'ter', 'tendo', 'nao',
                     'porque', 'fiz', 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro',
                     'outubro', 'novembro', 'dezembro', 'ate', 'talvez', 'aqui', 'portanto', 'estar', 'iria', 'ia',
                     'eis', 'vem', 'ir', 'preciso', 'sido', 'acerca', 'seguinte', 'domingos', ]
    stopwords.extend(new_stopwords)

    return stopwords


def lemma(text):
    doc = nlp(text)
    result = " ".join([token.lemma_ for token in doc])

    return result


def preprocessing(df=None):
    """text preprocessing"""
    df['comment'] = df['comment'].apply(lemma)
    df['comment'] = df['comment'].apply(lambda token: [word for word in token if word.isalpha()])
    df['comment'] = df['comment'].apply(str)

    return df


def tfidf_vect(df, column='comment', stopwords=None, min_df=None, max_df=None, n_gram=None):
    tfidf_text = TfidfVectorizer(use_idf=True, min_df=min_df, max_df=max_df,
                                 stop_words=stopwords, ngram_range=(n_gram, n_gram))
    vectors_text = tfidf_text.fit_transform(df[column])
    tfidf = pd.DataFrame(vectors_text[0].T.todense(), index=tfidf_text.get_feature_names(), columns=["TF-IDF"])
    tfidf = tfidf.sort_values('TF-IDF', ascending=False)

    return tfidf, tfidf_text, vectors_text


def topic(vectors_text=None, n_components=3):
    nmf_text_model = NMF(n_components=n_components, random_state=42)
    w_text_matrix = nmf_text_model.fit_transform(vectors_text)
    h_text_matrix = nmf_text_model.components_

    print(w_text_matrix.sum(axis=0)/w_text_matrix.sum()*100)

    return nmf_text_model
