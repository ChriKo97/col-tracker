import os

import helper
import analysis.timeframe as timeframe
import analysis.overall as overall
import analysis.category as category

import streamlit as st

from dotenv import load_dotenv
load_dotenv()

db_host = os.getenv("DB_HOST", "col-database")
db_port = os.getenv("DB_PORT", 5432)
db_name = os.getenv("DB_NAME", "col")
db_user = os.getenv("POSTGRES_USER", "admin")
db_password = os.getenv("POSTGRES_PASSWORD")

engine = helper.connect_to_database(
    user=db_user,
    password=db_password,
    name=db_name,
    host=db_host,
    port=db_port)


st.set_page_config(layout="wide")

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