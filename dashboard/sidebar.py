import streamlit as st
import pandas as pd

import update_data

def upload_new_file(engine):

    with st.expander("Update data"):

        label = "Upload your Excel file containing your costs of living here"

        help = """This file should be an .xlsx file containing the columns
        'date', 'category', 'name', 'cost', 'store' and 'unncessary'"""

        file = st.file_uploader(
            label=label,
            help=help)
        
        if file:
            df = update_data.check_prepare_file(file)

            if isinstance(df, pd.DataFrame):

                st.write("If everything seems fine you can feed it to the database!")
                st.button(
                    label="Feed to database!",
                    on_click=update_data.feed_to_database,
                    args=(df, engine))
                del file, df
