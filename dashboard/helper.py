from typing import Dict

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def connect_to_database(
        user: str = "admin",
        password: str = "",
        name: str = "col",
        host: str = "col-database",
        port: int = 5432):

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{name}")

    return engine


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
        if not row["name"] in _map.keys():
            _map[row["name"]] = row["category"]
        else:
            if not row["category"] == _map[row["name"]]:
                raise UserWarning(f"Different categories for {row['name']}")

    return _map


def resample_data(
        df: pd.DataFrame,
        _map: Dict) -> pd.DataFrame:

    start_date = df["date"].min()
    end_date = df["date"].max()

    date_range = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D")

    for name, cat in _map.items():
        tmp_df = pd.DataFrame({
            "date": date_range,
            "name": name,
            "category": cat,
            "cost": 0,
            "where": "",
            "unnecessary": False})
        
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
