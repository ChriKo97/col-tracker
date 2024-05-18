import os
import logging
from typing import List
import time

from dateutil.relativedelta import relativedelta
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import pandas as pd


db_user = os.getenv("POSTGRES_USER", "admin")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST", "col-database")
db_port = os.getenv("POSTGRES_PORT", 5432)


def get_timedelta(freq: str) -> relativedelta:
    
    if freq == "Weekly":
        return relativedelta(weeks=1)
    elif freq == "Bi-weekly":
        return relativedelta(weeks=2)
    elif freq == "Monthly":
        return relativedelta(months=1)
    elif freq == "Quarterly":
        return relativedelta(months=3)
    elif freq == "Yearly":
        return relativedelta(years=1)


def build_date_range(
        start: date,
        end: date,
        freq: relativedelta) -> List[date]:
    
    date_range = [start]

    delta = get_timedelta(freq)

    while max(date_range) < end:
        next_date = max(date_range) + delta
        date_range.append(next_date)

    return date_range


def add_row_to_database(
        row: pd.Series,
        engine: Engine) -> None:

    # create dataframe from series
    df = row.to_frame().transpose()

    # drop not needed columns
    df.drop(
        columns=[
            "start",
            "end",
            "frequency"],
        inplace=True)

    # add to col-table
    df.to_sql(
        name="col",
        con=engine,
        index=False,
        if_exists="append")


def create_cost_df(row):

    date_range = build_date_range(
                start=row["start"],
                end=row["end"],
                freq=row["frequency"])
            
    df = pd.DataFrame()
    df["date"] = date_range
    df["category"] = row["category"]
    df["item"] = row["item"]
    df["category"] = row["category"]
    df["cost"] = row["cost"]
    df["store"] = row["store"]
    df["unnecessary"] = row["unnecessary"]

    df = df[df["date"] <= date.today()].reset_index(drop=True)

    return df


def remove_duplicates(
        all_costs: pd.DataFrame,
        existing_costs: pd.DataFrame):

    all_costs = {tuple(x) for x in all_costs.to_numpy()}
    existing_costs = {tuple(x) for x in existing_costs.to_numpy()}

    df = pd.DataFrame(
        data=(all_costs ^ existing_costs),
        columns=["date", "category", "item", "cost", "store", "unnecessary"])

    return df


def add_recurring_costs():

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S')

    try:
        URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/col"
        engine = create_engine(URI)

        recurring = pd.read_sql("SELECT * FROM recurring_costs", engine)

        for idx, row in recurring.iterrows():

            all_costs = create_cost_df(row)


            sql = f"""
                SELECT * FROM col
                WHERE item = '{row["item"]}'
                AND category = '{row["category"]}'
                AND cost = '{row["cost"]}'
            """
            existing_recurring = pd.read_sql(sql, engine)

            new_costs = remove_duplicates(
                all_costs=all_costs,
                existing_costs=existing_recurring)

            if not new_costs.empty:
                new_costs.to_sql(
                    name="col",
                    con=engine,
                    index=False,
                    if_exists="append")

    except Exception as e:
        logging.error(e)


if __name__ == "__main__":

    while True:

        start_time = time.time()

        add_recurring_costs()

        end_time = time.time()
        elapsed_time = end_time - start_time

        time.sleep(10 - elapsed_time)
