import recurring_costs.db_service as db_service

from sqlalchemy.engine import Engine
import streamlit as st


def add_recurring_cost(engine: Engine):
    with st.expander("Add recurring cost"):
        left_col, right_col = st.columns(2)

        with left_col:

            day_of_cost = st.number_input(
                label="On which day of the month does the cost occur?",
                min_value=1, max_value=31, step=1,
                value=1)

            category = st.text_input(
                label="Which category does the cost fall into?")

            store = st.text_input(
                label="Where / at which store does the cost occur? (optional)")

        with right_col:

            name_of_cost = st.text_input(
                label="What is the name of the recurring cost?")

            price_of_cost = st.number_input(
                label="How much is the recurring cost?",
                min_value=0.01, step=1.0, value=50.0)

            st.write("Is this cost unnecessary?")
            unncessary = st.checkbox("Unnecessary")

        if day_of_cost and category and name_of_cost and price_of_cost:

            st.button(
                label="Add as recurring cost",
                on_click=db_service.add_to_database,
                args=(
                    engine,
                    day_of_cost,
                    category,
                    store,
                    name_of_cost,
                    price_of_cost, unncessary))
