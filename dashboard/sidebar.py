import streamlit as st
import pandas as pd


def check_dataframe(df):
    if len(df.columns) > 6:
        msg = "Detected extra columns in your file. "
        msg += "Please check if your file is in the correct format."
        raise ValueError(msg)
    
    if len(df) < 6:
        msg = "Detected missing columns in your file. "
        msg += "Please check if your file is in the correct format."
        raise ValueError(msg)
    
    correct_list = sorted(['category', 'cost', 'date', 'name', 'store', 'unnecessary'])
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
        st.error(f"Something is wrong with your file and can't be parsed correctly: {e}")
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
        st.error(f"Something went wrong preparing your Dataframe for the database: {e}")
        return False

    # display the dataframe
    st.write("This is your data:")
    st.dataframe(cleaned_df, use_container_width=True)

    return cleaned_df

def feed_to_database(df, engine):
    original_df = pd.read_sql("SELECT * FROM col", engine)

    new_database_df = pd.concat([df, original_df], ignore_index=True)
    new_database_df.drop_duplicates(inplace=True, ignore_index=True)

    new_database_df.to_sql(
        name="col",
        con=engine,
        if_exists="replace", 
        index=False)
    
    return


def upload_new_file(engine):

    with st.expander("Update data"):

        label = "Upload your Excel file containing your costs of living here"

        help = """This file should be an .xlsx file containing the columns
        'date', 'category', 'name', 'cost', 'store' and 'unncessary'"""

        file = st.file_uploader(
            label=label,
            help=help)
        
        if file:
            df = check_prepare_file(file)

            if isinstance(df, pd.DataFrame):

                st.write("If everything seems fine you can feed it to the database!")
                st.button("Feed to database!", on_click=feed_to_database, args=(df, engine))
                del file, df
