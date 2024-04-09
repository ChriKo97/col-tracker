import os

import helper
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

timeframe = st.radio(
    label="timeframe",
    options=[
        "All",
        "Custom"],
    horizontal=True)

min_max_dates = pd.read_sql("SELECT MIN(date), max(date) FROM col", engine)
min_date = min_max_dates.loc[0, "min"]
max_date = min_max_dates.loc[0, "max"]

if timeframe == "Custom":
    lcol, rcol = st.columns(2)

    with lcol:
        start_date = st.date_input(
            label="Start date",
            value=min_date,
            min_value=min_date)

    with rcol:
        end_date = st.date_input(
            label="End date",
            value=max_date,
            min_value=start_date)

    sql = f"""
        SELECT
            *
        FROM
            col
        WHERE
            date >= '{start_date}'
        AND
            date <= '{end_date}'
    """
    orig_df = pd.read_sql(sql, engine)

elif timeframe == "All":
    orig_df = pd.read_sql("SELECT * FROM col", engine)

orig_df = helper.clean_data(orig_df)

_map = helper.create_mapping(orig_df)

orig_df = helper.resample_data(orig_df, _map)

orig_df = helper.add_date_infos(orig_df)


overall_tab, cat_tab, store_tab, article_tab = st.tabs(
    ["Overall", "By category", "By store", "By article"])

with overall_tab:

    overall.cumulative_costs(orig_df)

    overall.average_costs(orig_df)

    overall.total_costs(orig_df)

    overall.costs_over_time(orig_df)

with cat_tab:

    cat = category.select_category(orig_df)

    cat_df = category.filter_df(orig_df, cat)

    category.cost_per_month(cat_df)

    category.cost_per_item(cat_df)

    category.unncessary_spent(cat_df)

    category.cost_per_store(cat_df)
