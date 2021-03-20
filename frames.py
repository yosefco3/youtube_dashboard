import streamlit as st
import pandas as pd
from us import abbrev_us_state, us_state_abbrev


@st.cache(persist=True)
def create_us_countries(data):
    df_countries = data["STATE"].value_counts().to_frame()
    df_countries.rename(columns={"STATE": "channels"}, inplace=True)
    df_countries["likes"] = data.groupby("STATE").mean()["likes"].round(0)
    df_countries["dislikes"] = data.groupby("STATE").mean()["dislikes"].round(0)
    df_countries["comments"] = data.groupby("STATE").mean()["comment_count"].round(0)
    df_countries["state_name"] = df_countries.index.to_series().apply(
        lambda x: abbrev_us_state[x]
    )
    return df_countries


@st.cache(persist=True)
def create_categories_table(data):
    df_categories = data["Category Name"].value_counts().to_frame()
    df_categories.rename(columns={"Category Name": "channels"}, inplace=True)
    df_categories["likes"] = data.groupby("Category Name").mean()["likes"].round(0)
    df_categories["dislikes"] = (
        data.groupby("Category Name").mean()["dislikes"].round(0)
    )
    df_categories["comments"] = (
        data.groupby("Category Name").mean()["comment_count"].round(0)
    )
    return df_categories


def categories_uploads(df_data, cat_names):
    categories = df_data[df_data["Category Name"].isin(cat_names)]
    categories["publish_time"] = pd.to_datetime(categories["publish_time"])
    categories = categories.groupby(
        ["publish_time", "Category Name"], as_index=False
    ).count()
    categories.sort_values(by="publish_time", inplace=True)
    categories["count"] = categories.iloc[:, 3]
    categories = categories.filter(["publish_time", "Category Name", "count"])
    return categories

