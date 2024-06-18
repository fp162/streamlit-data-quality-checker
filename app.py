import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Data Quality Checker",
    page_icon="🔍",
    layout="wide",
)

# Function to display the Data Quality tab
def data_quality_tab():
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
        check_columns_with_missing_values(df)

def check_total_rows(df):
    """Displays the total number of rows in the dataframe"""
    st.write("### Total Number of Rows")
    total_rows = df.shape[0]
    st.write(f"Total rows: {total_rows}")

def check_unique_parameters(df):
    """Displays the unique parameter list (column names)"""
    st.write("### Unique Parameters (Columns)")
    unique_columns = df.columns.tolist()
    st.write(unique_columns)

def check_null_percentage(df):
    """Displays the percentage of null values in each column"""
    st.write("### Percentage of Null Values")
    null_percentage = (df.isnull().sum() / len(df)) * 100
    st.write(null_percentage)

def check_duplicates(df):
    """Displays the number of duplicate rows"""
    st.write("### Duplicates")
    duplicates = df.duplicated().sum
