from typing import Dict

import pandas as pd


def read_data() -> pd.DataFrame:

    orig_df = pd.read_excel("C:\\Users\\ck4400e\\Documents\\03_privat\\02_coding\\03_kosten_graphs\\Lebenshaltungskosten.xlsx")

    return orig_df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # convert to datetime
    df["date"] = pd.to_datetime(df["date"])

    # remove alternative column
    df.drop(columns="alternative", inplace=True)

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
                raise UserWarning(f"Different categories for {row["name"]}")

    return _map


def resample_data(
        df: pd.DataFrame,
        _map: Dict) -> pd.DataFrame:

    start_date = df["Datum"].min()
    end_date = df["Datum"].max()

    date_range = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D")

    for name, cat in _map.items():
        tmp_df = pd.DataFrame({
            "date": date_range,
            "name": name,
            "category": cat,
            "costs": 0,
            "where": "",
            "unnecessary": False})
        
        df = pd.concat(
            objs=[df, tmp_df],
            ignore_index=True,
            copy=False)

    df.sort_values("Datum", inplace=True)

    return df
