from app.preprocessing import *
from app.visualization import *
from app.sql_conn import *


def app():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title('Portal da Queixa - Análise das marcas')

    st.write('Com este mini pet project pretendo ')
    st.write('Experimentem!')
    col1, col2 = st.columns(2)
    with col1:
        brand = st.selectbox('Escolha uma marca', ('worten', 'meo', 'shein', 'vodafone', 'fnac'))
    with col2:
        n_grams = st.selectbox('Junção de palavras', (1, 2, 3))
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
        st.header('Word Cloud')
        st.write('O WordCloud é uma forma rápida de analisar as palavras mais relevantes. '
                 'Para isso, usei a fórmula TF-IDF para identificar as palavras mais importantes neste documento.')
        word_cloud(tfidf['TF-IDF'], max_words=150)

        # topic finder
        st.header('Topic Finder')
        st.write('Para cada marca, poderá exisitir uma diversidade de tópicos que não estão categorizados no Portal da Queixa. '
                 'Fazer este processo manualmente poderá ser penoso. Para isso usei técnicas de unsupervised learning para encontrar os tópicos mais relevantes.')
        nmf_text_model = topic(vectors_text, n_components=5)
        display_topics(model=nmf_text_model, features=tfidf_text.get_feature_names(), no_top_words=5)

        # eda
        st.header('Linha Temporal')
        st.write('Por fim, uma breve analise temporal do total das queixas diárias.')
        time_series(df)
