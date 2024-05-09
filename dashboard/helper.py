from typing import Dict
from datetime import date

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def connect_to_database(
        user: str = "admin",
        password: str = "",
        host: str = "col-database",
        port: int = 5432) -> Engine:

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/col")

    return engine


def get_n_months(
        start_date: date,
        end_date: date) -> int:

    return \
        (end_date.year - start_date.year) * 12 + \
        end_date.month - start_date.month + 1


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # convert to datetime
    df["date"] = pd.to_datetime(df["date"])

    # fill unnecessary with 0 and convert to bool
    df.fillna({"unnecessary": 0}, inplace=True)
    df["unnecessary"] = df["unnecessary"].astype(bool)

    return df


def create_mapping(
        df: pd.DataFrame,
        _map: Dict = {}) -> Dict[str, str]:
    
    for idx, row in df.iterrows():
        if not row["item"] in _map.keys():
            _map[row["item"]] = row["category"]
        else:
            if not row["category"] == _map[row["item"]]:
                raise UserWarning(f"Different categories for {row['item']}")

    return _map


def resample_data(
        df: pd.DataFrame,
        _map: Dict,
        unnecessary: bool = False) -> pd.DataFrame:

    start_date = df["date"].min()
    end_date = df["date"].max()

    date_range = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D")

    for item, cat in _map.items():
        tmp_df = pd.DataFrame({
            "date": date_range,
            "item": item,
            "category": cat,
            "cost": 0,
            "store": "",
            "unnecessary": unnecessary})
        
        df = pd.concat(
            objs=[df, tmp_df],
            ignore_index=True,
            copy=False)

    df.sort_values("date", inplace=True, ignore_index=True)

    return df


def add_date_infos(df: pd.DataFrame) -> pd.DataFrame:

    # add "month" column
    df["month"] = df["date"].dt.month

    # add year column
    df["year"] = df["date"].dt.year

    # add day of week column
    df["dayofweek"] = df["date"].dt.dayofweek

    return df


def read_clean_data(
        sql: str,
        engine: Engine):

    df = pd.read_sql(sql, engine)

    df = clean_data(df)

    _map = create_mapping(df)

    df = resample_data(df, _map)

    df = add_date_infos(df)

    return df


def select_filter(
        orig_df: pd.DataFrame,
        filter_column: str):

    df = orig_df.copy()

    selected_filter = st.selectbox(
        label=f"Choose a {filter_column}",
        options=sorted(df[filter_column].unique()))

    return selected_filter


def filter_df(
        orig_df: pd.DataFrame,
        filter_column: str,
        filter_selection: str):

    df = orig_df[orig_df[filter_column] == filter_selection].copy()

    return df.sort_values("cost", ignore_index=True)
