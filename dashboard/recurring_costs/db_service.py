from typing import Tuple

import streamlit as st
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import text


def check_if_in_database(
        engine: Engine,
        name: str) -> Tuple[bool, pd.DataFrame]:

    sql = f"SELECT * FROM recurring_costs WHERE name = '{name}'"

    df = pd.read_sql(sql, engine)

    if len(df) >= 1:
        return True, df
    else:
        return False, df


def get_recurring_costs_from_db(engine: Engine):

    return pd.read_sql(
        "SELECT * FROM recurring_costs",
        engine)


def create_table(engine: Engine):

    with engine.connect() as con:

        sql = f"""
            CREATE TABLE IF NOT EXISTS recurring_costs (
                day INTEGER,
                name TEXT,
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
        day: int,
        name: str,
        category: str,
        cost: float,
        store: str,
        unnecessary: bool):

    df = pd.DataFrame(
        data={
            "day": day,
            "name": name,
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
        name: str):

    with engine.connect() as con:

        sql = f"""
            DELETE FROM recurring_costs
            WHERE name = '{name}'
        """

        con.execute(text(sql))
        con.commit()
        con.close()


def add_to_database(
        engine: Engine,
        day_of_cost: int,
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
            name=name_of_cost)

    add_to_table(
        engine=engine,
        day=day_of_cost,
        name=name_of_cost,
        category=category,
        cost=price_of_cost,
        store=store,
        unnecessary=unnecessary)

    st.success("Successfully added entry to database!")
