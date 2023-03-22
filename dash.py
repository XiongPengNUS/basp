import pandas as pd
import numpy as np
import streamlit as st

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from wordcloud import WordCloud


def all_special_ranking():

    sp_pct = data.iloc[:, 1:10].mean().sort_values() * 100
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sp_pct.index,
        x=sp_pct,
        orientation='h'
    ))
    fig.update_layout(xaxis_title="Percentage")
    st.plotly_chart(fig, use_container_width=True)

def all_special_overlap(sp):

    subset = data.loc[data[sp]].iloc[:, 1:10]
    subset.drop(columns=[sp], inplace=True)

    sp_pct = subset.mean().sort_values() * 100
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sp_pct.index,
        x=sp_pct,
        orientation='h'
    ))
    fig.update_layout(xaxis_title="Percentage")
    st.plotly_chart(fig, use_container_width=True)

def all_prog_python(sp):

    if sp == 'All':
        subset = data
    else:
        subset = data.loc[data[sp]]
    prog_pct = subset['Programming level'].value_counts(normalize=True).sort_index() * 100
    python_pct = subset['Python level'].value_counts(normalize=True).sort_index() * 100


    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=python_pct.index,
        y=prog_pct,
        name='Programming Experience'
    ))
    fig.add_trace(go.Bar(
        x=python_pct.index,
        y=python_pct,
        name='Python Experience'
    ))
    fig.update_layout(barmode='group', 
                      yaxis_title="Percentage",
                      legend_font_family='monospace')
    st.plotly_chart(fig, use_container_width=True)

def all_use_prog(sp):

    if sp == 'All':
        subset = data
    else:
        subset = data.loc[data[sp]]
    use_pct = subset['Use programming'].value_counts(normalize=True) * 100

    # st.write(len(use_pct))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=use_pct.index,
        y=use_pct.values,
    ))
    fig.update_layout(yaxis_title="Percentage")
    st.plotly_chart(fig, use_container_width=True)


def time_special(sps):

    sp_pct = data.groupby('Semester')[sps].mean().loc[semester] * 100
    fig = go.Figure()
    for sp in sps:
        fig.add_trace(go.Bar(
            x=sp_pct.index,
            y=sp_pct[sp],
            name=f'{sp:<40}',
        ))
    fig['data'][0]['showlegend'] = True
    fig.update_layout(barmode='group', 
                      xaxis_title="Semester",
                      yaxis_title="Percentage",
                      legend_font_family='monospace')
    st.plotly_chart(fig, use_container_width=True)

def time_special_ranking(sem):

    subset = data.loc[data['Semester'] == sem]
    sp_pct = subset.iloc[:, 1:10].mean().sort_values() * 100
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sp_pct.index,
        x=sp_pct,
        orientation='h'
    ))

    fig.update_layout(xaxis_title="Percentage")
    st.plotly_chart(fig, use_container_width=True)

def time_prog_python(prof):

    prog_pct = data.groupby('Semester')['Programming level'].value_counts(normalize=True).unstack() * 100
    python_pct = data.groupby('Semester')['Python level'].value_counts(normalize=True).unstack() * 100
    prog_pct = prog_pct.iloc[:, 1+options[prof]:].sum(axis=1)
    python_pct = python_pct.iloc[:, 1+options[prof]:].sum(axis=1)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=prog_pct.index,
        y=prog_pct,
        name='Programming Experience'
    ))
    fig.add_trace(go.Bar(
        x=python_pct.index,
        y=python_pct,
        name='Python Experience'
    ))
    fig.update_layout(barmode='group', 
                      xaxis_title="Semester",
                      yaxis_title="Percentage",
                      legend_font_family='monospace')
    st.plotly_chart(fig, use_container_width=True)

def time_use_prog():

    use_pct = data.groupby('Semester')['Use programming'].value_counts(normalize=True).unstack().iloc[:, ::-1] * 100
    st.write('#### Trend of Likelihood of Using Programming')

    fig = go.Figure()
    for col in use_pct.columns:
        fig.add_trace(go.Bar(
            x=use_pct.index,
            y=use_pct[col],
            name=f'{col:<18}',
        ))
    fig.update_layout(barmode='stack', 
                      xaxis_title="Semester",
                      yaxis_title="Percentage",
                      legend_font_family='monospace')
    st.plotly_chart(fig, use_container_width=True)

def time_wordcloud(sem):

    subset = data.loc[data['Semester'] == sem]
    wordcloud = WordCloud(max_words=40, random_state=1,
                          width=1000, height=600, 
                          margin=20, 
                          colormap='Wistia',
                          background_color='black').generate(' '.join(subset['Expected title'].dropna()))
    fig = plt.figure(figsize=(6, 3))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)


# st.set_page_config(layout="wide")

st.write('## A Study on BA Specialization')
data_file = st.file_uploader("Upload Data",type=['xlsx'])
if data_file:
    data = data = pd.read_excel('survey_data.xlsx')

    st.write('---')
    st.write('#### General Information')
    st.write(f'The dataset provides the survey responses of {data.shape[0]} students.')
    
    how = st.selectbox('How to Visualize Data:', ['Overall Pattern', 'Time Trend'], index=0)
    st.write('---')

    if how == 'Overall Pattern':
        sp_labels = list(data.columns[1:10])

        st.write('#### Ranking of Specialization Preference')
        all_special_ranking()
    
        st.write('---')
        st.write('#### Overlap of Specialization Preference')
        sp = st.selectbox('Specializations', sp_labels, index=4)
        all_special_overlap(sp)

        st.write('---')
        st.write('#### Programming/Python Skills')
        options = ['All'] + sp_labels
        sp = st.selectbox('Specializations', options, index=0, key='1')
        all_prog_python(sp)

        st.write('---')
        st.write('#### Likelihood of Using Programming')
        options = ['All'] + sp_labels
        sp = st.selectbox('Specializations', options, index=0, key='2')
        all_use_prog(sp)

    elif how == 'Time Trend':
        semester = ['AY202021 Sem1', 'AY202021 Sem2', 'AY202122 Sem1', 'AY202122 Sem2']
        st.write('#### Trend of Specialization Preference')
        sps = st.multiselect('Specializations', data.columns[1:10], 
                             default=['Business Analytics'])
        time_special(sps)

        st.write('---')
        st.write('#### Trend of Specialization Ranking')
        sem = st.select_slider('Semester', options=semester, value=semester[0])
        time_special_ranking(sem)

        st.write('---')
        st.write('#### Trend of Programming/Python Skills')
        options = {'At least 2': 0, 'At least 3: Basic': 1, 'At least 4': 2, 'At least 5: Proficient': 3}
        prof = st.selectbox('Proficiency in Programming/Python Skills', options, index=3)
        time_prog_python(prof)

        st.write('---')
        time_use_prog()

        st.write('---')
        st.write(f'#### Word Cloud of Expected Job Titles')
        sem = st.selectbox('Selected Semester for Word Cloud', data['Semester'].unique(), index=0)
        time_wordcloud(sem)
