import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
import datetime

from frames import create_us_countries, create_categories_table, categories_uploads
from create_plot_func import create_countries_plot, create_category_plot

dir_path = os.path.dirname(os.path.realpath(__file__))

DATA_URL = os.path.join(dir_path, "YoutubeDataCleaned_2.csv")

st.title("Analysis of Youtube data")

st.sidebar.title("Yosef Cohen Project, Udacity Business Analyst Program")


@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data["trending_date"] = pd.to_datetime(data["trending_date"])
    data["publish_time"] = pd.to_datetime(data["publish_time"])
    return data


data = load_data()
st.sidebar.markdown("### Youtube data by state:")
select = st.sidebar.selectbox(
    "Features By State:", ["Channels", "Likes", "Dislikes", "Comments"], key="1"
)

df_countries = create_us_countries(data)

if not st.sidebar.checkbox("Hide", True, key=2):
    st.markdown("### States Features:")
    if select == "Channels":
        fig = create_countries_plot(
            df_countries, "channels", "Youtube channels by state"
        )
    elif select == "Likes":
        fig = create_countries_plot(df_countries, "likes", "Youtube likes by state")
    elif select == "Dislikes":
        fig = create_countries_plot(
            df_countries, "dislikes", "Youtube dislikes by state"
        )
    elif select == "Comments":
        fig = create_countries_plot(
            df_countries, "comments", "Youtube comments by state"
        )
    st.plotly_chart(fig)


st.sidebar.markdown("### Youtube data by categories:")
select = st.sidebar.selectbox(
    "Features By Categories:", ["Channels", "Likes", "Dislikes", "Comments"], key="2"
)

df_categories = create_categories_table(data)
# st.write(df_categories)

if not st.sidebar.checkbox("Hide", True, key=3):
    st.markdown("### Categories Features:")
    if select == "Channels":
        fig = create_category_plot(df_categories, "channels", "Channels per category")
    elif select == "Likes":
        fig = create_category_plot(df_categories, "likes", "Likes per category")
    elif select == "Dislikes":
        fig = create_category_plot(df_categories, "dislikes", "Dislikes per category")
    elif select == "Comments":
        fig = create_category_plot(df_categories, "comments", "Comments per category")
    st.plotly_chart(fig)


categories_names = df_categories.index

st.sidebar.subheader("Comparing categories By Time")
choice = st.sidebar.multiselect("Pick category/categories", categories_names)


if len(choice) > 0:
    categories = categories_uploads(data, choice)
    date_b = categories["publish_time"].min()
    date_e = categories["publish_time"].max()
    start_date = st.date_input("Start date", date_b)
    end_date = st.date_input("End date", date_e)
    if st.button("Plot lines"):
        if start_date < end_date:
            categories = categories[
                (categories["publish_time"] > date_b)
                & (categories["publish_time"] < date_e)
            ]
            st.success("Start date: `%s`\n\nEnd date:`%s`" % (start_date, end_date))
            # st.write(categories)
            fig = px.line(
                categories,
                x="publish_time",
                y="count",
                color="Category Name",
                width=800,
                height=600,
                title="Uploads vs Publish Time",
            )
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig)
        else:
            st.error("Error: End date must fall after start date.")


st.sidebar.header("Word Cloud")
if not st.sidebar.checkbox("Close", True, key="3"):
    st.subheader("Word cloud for tags")
    df = pd.read_csv("df_tags_clean.csv")
    s = df["Value"].value_counts().drop("[none]")
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=s)

    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot(plt)
