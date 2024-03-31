import helper

import streamlit as st


orig_df = helper.read_data()

orig_df = helper.clean_data(orig_df)

_map = helper.create_mapping(orig_df)

orig_df = helper.resample_data(orig_df, _map)


lcol, rcol = st.columns(2)

with lcol:
    start_date = st.date_input(
        label="Start date",
        value=orig_df["Datum"].dt.date.min(),
        min_value=orig_df["Datum"].dt.date.min())

with rcol:
    end_date = st.date_input(
        label="End date",
        value=orig_df["Datum"].dt.date.max(),
        min_value=orig_df["Datum"].dt.date.max())

cond = ((orig_df["Datum"].dt.date >= start_date) &
        (orig_df["Datum"].dt.date <= end_date))
filtered_df = orig_df[cond].reset_index(drop=True)
