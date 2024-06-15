import streamlit as st
import pandas as pd
import plotly.express as px

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
        check_columns_with_missing_values(df)

        # Plotting section
        st.write("### Data Plotting")
        datetime_column = st.selectbox("Select the datetime column", df.columns)
        
        # Ensure selected column is datetime type
        if not pd.api.types.is_datetime64_any_dtype(df[datetime_column]):
            df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')
        
        parameter_column = st.selectbox("Select the parameter column to plot", [col for col in df.columns if col != datetime_column])
        
        plot_data(df, datetime_column, parameter_column)

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
    duplicates = df.duplicated().sum()
    st.write(f"Number of duplicate rows: {duplicates}")

def check_data_types(df):
    """Displays the data types of each column"""
    st.write("### Data Types")
    data_types = df.dtypes
    st.write(data_types)

def check_summary_stats(df):
    """Displays summary statistics of the dataframe"""
    st.write("### Summary Statistics")
    summary_stats = df.describe()
    st.write(summary_stats)

def check_unique_values_per_column(df):
    """Displays the number of unique values per column"""
    st.write("### Unique Values Per Column")
    unique_values = df.nunique()
    st.write(unique_values)

def check_columns_with_missing_values(df):
    """Displays the number of columns with missing values"""
    st.write("### Columns with Missing Values")
    columns_with_missing = df.columns[df.isnull().any()].tolist()
    st.write(columns_with_missing)

def plot_data(df, datetime_column, parameter_column):
    """Plots the selected parameter against the datetime column using Plotly"""
    fig = px.line(df, x=datetime_column, y=parameter_column, title=f"{parameter_column} over time")
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
