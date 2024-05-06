import os

import helper
import recurring_costs.recurring_costs as recurring_costs

import streamlit as st


db_user = os.getenv("POSTGRES_USER", "admin")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("DB_HOST", "col-database")
db_port = os.getenv("DB_PORT", 5432)

engine = helper.connect_to_database(
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port)

st.set_page_config(layout='wide')

recurring_costs.view_recurring_costs(engine)

recurring_costs.add_recurring_cost(engine)

