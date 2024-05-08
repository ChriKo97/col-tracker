import pandas as pd
import streamlit as st
import plotly.express as px

def select_category(orig_df: pd.DataFrame):

    df = orig_df.copy()

    cat = st.selectbox(
        label="Choose a category",
        options=sorted(df["category"].unique()))

    return cat


def filter_df(orig_df: pd.DataFrame, cat:str):

    df = orig_df[orig_df["category"] == cat].copy()

    return df.sort_values("cost", ignore_index=True)

def cost_per_month(cat_df: pd.DataFrame):

    df = cat_df.copy()

    df = df.groupby("category").resample(
        "ME", on="date").sum(numeric_only=True)
    df.reset_index(inplace=True)
    cat_month_fig = px.bar(
        data_frame=df, x="date", y="cost",
        title="Cost per month over time")
    cat_month_fig.layout.xaxis.tickvals = pd.date_range(
        start=df["date"].min(),
        end=df["date"].max(),
        freq='ME')
    cat_month_fig.layout["xaxis_tickformat"] = "%B %Y"
    st.plotly_chart(
        figure_or_data=cat_month_fig,
        use_container_width=True)

def cost_per_item(cat_df: pd.DataFrame):

    df = cat_df.copy()

    # selection for total or monthly mean
    total_monthly = st.radio(
        label="", key="total_or_monthly_mean",
        options=["Total", "Monthly mean"],
        horizontal=True)

    # total fig
    total_df = df.groupby("item", as_index=False).sum(numeric_only=True)
    total_df.sort_values("cost", inplace=True, ignore_index=True)
    total_fig = px.bar(
        data_frame=total_df, x="item", y="cost",
        title="Total cost per item")

    # monthly mean fig
    monthly_df = df.groupby(["item", "month"], as_index=False).sum(numeric_only=True)
    monthly_df = monthly_df.groupby("item", as_index=False).mean(numeric_only=False)
    monthly_df.sort_values("cost", inplace=True, ignore_index=True)
    monthly_fig = px.bar(
        data_frame=monthly_df, x="item", y="cost",
        title="Mean monthly cost per item")

    if total_monthly == "Total":
        st.plotly_chart(total_fig, use_container_width=True)
    elif total_monthly == "Monthly mean":
        st.plotly_chart(monthly_fig, use_container_width=True)
    
def unncessary_spent(cat_df: pd.DataFrame):

    df = cat_df.copy()

    # unnecessary spent money for cat
    df = df[df["unnecessary"]]
    df = df.groupby(
        "item", as_index=False).sum(numeric_only=True)
    df.sort_values("cost", inplace=True, ignore_index=True)
    st.plotly_chart(
        figure_or_data=px.bar(
            data_frame=df, x="item", y="cost",
            title="Unnecessary spent money by item"),
        use_container_width=True)

def cost_per_store(cat_df: pd.DataFrame):

    df = cat_df.copy()

    # cost per store
    df = df.groupby("store", as_index=False).sum(numeric_only=True)
    df = df[df["store"] != ""]
    df.sort_values("cost", inplace=True, ignore_index=True)
    st.plotly_chart(
        figure_or_data=px.bar(
            data_frame=df, x="store", y="cost",
            title="Total costs per store"),
        use_container_width=True)
