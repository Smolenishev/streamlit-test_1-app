import streamlit as st

from datetime import datetime
import numpy as np
import pandas as pd
import os


st.set_page_config(page_title="Smolenishev / otter-finance.ru", layout="wide")

st.title(':blue[Презентация функционала Streamlit для создания простых информационных панелей на основе данных из 1С]')

st.subheader('Сайт автора: [otter-finance.ru](https://otter-finance.ru)')




now = datetime.now()

now_2 = now.strftime("%Y-%m-%d %H:%M")


st.write("Текущая дата и время: ", now_2)

with st.sidebar:
    st.header("Оглавление")

st.sidebar.markdown('''
    - [Источники](#section-1)
    - [Продажи и маржа](#section-2) 
    - [Анализ продаж по покупателям](#section-3)
    - [Анализ продаж по номенклатуре](#section-4)
    ''', unsafe_allow_html=True)


#---------------------------------------------------
st.divider()
st.subheader('Section 1')
st.header(":blue[Источники данных]")
st.subheader("Чтение файла xlsx с выгруженными бух. транзакциями из 1С")
st.write("файл xlsx: 4,9 Mb, 42 тыс.строк - загружается примерно 30 сек.")


#--------- начало блока подготовки данных ---------------

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

# по годам
pt0 = pd.pivot_table(df, index=['Статья'], values=['ДС'], columns=['Год'], aggfunc='sum', fill_value='', margins=False).round(2)
pt0 = pt0['ДС']
pt0 = pt0.transpose()
pt0['Марж.прибыль'] = pt0['Продажи'] + pt0['Себестоимость']

# вот так исправляю формат числа:
pt00 = pt0.style.format(precision=1, thousands=" ", decimal=",")

# по годоам и месяцам
# pt1 = pd.pivot_table(df, index=['Статья'], values=['ДС'], columns=['Год', 'Месяц'], aggfunc='sum', fill_value='', margins=False).round(2)
pt1 = pd.pivot_table(df, index=['Статья'], values=['ДС'], columns=['YM'], aggfunc='sum', fill_value='', margins=False).round(2)
pt1 = pt1['ДС']
pt1 = pt1.transpose()
pt1['Марж.прибыль'] = pt1['Продажи'] + pt1['Себестоимость']
pt1['Маржа_%'] = (pt1['Марж.прибыль']/pt1['Продажи'])*100

# st.dataframe(pt1.loc[:, "Маржа_%"])



# вот так исправляю формат числа:
pt01 = pt1.style.format(precision=1, thousands=" ", decimal=",")

# для метрик в отдельных квадратах:
sales = (pt0.loc[:,'Продажи'].sum()/1000).round(2)
marg = (pt0['Марж.прибыль'].sum()/1000).round(1)
marg_pr = (pt0['Марж.прибыль'].sum()/(pt0['Продажи'].sum())*100).round(1)

# для продаж по месяцам
df90 = df[df['SK']=='90.01.1']
pt90_1 = pd.pivot_table(df90, index=['YM'], values=['ДС'], aggfunc='sum', fill_value=0, margins=False)/1000
pt90_1.reset_index(inplace=True)
pt90_1['YM'] = pt90_1['YM'].astype('str')

# для маржи по месяцам
pt90_m = pt1[['Маржа_%']]
pt90_m.reset_index(inplace=True)
pt90_m['YM'] = pt90_m['YM'].astype('str')

# для продаж по покупателям

pt90_p = pd.pivot_table(df90, index=['SKD1'], values=['ДС'], columns= ['Год'], aggfunc='sum', fill_value=0, margins=True)/1000
pt90_p = pt90_p['ДС']
pt90_p.sort_values(by='All', ascending=False, inplace=True)
pt90_p = pt90_p.style.format(precision=1, thousands=" ", decimal=",")

# для продаж по номенклатуре

pt90_n = pd.pivot_table(df90, index=['SKK3'], values=['ДС'], columns= ['Год'], aggfunc='sum', fill_value=0, margins=True)/1000
pt90_n = pt90_n['ДС']
pt90_n.sort_values(by='All', ascending=False, inplace=True)
pt90_n = pt90_n.style.format(precision=1, thousands=" ", decimal=",")

#--------- окочание блока подготовки данных ---------------



#---------------------------------------------------
st.divider()
st.subheader('Section 2')
st.header(":blue[Продажи и маржинальный доход]")

st.divider()


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Продажи всего (млн.руб.): ",value=sales, delta='-Снижаются')
    

with col2:
    st.metric("Марж.прибыль всего (млн.руб.): ",value=marg)
    

with col3:
    st.metric("Рент-ть по марж.прибыли (%) всего: ",value=marg_pr)
    



col1, col2 = st.columns(2)
with col1:
    st.markdown("***Таблица продаж, себестоимости и марж.прибыли (тыс.руб.)***")
    st.table(pt00)

with col2:
    st.markdown("***График продаж, себестоимости и марж.прибыли (тыс.руб.)***")
    st.bar_chart(pt00, y_label="тыс.руб.", stack=False, width=200, height=600)

st.divider()
st.subheader("Данные по годам и месяцам:")
# st.dataframe(pt01)
st.write("График продаж (млн.руб.)")
st.bar_chart(pt90_1, x="YM", y="ДС", y_label="млн.руб.", stack=False) # , width=800, height=600

st.write("График рентабельности по марж. прибыли (%)")
st.area_chart(pt90_m, x="YM", y="Маржа_%", y_label="%", color="#FF0000")

st.write("Таблица продаж, марж.прибыли (тыс.руб.) и рентабельности (%)")
st.table(pt01)




#-------------------------------------------
st.divider()
st.subheader('Section 3')
st.header(":blue[Анализ продаж по покупателям]")
st.write("Таблица продаж по покупателям (млн.руб.). Сортировка по убыванию:")
st.table(pt90_p)



#-------------------------------------------
st.divider()
st.subheader('Section 4')
st.header(":blue[Анализ продаж по номенклатуре]")
st.write("Таблица продаж по номенклатуре (млн.руб.). Сортировка по убыванию:")
st.table(pt90_n)




st.write('''
        Log:\n
        2024-11-29 12:30 start \n
        2024-11-30 18:00 Git - GitHub - Streamlit.io \n
        2024-12-01 15:20 development and evolution \n
        2024-12-02 22:50 add graph month, tabl customer \n
        Smolenishev Oleg
        ''')