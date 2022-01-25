from wordcloud import WordCloud
from collections import Counter
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def display_topics(model, features, no_top_words=5):
    dicts = {}
    new_list = []
    
    for topic, word_vector in enumerate(model.components_):
        largest = word_vector.argsort()[::-1]
        dicts["Tópico " + str(topic+1)] = new_list
        
        for i in range(0, 5):
          new_list.append(features[largest[i]])
          if i == 4:
            new_list = []
    
    df_topicos = pd.DataFrame.from_dict(dicts)
    st.table(df_topicos)


def visualize_topics(tsne_embedding, df):
    years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

    year = st.select_slider('Escolha uma ano', options=years, value=2021, key="year")

    data = tsne_embedding.loc[df['year'] <= year]
    fig = px.scatter(data, x='x', y='y', color='hue',
                     title=f"Queixas até {year}")
    st.write(fig)


def word_cloud(word_freq, title=None, max_words=200):
    wc = WordCloud(width=600, height=300, background_color='white', colormap='bone',
                   max_font_size=300, max_words=max_words, relative_scaling=1)

    # convert df to dict
    counter = Counter(word_freq.fillna(0).to_dict())

    wc.generate_from_frequencies(counter)

    plt.figure(figsize=(15, 7))
    plt.title(title)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')

    st.pyplot()


def describe(brand=None):
    brand['length'] = brand['comment'].str.len()
    st.dataframe(brand.describe().T)


def time_series(brand=None, start=None, end=None):
    brand['year-month'] = brand['data'].dt.strftime('%Y-%m')
    timeseries = brand.groupby('year-month', as_index=False).size()
    fig = px.line(timeseries, x="year-month", y='size', labels={'year-month': 'Ano-mês', 'size': 'Total'}, )

    st.write(fig)
