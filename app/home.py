from preprocessing import *
from visualization import *
from sql_conn import *


def home():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title('Analise queixas')

    st.write('We need some information to predict the car price')
    col1, col2 = st.columns(2)
    with col1:
        brand = st.selectbox('Escolha uma marca', ('worten', 'meo', 'shein'))
    with col2:
        n_grams = st.selectbox('N-Grams', (1, 2, 3))
    count_result = count_queixas(brand)

    ok = st.button('Ver análise')
    if ok:
        with st.spinner('A carregar {} queixas... Pode demorar um minutinho! :coffee: :coffee:'
                        ' Pet projet = pequeno orçamento!'.format(count_result[0])):
            df = sql_df(brand)
            df['data'] = df['data'].map(date_parser, na_action='ignore')
            stopwords = stop_words()
            tfidf, tfidf_text, vectors_text = tfidf_vect(df, column='comment', stopwords=stopwords,
                                                         min_df=1, max_df=1.0, n_gram=n_grams)

        # wordcloud
        st.title('Word Cloud')
        word_cloud(tfidf['TF-IDF'], max_words=150)

        # topic finder
        st.title('Topic finder')
        nmf_text_model = topic(vectors_text, n_components=5)
        display_topics(model=nmf_text_model, features=tfidf_text.get_feature_names(), no_top_words=5)

        # eda
        st.title('EDA')
        time_series(df)
