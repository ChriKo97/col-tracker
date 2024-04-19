from typing import Tuple

import streamlit as st
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import text


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

    # cur = con.cursor()

    # sql = f"""
    #     INSERT INTO recurring_costs VALUES (%s, %s, %s, %s, %s, %s)
    # """
    # values = (day, name, category, cost, store, unnecessary)

    # cur.execute(sql, values)

def add_to_database(
        engine: Engine,
        day_of_cost: int,
        category: str,
        store: str,
        name_of_cost: str,
        price_of_cost: str,
        unnecessary: bool):

    create_table(engine)

    add_to_table(
        engine=engine,
        day=day_of_cost,
        name=name_of_cost,
        category=category,
        cost=price_of_cost,
        store=store,
        unnecessary=unnecessary)
