import recurring_costs.db_service as db_service

from sqlalchemy.engine import Engine
import streamlit as st


def view_recurring_costs(engine: Engine):

    recurring_costs = db_service.get_recurring_costs_from_db(engine)

    with st.expander("View your recurring costs"):

        st.dataframe(
            data=recurring_costs,
            use_container_width=True)


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

        if name_of_cost:

            in_database, data_entry = db_service.check_if_in_database(
                engine=engine,
                name=name_of_cost)

            if in_database:
                st.write("Entry with that name already exists in database:")
                st.dataframe(data_entry, use_container_width=True)

        if day_of_cost and category and name_of_cost and price_of_cost:

            if not in_database:

                st.button(
                    label="Add as recurring cost",
                    on_click=db_service.add_to_database,
                    args=(
                        engine,
                        day_of_cost,
                        category,
                        store,
                        name_of_cost,
                        price_of_cost,
                        unncessary,
                        "append"))

                del day_of_cost, category, name_of_cost, price_of_cost

            else:

                left_col2, right_col2 = st.columns(2)

                with left_col2:
                    st.button(
                        label="Add anyway!",
                        on_click=db_service.add_to_database,
                        args=(
                            engine,
                            day_of_cost,
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
                            day_of_cost,
                            category,
                            store,
                            name_of_cost,
                            price_of_cost,
                            unncessary,
                            "replace"))
