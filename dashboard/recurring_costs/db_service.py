from typing import Tuple

import streamlit as st
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import text
import datetime

from sqlalchemy.exc import ProgrammingError


def check_if_in_database(
        engine: Engine,
        item: str) -> Tuple[bool, pd.DataFrame]:

    sql = f"SELECT * FROM recurring_costs WHERE item = '{item}'"

    df = pd.read_sql(sql, engine)

    if len(df) >= 1:
        return True, df
    else:
        return False, df


def get_recurring_costs_from_db(engine: Engine):

    try:
        df = pd.read_sql(
            "SELECT * FROM recurring_costs",
            engine)
        return df
    except ProgrammingError:
        create_table(engine)
        df = pd.read_sql(
            "SELECT * FROM recurring_costs",
            engine)
        return df


def create_table(engine: Engine):

    with engine.connect() as con:

        sql = f"""
            CREATE TABLE IF NOT EXISTS recurring_costs (
                "start" DATE,
                "end" DATE,
                frequency TEXT,
                item TEXT,
                category TEXT,
                cost DOUBLE PRECISION,
                store TEXT,
                unnecessary BOOL)
        """

        con.execute(text(sql))
        con.commit()
        con.close()


def add_to_table(
        engine: Engine,
        start_date: datetime.date,
        end_date: datetime.date,
        frequency: str,
        item: str,
        category: str,
        cost: float,
        store: str,
        unnecessary: bool):

    df = pd.DataFrame(
        data={
            "start": start_date,
            "end": end_date,
            "frequency": frequency,
            "item": item,
            "category": category,
            "cost": cost,
            "store": store,
            "unnecessary": unnecessary},
        index=[0])

    df.to_sql(
        name="recurring_costs",
        con=engine,
        if_exists="append",
        index=False)


def remove_from_table(
        engine: Engine,
        item: str):

    with engine.connect() as con:

        sql = f"""
            DELETE FROM recurring_costs
            WHERE item = '{item}'
        """

        con.execute(text(sql))
        con.commit()
        con.close()


def add_to_database(
        engine: Engine,
        start_date: datetime.date,
        end_date: datetime.date,
        frequency: str,
        category: str,
        store: str,
        name_of_cost: str,
        price_of_cost: str,
        unnecessary: bool,
        append_replace: str):

    create_table(engine)

    if append_replace == "replace":
        remove_from_table(
            engine=engine,
            item=name_of_cost)

    add_to_table(
        engine=engine,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        item=name_of_cost,
        category=category,
        cost=price_of_cost,
        store=store,
        unnecessary=unnecessary)

    st.success("Successfully added entry to database!")
