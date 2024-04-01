import helper

import streamlit as st
import plotly.express as px
import pandas as pd


orig_df = helper.read_data()

orig_df = helper.clean_data(orig_df)

_map = helper.create_mapping(orig_df)

orig_df = helper.resample_data(orig_df, _map)

orig_df = helper.add_date_infos(orig_df)


st.set_page_config(layout="wide")


timeframe = st.radio(
    label="timeframe",
    options=[
        "All",
        "Custom"],
    horizontal=True)

if timeframe == "Custom":
    lcol, rcol = st.columns(2)

    with lcol:
        start_date = st.date_input(
            label="Start date",
            value=orig_df["date"].dt.date.min(),
            min_value=orig_df["date"].dt.date.min())

    with rcol:
        end_date = st.date_input(
            label="End date",
            value=orig_df["date"].dt.date.max(),
            min_value=orig_df["date"].dt.date.min())
elif timeframe == "All":
    start_date = orig_df["date"].dt.date.min()
    end_date = orig_df["date"].dt.date.max()

cond = ((orig_df["date"].dt.date >= start_date) &
        (orig_df["date"].dt.date <= end_date))
filtered_df = orig_df[cond].reset_index(drop=True)


overall, by_cat, by_store, by_article = st.tabs(
    ["Overall", "By category", "By store", "By article"])

with overall:

    # calculate sum per day and category and cumulative costs
    oa_df = filtered_df.groupby(["category", "date"], as_index=False).sum()
    oa_df["cumulative costs"] = oa_df.groupby("category")["costs"].cumsum()

    # plot cumulative costs
    st.plotly_chart(
        figure_or_data=px.line(
            data_frame=oa_df, x="date", y="cumulative costs", color="category",
            title="Cumulative cost over time"),
        use_container_width=True)

    # plot average costs per category
    oa_monthly_df = oa_df.copy()
    oa_monthly_df = oa_monthly_df.groupby(
        ["month", "category"], as_index=False).sum(numeric_only=True)
    oa_monthly_df = oa_monthly_df.groupby("category", as_index=False).mean()
    oa_monthly_df.sort_values("costs", inplace=True, ignore_index=True)
    st.plotly_chart(
        figure_or_data=px.bar(
            data_frame=oa_monthly_df, x="category", y="costs",
            title="Mean costs per month per category"),
        use_container_width=True)

    # plot costs per category
    oa_sum_df = filtered_df.groupby(
        "category", as_index=False).sum(numeric_only=True)
    oa_sum_df.sort_values("costs", inplace=True)
    st.plotly_chart(
        figure_or_data=px.bar(
            data_frame=oa_sum_df, x="category", y="costs",
            title="Cumulative costs per category"),
        use_container_width=True)

    # plot costs
    st.plotly_chart(
        figure_or_data=px.line(
            data_frame=oa_df, x="date", y="costs", color="category",
            title="Costs over time"),
        use_container_width=True)

with by_cat:

    cat = st.selectbox(
        label="Choose a category",
        options=sorted(filtered_df["category"].unique()))

    cat_df = filtered_df[filtered_df["category"] == cat]
    cat_df.sort_values("costs", inplace=True, ignore_index=True)

    # cost per month
    cat_month_df = cat_df.groupby("category").resample(
        "ME", on="date").sum(numeric_only=True)
    cat_month_df.reset_index(inplace=True)
    cat_month_fig = px.bar(
        data_frame=cat_month_df, x="date", y="costs",
        title="Cost per month over time")
    cat_month_fig.layout.xaxis.tickvals = pd.date_range(
        start=cat_month_df["date"].min(),
        end=cat_month_df["date"].max(),
        freq='ME')
    cat_month_fig.layout["xaxis_tickformat"] = "%B %Y"
    st.plotly_chart(
        figure_or_data=cat_month_fig,
        use_container_width=True)

    # cost per item
    cat_item_df = cat_df.groupby("name", as_index=False).sum(numeric_only=True)
    cat_item_df.sort_values("costs", inplace=True, ignore_index=True)
    st.plotly_chart(
        figure_or_data=px.bar(
            data_frame=cat_item_df, x="name", y="costs",
            title="Cost per item"),
        use_container_width=True)

    # unnecessary spent money for cat
    cat_un_df = cat_df[cat_df["unnecessary"]]
    cat_un_df = cat_un_df.groupby(
        "name", as_index=False).sum(numeric_only=True)
    cat_un_df.sort_values("costs", inplace=True, ignore_index=True)
    st.plotly_chart(
        figure_or_data=px.bar(
            data_frame=cat_un_df, x="name", y="costs",
            title="Unnecessary spent money by item"),
        use_container_width=True)

    # cost per store
    cat_sum_df = cat_df.groupby("where", as_index=False).sum(numeric_only=True)
    cat_sum_df = cat_sum_df[cat_sum_df["where"] != ""]
    cat_sum_df.sort_values("costs", inplace=True, ignore_index=True)
    st.plotly_chart(
        figure_or_data=px.bar(
            data_frame=cat_sum_df, x="where", y="costs",
            title="Total costs per store"),
        use_container_width=True)
