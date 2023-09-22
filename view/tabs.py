import datetime
import streamlit as st


# Эта функция будет вызывать отображение погоды на день, неделю, месяц
def show_tabs(date: datetime.date):
    # Пример табов (из документации)
    tab1, tab2, tab3 = st.tabs(['На сегодня', 'На неделю', 'На месяц'])
    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
