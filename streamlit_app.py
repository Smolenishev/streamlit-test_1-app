import streamlit as st

from datetime import datetime
import numpy as np
import pandas as pd
import os
# import xlsxwriter
# import openpyxl

st.title('🎈 Streamlit-test_1-app')

st.write('Hello world!')

#-----------------
st.title("Тест страница изучения Streamlit")
st.subheader("2024-11-29 12:30. Smolenishev Oleg")

now = datetime.now()

now_2 = now.strftime("%Y-%m-%d %H:%M")

st.write(now)
st.write(now_2)

st.divider()
st.subheader("Таблицы")

df = pd.DataFrame({
    'Наименование': ["Первый", "Второй"],
    'Значение': [10, 20]
})

st.table(df)

df2 = st.data_editor(df)

#st.table(df2)

st.metric(label="Количество строк таблицы: ", value=len(df))
st.metric(label="Сумма по столбцу Значение: ", value=df['Значение'].sum())

st.divider()

st.subheader("Графики")

df3 = pd.DataFrame(
    np.random.rand(10, 4),
    columns=['A', 'B', 'C', 'D']
)

st.table(df3)
st.area_chart(df3)
st.line_chart(df3)
st.scatter_chart(df3[['A', 'B']])


st.divider()
st.subheader("Слайдер")

x = st.slider("Установить значениеЖ ", 1, 10)
st.write("Установлено значение: ", x)


st.divider()
st.subheader("Разделение на столбцы")

col1, col2 = st.columns(2)

with col1:
    st.write("Столбец 1")

with col2:
    st.write("Столбец 2")


with st.sidebar:
    st.header("Slidebar")


st.divider()
st.subheader("Чтение файла xlsx")
# base1.xlsx

df3 = pd.read_excel('base1.xlsx', sheet_name='base')

st.table(df3.head(2))



