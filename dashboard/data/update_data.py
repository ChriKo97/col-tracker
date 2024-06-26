import pandas as pd
import streamlit as st


def add_single_entry(
        engine):

    date = st.date_input(
        label="Date")

    item = st.text_input(
        label="Name")

    category = st.text_input(
        label="Category")

    store = st.text_input(
        label="Store")

    cost = st.number_input(
        label="Price",
        step=0.01)

    unnecessary = st.checkbox(
        label="Is this cost unnecessary?")

    if date and item and category and cost:

        df = pd.DataFrame(
            data=[[date, item, category, store, cost, unnecessary]],
            columns=["date", "item", "category", "store", "cost", "unnecessary"])

        st.button(
            label="Add",
            on_click=feed_to_database,
            args=(
                df,
                engine,
                "append"))

        st.session_state["new_data_in_db"] = True


def check_dataframe(df):
    if len(df.columns) > 6:
        msg = "Detected extra columns in your file. "
        msg += "Please check if your file is in the correct format."
        raise ValueError(msg)

    if len(df) < 6:
        msg = "Detected missing columns in your file. "
        msg += "Please check if your file is in the correct format."
        raise ValueError(msg)
    
    correct_list = sorted(['category', 'cost', 'date', 'item', 'store', 'unnecessary'])
    if sorted(df.columns) != correct_list:
        msg = "Detected not supported column names in your file. "
        msg += "Please check if your file is in the correct format. "
        msg += f"The correct columns are {correct_list} but your column names are "
        msg += f"{sorted(df.columns)}"
        raise ValueError(msg)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df["unnecessary"] = df["unnecessary"].fillna(0).astype(bool)

    df["date"] = pd.to_datetime(df["date"]).dt.date

    return df


def check_prepare_file(file):

    # read dataframe
    try:
        df = pd.read_excel(file)
    except Exception as e:
        st.error(
            f"Something is wrong with your file and can't be parsed correctly: {e}")
        return False

    # check if dataframe seems correct
    try:
        check_dataframe(df)
    except Exception as e:
        st.error(e)
        return False

    # clean dataframae
    try:
        cleaned_df = clean_dataframe(df)
    except Exception as e:
        st.error(
            f"Something went wrong preparing your Dataframe for the database: {e}")
        return False

    # display the dataframe
    st.write("This is your data:")
    st.dataframe(cleaned_df, use_container_width=True)

    return cleaned_df


def confirm(add_replace):
    if add_replace == "append":
        msg = "I understand that everything in the table will be *added* to the database"
        return st.checkbox(msg)

    elif add_replace == "replace":
        msg = "I understand that everything in the database will be *deleted* and *replaced* by the table"
        return st.checkbox(msg)


def feed_to_database(
        df,
        engine,
        append_replace):

    df.to_sql(
        name="col",
        con=engine,
        if_exists=append_replace,
        index=False)

    st.success("Succesfully added to database!")


def upload_new_file(
        engine,
        append_replace):

    label = "Upload your Excel file containing your costs of living here"

    help = """This file should be an .xlsx file containing the columns
    'date', 'category', 'item', 'cost', 'store' and 'unncessary'"""

    file = st.file_uploader(
        label=label,
        key=append_replace,
        help=help)

    if file:
        df = check_prepare_file(file)

        if isinstance(df, pd.DataFrame):

            st.write("If everything seems fine you can feed it to the database!")
            if confirm(append_replace):
                st.button(
                    label="Feed to database!",
                    on_click=feed_to_database,
                    args=(df, engine, append_replace))
                del file, df

                st.session_state["new_data_in_db"] = True
