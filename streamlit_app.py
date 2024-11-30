import streamlit as st

from datetime import datetime
import numpy as np
import pandas as pd
import os
# import xlsxwriter
# import openpyxl



st.title(':blue[Демонстрация возвожностей Streamlit для базовых дашбордов на основе данных из 1С]')

st.write('Сайт автора: [otter-finance.ru](https://otter-finance.ru)')
st.subheader("2024-11-29 12:30. Smolenishev Oleg")



now = datetime.now()

now_2 = now.strftime("%Y-%m-%d %H:%M")


st.write("Текущая дата и время: ", now_2)

with st.sidebar:
    st.header("Оглавление")

st.sidebar.markdown('''
    - [Источники](#section-1)
    - [Продажи и маржа](#section-2) 
    - [Себестоимость](#section-3)
    - [Рабочий капитал](#section-4)
    ''', unsafe_allow_html=True)


st.divider()
# st.subheader("Таблицы")

# df1 = pd.DataFrame({
#     'Наименование': ["Первый", "Второй"],
#     'Значение': [10, 20]
# })

# st.table(df1)

# df2 = st.data_editor(df1)

# #st.table(df2)

# st.metric(label="Количество строк таблицы: ", value=len(df1))
# st.metric(label="Сумма по столбцу Значение: ", value=df1['Значение'].sum())

# st.divider()

# st.subheader("Графики")

# df3 = pd.DataFrame(
#     np.random.rand(10, 4),
#     columns=['A', 'B', 'C', 'D']
# )

# st.table(df3)
# st.area_chart(df3)
# st.line_chart(df3)
# st.scatter_chart(df3[['A', 'B']])


# st.divider()
# st.subheader("Слайдер")

# x = st.slider("Установить значениеЖ ", 1, 10)
# st.write("Установлено значение: ", x)


# st.divider()
# st.subheader("Разделение на столбцы")

# col1, col2 = st.columns(2)

# with col1:
#     st.write("Столбец 1")

# with col2:
#     st.write("Столбец 2")




st.divider()
st.divider()
st.subheader('Section 1')
st.header(":blue[Источники данных]")
st.subheader("Чтение файла xlsx. Источник: ДЕМО-база")
# base1.xlsx

df = pd.read_excel('base1.xlsx', sheet_name='base')

st.table(df.head(2))

st.divider()

df.rename(columns={'Дата': 'DATA', 'Счет Дт': 'SD', 'Субконто1 Дт': 'SKD1', 'Субконто2 Дт': 'SKD2', 'Субконто3 Дт': 'SKD3', 'Счет Кт': 'SK', 
        'Субконто1 Кт': 'SKK1', 'Субконто2 Кт': 'SKK2', 'Субконто3 Кт': 'SKK3', 'Сумма': 'SUMMA'}, inplace=True)

df = df[(df['SK']=='90.01.1') | (df['SD']=='90.02.1')]

df['ST'] = (df['SUMMA']/1000).round(2)
df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True)
df['Год']=pd.DatetimeIndex(df['DATA']).year.astype('object')
df['Месяц'] = pd.DatetimeIndex(df['DATA']).month.astype('object')
df['День'] = pd.DatetimeIndex(df['DATA']).day.astype('object')
df['Квартал'] = pd.DatetimeIndex(df['DATA']).quarter.astype('object')
df['YM'] = df['DATA'].dt.to_period('M')

df = df[df['Год']>=2021]

df['Статья'] = ''
df.loc[df['SK']=='90.01.1', 'Статья'] = 'Продажи'
df.loc[df['SD']=='90.02.1', 'Статья'] = 'Себестоимость'

df['Номенклатура'] = ''
df.loc[df['SK']=='90.01.1', 'Номенклатура'] = df['SKK3']
df.loc[((df['SD']=='90.02.1') & (df['SK']=='41.01')), 'Номенклатура'] = df['SKK1']
df.loc[((df['SD']=='90.02.1') & (df['SK']=='45.01')), 'Номенклатура'] = df['SKK2']

df['ДС'] = 0
df.loc[df['SK']=='90.01.1', 'ДС'] = df['ST'] /1.2
df.loc[df['SD']=='90.02.1', 'ДС'] = df['ST']*-1

df['Продажи'] = 0
df.loc[df['SK']=='90.01.1', 'Продажи'] = df['ST'] /1.2

df['Себестоимость'] = 0
df.loc[df['SD']=='90.02.1', 'Себестоимость'] = df['ST']*-1

pt00 = pd.pivot_table(df, index=['Статья'], values=['ДС'], columns=['Год'], aggfunc='sum', fill_value='', margins=False).round(2)

pt00 = pt00['ДС']

pt00 = pt00.transpose()

pt00['Марж.прибыль'] = pt00['Продажи'] + pt00['Себестоимость']

st.divider()
st.subheader('Section 2')
st.header(":blue[Продажи и маржинальный доход]")

st.subheader("Выходные таблицы и графики")

st.markdown("***Таблица продаж, себестоимости и марж.прибыли (тыс.руб.)***")
st.table(pt00)

# вот так исправляю формат числа:
pt01 = pt00.style.format(precision=1, thousands=" ", decimal=",")

st.table(pt01)

st.markdown("***График продаж, себестоимости и марж.прибыли (тыс.руб.)***")

st.bar_chart(pt00, stack=False, width=200, height=500)



# st.area_chart(pt00)
st.line_chart(pt01)


st.divider()

st.subheader("Разделение на столбцы")

col1, col2 = st.columns(2)

with col1:
    st.write("Таблица")
    st.table(pt01)

with col2:
    st.write("График")
    st.bar_chart(pt00, stack=False)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Продажи всего (млн.руб.): ",value=(pt00['Продажи'].sum()/1000).round(2))

with col2:
    st.metric("Марж.прибыль всего (млн.руб.): ",value=(pt00['Марж.прибыль'].sum()/1000).round(1))

with col3:
    st.metric("Рент-ть по марж.прибыли (%) всего: ",value=(pt00['Марж.прибыль'].sum()/(pt00['Продажи'].sum())*100).round(1))


st.divider()
st.subheader('Section 3')
st.header(":blue[Себестоимость]")

st.write("Раздел находится в разработке")


st.divider()
st.subheader('Section 4')
st.header(":blue[Рабочий капитал]")

st.write("Раздел находится в разработке")