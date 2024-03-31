from typing import Dict

import pandas as pd


def read_data() -> pd.DataFrame:

    orig_df = pd.read_excel("C:\\Users\\ck4400e\\Documents\\03_privat\\02_coding\\03_kosten_graphs\\Lebenshaltungskosten.xlsx")

    return orig_df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # convert to datetime
    df["Datum"] = pd.to_datetime(df["Datum"])

    # remove alternative column
    df.drop(columns="Alternative", inplace=True)

    # fill unnecessary with 0 and convert to bool
    df.fillna({"Unnötig": 0}, inplace=True)
    df["Unnötig"] = df["Unnötig"].astype(bool)

    return df


def create_mapping(
        df: pd.DataFrame,
        _map: Dict = {}) -> Dict[str, str]:
    
    for idx, row in df.iterrows():
        if not row["Bezeichnung"] in _map.keys():
            _map[row["Bezeichnung"]] = row["Kategorie"]
        else:
            if not row["Kategorie"] == _map[row["Bezeichnung"]]:
                raise UserWarning(f"Different categories for {row["Bezeichnung"]}")

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
            "Datum": date_range,
            "Bezeichnung": name,
            "Kategorie": cat,
            "Kosten": 0,
            "Wo": "",
            "Unnötig": False})
        
        df = pd.concat(
            objs=[df, tmp_df],
            ignore_index=True,
            copy=False)

    df.sort_values("Datum", inplace=True)

    return df
