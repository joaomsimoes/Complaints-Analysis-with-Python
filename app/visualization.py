from wordcloud import WordCloud
from collections import Counter
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt


def display_topics(model, features, no_top_words=5):
    for topic, word_vector in enumerate(model.components_):
        largest = word_vector.argsort()[::-1]
        st.subheader('\nTopic {}'.format(topic))
        for i in range(0, no_top_words):
            st.text('{}'.format(features[largest[i]]))


def word_cloud(word_freq, title=None, max_words=200):
    wc = WordCloud(width=1000, height=500, background_color='white', colormap='bone',
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


def time_series(brand=None):
    brand['year-month'] = brand['data'].dt.strftime('%Y-%m')
    timeseries = brand.groupby('year-month', as_index=False).size()
    fig = px.line(timeseries, x="year-month", y='size', labels={'year-month': 'Ano-mês', 'size': 'Total'}, )

    st.write(fig)
