import recurring_costs.db_service as db_service

from sqlalchemy.engine import Engine
import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta


def create_end_date(
        start_date: date,
        end: str):

    if end == "After 1 week":
        end_date = start_date + relativedelta(weeks=1)
    elif end == "After 1 month":
        end_date = start_date + relativedelta(months=30)
    elif end == "After 1 year":
        end_date = start_date + relativedelta(years=1)
    elif end == "After 5 years":
        end_date = start_date + relativedelta(years=5)
    elif end == "Never":
        end_date = date(2099, 12, 31)
    elif end == "Choose a date":
        end_date = st.date_input(
            label="recurring_end_date_input",
            label_visibility="collapsed",
            min_value=start_date)

    return end_date


def view_recurring_costs(engine: Engine):

    recurring_costs = db_service.get_recurring_costs_from_db(engine)

    with st.expander("View your recurring costs"):

        if recurring_costs.empty:
            st.write("You do not have any recurring costs!")
        else:
            st.dataframe(
                data=recurring_costs,
                use_container_width=True)


def add_recurring_cost(engine: Engine):
    with st.expander("Add recurring cost"):

        start_date = st.date_input(
            label="When does this cost start occuring?",
            value=date.today())

        name_of_cost = st.text_input(
            label="What is the name of the recurring cost?")

        category = st.text_input(
            label="Which category does the cost fall into?")

        store = st.text_input(
            label="Where / at which store does the cost occur? (optional)")

        price_of_cost = st.number_input(
            label="How much is the recurring cost?",
            min_value=0.01, step=1.0, value=50.0)

        st.write("Is this cost unnecessary?")
        unncessary = st.checkbox("Unnecessary")

        frequency = st.radio(
            label="With which frequency does this cost occur?",
            options=[
                "Weekly",
                "Bi-weekly",
                "Monthly",
                "Quarterly",
                "Yearly"],
            horizontal=True)

        end = st.radio(
            label="When will this cost stop occuring?",
            options=[
                "After 1 week",
                "After 1 month",
                "After 1 year",
                "After 5 years",
                "Never",
                "Choose a date"],
            horizontal=True)

        end_date = create_end_date(start_date, end)

        if name_of_cost:

            in_database, data_entry = db_service.check_if_in_database(
                engine=engine,
                name=name_of_cost)

            if in_database:
                st.write("Entry with that name already exists in database:")
                st.dataframe(data_entry, use_container_width=True)

        if start_date and category and name_of_cost and price_of_cost:

            if not in_database:

                st.button(
                    label="Add as recurring cost",
                    on_click=db_service.add_to_database,
                    args=(
                        engine,
                        start_date,
                        end_date,
                        frequency,
                        category,
                        store,
                        name_of_cost,
                        price_of_cost,
                        unncessary,
                        "append"))

            else:

                left_col2, right_col2 = st.columns(2)

                with left_col2:
                    st.button(
                        label="Add anyway!",
                        on_click=db_service.add_to_database,
                        args=(
                            engine,
                            start_date,
                            end_date,
                            frequency,
                            category,
                            store,
                            name_of_cost,
                            price_of_cost,
                            unncessary,
                            "append"))

                with right_col2:
                    st.button(
                        label="Replace!",
                        on_click=db_service.add_to_database,
                        args=(
                            engine,
                            start_date,
                            end_date,
                            frequency,
                            category,
                            store,
                            name_of_cost,
                            price_of_cost,
                            unncessary,
                            "replace"))
