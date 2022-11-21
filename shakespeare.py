from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import glob, nltk, os, re
from nltk.corpus import stopwords
nltk.download('stopwords')
import nltk
nltk.download('punkt')
import altair as alt
import string


st.write('# Analyzing Shakespeare texts')

st.sidebar.header('Word Cloud Settings')
max_word = st.sidebar.slider('Max Words',10,200,100,10)
max_font = st.sidebar.slider('Size of Largest Word',50,350,60)
image_size = st.sidebar.slider('Image Width',100,800,400,10)
random = st.sidebar.slider('Random State',30,100,42)
remove_sw = st.sidebar.checkbox('Remove Stop Words?')

st.sidebar.header("Word Count Settings")
min_word = st.sidebar.slider('Minimum count of words',5,100,40,5)

# Creating a dictionary not a list 
books = {" ":" ","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice":"data/merchant.txt","Romeo and Juliet":"data/romeo.txt"}
selected_book = st.selectbox('Choose a txt file', books.keys())
image = books.get(selected_book)

stopword=[]

if image != " ":
    raw_text = open(image,"r").read().lower()
    
    #Remove punctuation
    clean_text = raw_text.translate(str.maketrans('','', string.punctuation))

    #Tokenize the dataset
    tokens = nltk.word_tokenize(clean_text)

    if remove_sw == True:
        stopword = set(STOPWORDS)
        stopword.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
        'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
        'put', 'seem', 'asked', 'made', 'half', 'much',
        'certainly', 'might', 'came'])

        tokens = [w for w in tokens if not w.lower() in stopword] 


    frequency = nltk.FreqDist(tokens)
    freq_df = pd.DataFrame(frequency.items(),columns=['word','count'])

    freq_df_mod = freq_df[freq_df['count'] > min_word]


tab1, tab2, tab3 = st.tabs(['Word Cloud','Bar Chart','View Text'])

with tab1:
    if image != " ":
        cloud = WordCloud(background_color = "white", 
                            max_words = max_word, 
                            max_font_size=max_font, 
                            stopwords = stopword, 
                            random_state=random)
        wc = cloud.generate(raw_text)
        word_cloud = cloud.to_file("wordcloud.png")
        st.image(wc.to_array(), width=image_size)

with tab2:
    if image != " ":
        bar = alt.Chart(freq_df_mod).mark_bar().encode(
        x=alt.X("count:Q", title="count"),
        y=alt.Y('word:N', sort = alt.EncodingSortField(field="count", op="sum", order="descending")),
        )
        

        text = bar.mark_text(
        align='left',
        baseline='middle',
        dx=3,
        color='white'
        ).encode(
        text='count'
        )
        
        st.altair_chart(bar + text, use_container_width=True)


with tab3:
    if image != " ":
        #Read the raw text, no formating/lowercasing
        raw = open(image, "r").read()
        st.write(raw)



