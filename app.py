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
    summary_stats = df.describe(include='all', datetime_is_numeric=True)
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

# Function to display the Data Plotting tab
def data_plotting_tab():
    st.title("Data Plotting")

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

        # Plotting section
        st.write("### Data Plotting")
        datetime_column = st.selectbox("Select the datetime column", df.columns)

        # Ensure selected column is datetime type and drop rows where conversion fails
        df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')
        df = df.dropna(subset=[datetime_column])

        # Convert object type columns to strings to avoid serialization issues
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)

        parameter_column = st.selectbox("Select the parameter column to plot", [col for col in df.columns if col != datetime_column])

        # Plot the original data
        plot_data(df, datetime_column, parameter_column)

        # EWMA settings
        st.write("### EWMA Settings")
        lambda_ = st.slider("Select the smoothing factor (lambda)", min_value=0.01, max_value=1.0, value=0.2)
        span = st.slider("Select the span (number of periods)", min_value=1, max_value=100, value=20)
        center_of_mass = st.slider("Select the center of mass", min_value=0.0, max_value=30.0, value=10.0)

        if st.button("Run EWMA"):
            df['EWMA'] = df[parameter_column].ewm(alpha=lambda_, span=span, adjust=False).mean()
            plot_data(df, datetime_column, 'EWMA')

def plot_data(df, datetime_column, parameter_column):
    """Plots the selected parameter against the datetime column using Plotly"""
    fig = px.line(df, x=datetime_column, y=parameter_column, title=f"{parameter_column} over time")
    st.plotly_chart(fig)

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Data Quality Checker", "Data Plotting"])

# Conditional display of each tab
if selection == "Data Quality Checker":
    data_quality_tab()
elif selection == "Data Plotting":
    data_plotting_tab()
