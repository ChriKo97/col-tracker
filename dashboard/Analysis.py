import os

import helper
import analysis.timeframe as timeframe
import analysis.overall_figures as overall_figures
import analysis.figures as figures

import streamlit as st
import pandas as pd


db_user = os.getenv("POSTGRES_USER", "admin")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("DB_HOST", "col-database")
db_port = os.getenv("DB_PORT", 5432)

engine = helper.connect_to_database(
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port)


st.set_page_config(layout="wide")

# get min and max dates to choose timeframe from
min_date, max_date = timeframe.get_min_max_dates(engine)

if (not 'new_data_in_db' in st.session_state or st.session_state["new_data_in_db"]) and min_date and max_date:
    # choose time frame to look at
    time_frame = timeframe.display_timeframe_options(
        min_date=min_date,
        max_date=max_date)

    # get number of months for monthly mean calculations
    n_months = helper.get_n_months(
        start_date=min_date,
        end_date=max_date)

    # create SQL query for dataframe
    sql = timeframe.create_sql_query(time_frame)

    # read and clean data
    orig_df = helper.read_clean_data(sql, engine)

    overall_tab, cat_tab, store_tab, item_tab = st.tabs(
        ["Overall", "By category", "By store", "By item"])

    with overall_tab:

        overall_figures.cumulative_costs(orig_df)

        figures.time_bar_graph(orig_df, "category", "category")

        figures.grouped_bar_graph(
            df=orig_df,
            tab_name="overall",
            n_months=n_months,
            primary_grouping_col="category")

        overall_figures.unnecessary_cumulative(orig_df)

        overall_figures.costs_over_time(orig_df)

    with cat_tab:

        cat = helper.select_filter(
            orig_df=orig_df,
            filter_column="category")

        cat_df = helper.filter_df(
            orig_df=orig_df,
            filter_column="category",
            filter_selection=cat)

        figures.time_bar_graph(
            df=cat_df,
            primary_grouping_col="category")

        figures.grouped_bar_graph(
            df=cat_df,
            primary_grouping_col="item",
            n_months=n_months,
            tab_name="cat")

        figures.grouped_bar_graph(
            df=cat_df,
            primary_grouping_col="store",
            n_months=n_months,
            tab_name="cat")

        figures.grouped_bar_graph(
            df=cat_df,
            primary_grouping_col="item",
            n_months=n_months,
            unnecessary=True,
            tab_name="cat")

    with store_tab:

        store = helper.select_filter(
            orig_df=orig_df,
            filter_column="store")

        store_df = helper.filter_df(
            orig_df=orig_df,
            filter_column="store",
            filter_selection=store)

        figures.time_bar_graph(
            df=store_df,
            primary_grouping_col="store")

        figures.grouped_bar_graph(
            df=store_df,
            primary_grouping_col="item",
            n_months=n_months,
            tab_name="store")

        figures.grouped_bar_graph(
            df=store_df,
            primary_grouping_col="category",
            n_months=n_months,
            tab_name="store")

        figures.grouped_bar_graph(
            df=store_df,
            primary_grouping_col="item",
            n_months=n_months,
            unnecessary=True,
            tab_name="store")
else:
    st.write("No data to show yet!")