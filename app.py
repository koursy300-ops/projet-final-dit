import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Transactions', layout='wide')
st.title('Dashboard - Analyse des Transactions')
st.markdown('Projet Final - DIT Dakar 2026')

df = pd.read_csv('Dataset.csv')
df['TransactionStartTime'] = pd.to_datetime(df['TransactionStartTime'])
df['Hour'] = df['TransactionStartTime'].dt.hour
df['MargeBrute'] = df['Amount'] - df['Value']

st.sidebar.header('Filtres')
categories = st.sidebar.multiselect(
    'Choisir les categories :',
    options=df['ProductCategory'].unique(),
    default=df['ProductCategory'].unique()
)
canaux = st.sidebar.multiselect(
    'Choisir les canaux :',
    options=df['ChannelId'].unique(),
    default=df['ChannelId'].unique()
)

df_filtre = df[
    (df['ProductCategory'].isin(categories)) &
    (df['ChannelId'].isin(canaux))
]

col1, col2, col3 = st.columns(3)
col1.metric('Total transactions', len(df_filtre))
col2.metric('Revenu total (UGX)', f"{df_filtre['Value'].sum():,.0f}")
col3.metric('Fraudes detectees', int(df_filtre['FraudResult'].sum()))

st.subheader('Revenu total par categorie')
rev_cat = df_filtre.groupby('ProductCategory')['Value'].sum().reset_index()
fig1 = px.bar(rev_cat, x='ProductCategory', y='Value', color='Value')
st.plotly_chart(fig1, use_container_width=True)

st.subheader('Transactions par heure')
heure = df_filtre['Hour'].value_counts().sort_index().reset_index()
heure.columns = ['Heure', 'NbTransactions']
fig2 = px.line(heure, x='Heure', y='NbTransactions')
st.plotly_chart(fig2, use_container_width=True)

st.subheader('Repartition par canal')
canal = df_filtre['ChannelId'].value_counts().reset_index()
canal.columns = ['Canal', 'Count']
fig3 = px.pie(canal, names='Canal', values='Count')
st.plotly_chart(fig3, use_container_width=True)

st.subheader('Apercu des donnees filtrees')
st.dataframe(df_filtre.head(20))