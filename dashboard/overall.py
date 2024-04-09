import pandas as pd
import plotly.express as px
import streamlit as st


def cumulative_costs(orig_df: pd.DataFrame) -> st.plotly_chart:

    df = orig_df.copy()

    # calculate sum per day and category and cumulative costs
    oa_df = df.groupby(["category", "date"], as_index=False).sum()
    oa_df["cumulative costs"] = oa_df.groupby("category")["cost"].cumsum()

    # plot cumulative costs
    st.plotly_chart(
        figure_or_data=px.line(
            data_frame=oa_df, x="date", y="cumulative costs", color="category",
            title="Cumulative cost over time"),
        use_container_width=True)

def average_costs(orig_df: pd.DataFrame) -> st.plotly_chart:

    df = orig_df.copy()

    # plot average costs per category
    df["month"] = df["date"].dt.month
    df = df.groupby(
        ["month", "category"], as_index=False).sum(numeric_only=True)
    df = df.groupby("category", as_index=False).mean()
    df.sort_values("cost", inplace=True, ignore_index=True)

    st.plotly_chart(
        figure_or_data=px.bar(
            data_frame=df, x="category", y="cost",
            title="Mean costs per month per category"),
        use_container_width=True)

def total_costs(orig_df: pd.DataFrame) -> st.plotly_chart:

    df = orig_df.copy()

    # plot costs per category
    df = df.groupby(
        "category", as_index=False).sum(numeric_only=True)
    df.sort_values("cost", inplace=True)
    st.plotly_chart(
        figure_or_data=px.bar(
            data_frame=df, x="category", y="cost",
            title="Cumulative costs per category"),
        use_container_width=True)

def costs_over_time(orig_df: pd.DataFrame) -> st.plotly_chart:

    df = orig_df.copy()

    # plot costs
    df = df.groupby(
        ["category", "date"],
        as_index=False).sum(numeric_only=True)
    st.plotly_chart(
        figure_or_data=px.line(
            data_frame=df, x="date", y="cost", color="category",
            title="Costs over time"),
        use_container_width=True)