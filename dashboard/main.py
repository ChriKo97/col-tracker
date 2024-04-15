import os

import helper
import sidebar
import timeframe
import overall
import category

import streamlit as st
import plotly.express as px
import pandas as pd


db_user = os.getenv("POSTGRES_USER", "admin")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("DB_NAME", "col")
db_host = os.getenv("DB_HOST", "col-database")
db_port = os.getenv("DB_PORT", 5432)


engine = helper.connect_to_database(
    user=db_user,
    password=db_password,
    name=db_name,
    host=db_host,
    port=db_port)


st.set_page_config(layout="wide")

# sidebar stuff
with st.sidebar:

    # uploading of new data
    sidebar.upload_new_file(engine)

# get min and max dates to choose timeframe from
min_date, max_date = timeframe.get_min_max_dates(engine)

# choose time frame to look at
time_frame = timeframe.display_timeframe_options(
    min_date=min_date,
    max_date=max_date)

# create SQL query for dataframe
sql = timeframe.create_sql_query(time_frame)

# read and clean data
orig_df = helper.read_clean_data(sql, engine)


overall_tab, cat_tab, store_tab, article_tab = st.tabs(
    ["Overall", "By category", "By store", "By article"])

with overall_tab:

    overall.cumulative_costs(orig_df)

    overall.average_costs(orig_df)

    overall.unnecessary_cumulative(orig_df)

    overall.costs_over_time(orig_df)

with cat_tab:

    cat = category.select_category(orig_df)

    cat_df = category.filter_df(orig_df, cat)

    category.cost_per_month(cat_df)

    category.cost_per_item(cat_df)

    category.unncessary_spent(cat_df)

    category.cost_per_store(cat_df)
