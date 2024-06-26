import os

import data.update_data as update_data
import helper

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

with st.expander("Add single entry"):
    update_data.add_single_entry(
        engine=engine)

with st.expander("Append to existing data"):
    update_data.upload_new_file(
        engine=engine,
        append_replace="append")
    
with st.expander("Replace existing data"):
    update_data.upload_new_file(
        engine=engine,
        append_replace="replace")

