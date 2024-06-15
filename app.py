import streamlit as st
import pandas as pd

def main():
    st.title("Data Quality Checker")

    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("Data Preview:")
        st.dataframe(df.head())

        st.write("Data Quality Indicators:")

        # Data Quality Checks
        check_total_rows(df)
        check_unique_parameters(df)
        check_null_percentage(df)
        check_duplicates(df)
        check_data_types(df)
        check_summary_stats(df)
        check_unique_values_per_column(df)
        check_columns_with_missing_values(
