import pandas as pd
import plotly.express as px
import streamlit as st


def time_bar_graph(
        df: pd.DataFrame,
        primary_grouping_col: str = None,
        color_col: str = None):

    df = df.copy()

    df = df.groupby(
        by=primary_grouping_col).resample(
            "ME", on="date").sum(
            numeric_only=True)

    df.reset_index(inplace=True)
    df.sort_values(["date", primary_grouping_col],
                   ignore_index=True, inplace=True)

    cost_per_month_fig = px.bar(
        data_frame=df, x="date", y="cost",
        title="Cost per month over time",
        color=color_col)
    cost_per_month_fig.layout.xaxis.tickvals = pd.date_range(
        start=df["date"].min(),
        end=df["date"].max(),
        freq='ME')
    cost_per_month_fig.layout["xaxis_tickformat"] = "%B %Y"

    st.plotly_chart(
        figure_or_data=cost_per_month_fig,
        use_container_width=True)


def grouped_bar_graph(
        df: pd.DataFrame,
        tab_name: str,
        n_months: int,
        primary_grouping_col: str = None,
        unnecessary: bool = False):

    df = df.copy()

    if unnecessary:
        df = df[df["unnecessary"]]
        total_title = f"Total unnecessary cost per {primary_grouping_col}"
        monthly_title = f"Mean monthly unnecessary cost per {primary_grouping_col}"
    else:
        total_title = f"Total cost per {primary_grouping_col}"
        monthly_title = f"Mean monthly cost per {primary_grouping_col}"

    # selection for total or monthly mean
    total_monthly = st.radio(
        label="", key=f"{tab_name}_{primary_grouping_col}_total_or_monthly_{unnecessary}",
        options=["Total", "Monthly mean"],
        horizontal=True)

    # total fig
    total_df = df.groupby(primary_grouping_col,
                          as_index=False).sum(numeric_only=True)
    total_df.sort_values("cost", inplace=True, ignore_index=True)
    total_fig = px.bar(
        data_frame=total_df, x=primary_grouping_col, y="cost",
        title=total_title)

    # monthly mean fig
    monthly_df = total_df.copy()
    monthly_df["cost"] = monthly_df["cost"] / n_months
    monthly_df.sort_values("cost", inplace=True, ignore_index=True)

    monthly_fig = px.bar(
        data_frame=monthly_df, x=primary_grouping_col, y="cost",
        title=monthly_title)

    if total_monthly == "Total":
        st.plotly_chart(total_fig, use_container_width=True)
    elif total_monthly == "Monthly mean":
        st.plotly_chart(monthly_fig, use_container_width=True)
