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
        check_nulls(df)
        check_duplicates(df)
        check_data_types(df)
        check_summary_stats(df)

def check_nulls(df):
    st.write("### Null Values")
    null_values = df.isnull().sum()
    st.write(null_values)

def check_duplicates(df):
    st.write("### Duplicates")
    duplicates = df.duplicated().sum()
    st.write(f"Number of duplicate rows: {duplicates}")

def check_data_types(df):
    st.write("### Data Types")
    data_types = df.dtypes
    st.write(data_types)

def check_summary_stats(df):
    st.write("### Summary Statistics")
    summary_stats = df.describe()
    st.write(summary_stats)

if __name__ == "__main__":
    main()
