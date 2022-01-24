from app.preprocessing import *
from app.visualization import *
from app.sql_conn import *
import datetime

first_date = datetime.date(2013, 1, 1)
today = datetime.date.today()


def app():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Intro
    st.title(':closed_book: :face_palm:')
    st.title('Portal da Queixa - Análise das Marcas')
    st.write('Para esta app estão apenas dispiníveis algumas marcas. Com o N-Gram é '
             'possível fazer a junção de palavras.')
    st.write('Experimentem!')

    # sidebar
    st.sidebar.header('Info')
    st.sidebar.write('Olá e sejam bem vindos a este pet-project! '
                     'Decidi criar um scrapper para analisar as reclamações no Portal da Queixa. '
                    'Este projecto pode ser aplicado noutras situações de negócio. '
                    'Como por exemplo, análise de notícias, comentários numa ecommerce, emails, ... '
                    )
    st.sidebar.write('Abraço, João Simões')
    st.sidebar.info("[GitHub Repo] (https://github.com/joaomsimoes/scrapper-portaldaqueixa)")
    st.sidebar.info("[LinkedIn] (https://www.linkedin.com/in/joaomsimoes/)")

    # Options
    col1, col2 = st.columns(2)
    with col1:
        brand = st.selectbox('Escolha uma marca', (brands()))
        start_date = st.date_input('Data início', first_date)
    with col2:
        n_grams = st.selectbox('N-Gram', (1, 2))
        end_date = st.date_input('Data fim', today)

    ok = st.button('Ver análise')
    if ok:
        df = sql_df(brand)
        df['data'] = df['data'].map(date_parser, na_action='ignore')
        mask = (df['data'].dt.date > start_date) & (df['data'].dt.date <= end_date)
        df = df.loc[mask]
        with st.spinner('A carregar {} queixas... Pode demorar um minutinho! :coffee: :coffee:'
                        ' Pet projet = pequeno orçamento!'.format(len(df))):
            df = sql_df(brand)
            df['data'] = df['data'].map(date_parser, na_action='ignore')
            mask = (df['data'].dt.date > start_date) & (df['data'].dt.date <= end_date)
            df = df.loc[mask]
            stopwords = stop_words()
            tfidf, tfidf_text, vectors_text = tfidf_vect(df, column='comment', stopwords=stopwords,
                                                         min_df=1, max_df=1.0, n_gram=n_grams)

        # wordcloud
        st.header('WordCloud')
        st.write('O WordCloud é uma forma rápida de analisar as palavras mais relevantes. '
                 'Para isso, usei a fórmula TF-IDF para identificar as palavras com uma maior '
                 'importancia neste documento.')
        with st.spinner('A carregar...'):
            word_cloud(tfidf['TF-IDF'], max_words=150)
        st.text("")

        # topic finder
        st.header('Topic Finder')
        st.write('Para cada marca, poderá exisitir uma diversidade de tópicos que não estão categorizados no Portal da Queixa. '
                 'Fazer este processo manualmente poderá ser penoso. Para isso usei técnicas de unsupervised learning para encontrar os tópicos mais relevantes.')
        with st.spinner('A carregar...'):
            nmf_text_model = topic(vectors_text, n_components=4)
            display_topics(model=nmf_text_model, features=tfidf_text.get_feature_names(), no_top_words=5)
        st.text("")

        # eda
        st.header('Linha Temporal')
        st.write('Por fim, uma breve analise temporal do total das queixas mensais.')
        with st.spinner('A carregar...'):
            time_series(df)
