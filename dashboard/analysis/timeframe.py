from typing import Tuple

import streamlit as st
import pandas as pd
from sqlalchemy.engine import Engine


def get_min_max_dates(engine: Engine) -> Tuple[str, str]:

    min_max_dates = pd.read_sql("SELECT MIN(date), MAX(date) FROM col", engine)
    min_date = min_max_dates.loc[0, "min"]
    max_date = min_max_dates.loc[0, "max"]

    return (min_date, max_date)


def display_timeframe_options(
        min_date: str,
        max_date: str):

    time_frame = st.radio(
        label="timeframe",
        options=[
            "All",
            "Custom"],
        horizontal=True)

    if time_frame == "Custom":
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
            
        return start_date, end_date

    else:
         return time_frame


def create_sql_query(time_frame: str | Tuple[str, str]) -> str:
        
        if isinstance(time_frame, Tuple):
            start_date = time_frame[0]
            end_date = time_frame[1]

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

            return sql
        
        elif isinstance(time_frame, str):
            if time_frame == "All":
                 return "SELECT * FROM col"
