from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd


def count_vect(df, column='comment', stopwords=None, min_df=None, max_df=None, n_gram=None):
    count_vectorizer = CountVectorizer(min_df=min_df, max_df=max_df,
                                 stop_words=stopwords, ngram_range=(n_gram, n_gram))
    count_vectors = count_vectorizer.fit_transform(df[column])
    df = pd.DataFrame(count_vectors[0].T.todense(), index=count_vectorizer.get_feature_names(), columns=["TF-IDF"])
    df = df.sort_values('TF-IDF', ascending=False)

    return df, count_vectorizer, count_vectors


def topic(vectors_text=None, n_components=3):
    lda_text_model = LatentDirichletAllocation(n_components=n_components, random_state=42)
    w_text_matrix = lda_text_model.fit_transform(vectors_text)
    h_text_matrix = lda_text_model.components_

    print(w_text_matrix.sum(axis=0)/w_text_matrix.sum()*100)

    return lda_text_model
