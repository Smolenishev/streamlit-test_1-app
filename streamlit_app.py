import streamlit as st

from datetime import datetime
import numpy as np
import pandas as pd
import os
import xlsxwriter
import openpyxl

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



