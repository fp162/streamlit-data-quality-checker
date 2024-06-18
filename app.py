import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

st.set_page_config(
    page_title="IoT Data Quality Checker",
    page_icon="🔍",
    layout="wide",
)

# Function to display the Data Quality tab
def data_quality_tab():
    st.title("IoT Data Quality Checker")

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

        # Anomaly Detection
        if st.checkbox("Run Anomaly Detection"):
            anomaly_detection(df)

        # Existing Quality Checks
        check_total_rows(df)
        check_unique_parameters(df)
        check_null_percentage(df)
        check_duplicates(df)
        check_data_types(df)
        check_summary_stats(df)
        check_unique_values_per_column(df)
        check_columns_with_missing_values(df)

def anomaly_detection(df):
    st.write("### Anomaly Detection")
    datetime_column = st.selectbox("Select the datetime column", df.columns)
    parameter_column = st.selectbox("Select the parameter column to analyze", [col for col in df.columns if col != datetime_column])

    # Isolation Forest for anomaly detection
    model = IsolationForest(contamination=0.05)
    df['anomaly'] = model.fit_predict(df[[parameter_column]])
    df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})  # 0 for normal, 1 for anomaly

    plot_anomaly_data(df, datetime_column, parameter_column, 'anomaly')

def plot_anomaly_data(df, datetime_column, parameter_column, anomaly_column):
    fig = px.scatter(df, x=datetime_column, y=parameter_column, color=anomaly_column,
                     title=f"{parameter_column} with Anomalies")
    st.plotly_chart(fig)

# Existing quality checks
def check_total_rows(df):
    st.write("### Total Number of Rows")
    total_rows = df.shape[0]
    st.write(f"Total rows: {total_rows}")

def check_unique_parameters(df):
    st.write("### Unique Parameters (Columns)")
    unique_columns = df.columns.tolist()
    st.write(unique_columns)

def check_null_percentage(df):
    st.write("### Percentage of Null Values")
    null_percentage = (df.isnull().sum() / len(df)) * 100
    st.write(null_percentage)

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
    summary_stats = df.describe(include='all')
    st.write(summary_stats)

def check_unique_values_per_column(df):
    st.write("### Unique Values Per Column")
    unique_values = df.nunique()
    st.write(unique_values)

def check_columns_with_missing_values(df):
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

        df[datetime_column] = pd.to_datetime(df[datetime_column], errors='coerce')
        df = df.dropna(subset=[datetime_column])

        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)

        parameter_column = st.selectbox("Select the parameter column to plot", [col for col in df.columns if col != datetime_column])

        # Default selection of the latest 30% of data
        end_date = df[datetime_column].max()
        start_date = df[datetime_column].quantile(0.7)

        st.write(f"By default, displaying the latest 30% of data from {start_date.date()} to {end_date.date()}")
        filtered_df = df[(df[datetime_column] >= start_date) & (df[datetime_column] <= end_date)]

        # Custom date range selection
        st.write("### Custom Date Range Selection")
        custom_start_date = st.date_input("Select start date", value=start_date.date(), min_value=df[datetime_column].min().date(), max_value=df[datetime_column].max().date())
        custom_end_date = st.date_input("Select end date", value=end_date.date(), min_value=custom_start_date, max_value=df[datetime_column].max().date())

        if st.button("Apply Custom Date Range"):
            filtered_df = df[(df[datetime_column] >= pd.to_datetime(custom_start_date)) & (df[datetime_column] <= pd.to_datetime(custom_end_date))]

        plot_type = st.selectbox("Select Plot Type", ["Line Plot", "Scatter Plot", "Bar Chart", "Histogram", "Heatmap"])

        if plot_type == "Line Plot":
            plot_data(filtered_df, datetime_column, parameter_column, title="Line Plot")
        elif plot_type == "Scatter Plot":
            plot_scatter(filtered_df, datetime_column, parameter_column, title="Scatter Plot")
        elif plot_type == "Bar Chart":
            plot_bar(filtered_df, datetime_column, parameter_column, title="Bar Chart")
        elif plot_type == "Histogram":
            plot_histogram(filtered_df, parameter_column, title="Histogram")
        elif plot_type == "Heatmap":
            plot_heatmap(filtered_df, datetime_column, parameter_column, title="Heatmap")

        st.write("### EWMA Settings")
        ewma_type = st.radio("Select EWMA Type", options=["Alpha (Smoothing Factor)", "Span", "Center of Mass"])

        if ewma_type == "Alpha (Smoothing Factor)":
            alpha = st.slider("Select the smoothing factor (alpha)", min_value=0.01, max_value=1.0, value=0.2)
            if st.button("Run EWMA with Alpha"):
                filtered_df['EWMA'] = filtered_df[parameter_column].ewm(alpha=alpha, adjust=False).mean()
                plot_combined_data(filtered_df, datetime_column, parameter_column, 'EWMA')
        
        elif ewma_type == "Span":
            span = st.slider("Select the span (number of periods)", min_value=1, max_value=100, value=20)
            if st.button("Run EWMA with Span"):
                filtered_df['EWMA'] = filtered_df[parameter_column].ewm(span=span, adjust=False).mean()
                plot_combined_data(filtered_df, datetime_column, parameter_column, 'EWMA')
        
        elif ewma_type == "Center of Mass":
            center_of_mass = st.slider("Select the center of mass", min_value=0.0, max_value=30.0, value=10.0)
            if st.button("Run EWMA with Center of Mass"):
                filtered_df['EWMA'] = filtered_df[parameter_column].ewm(com=center_of_mass, adjust=False).mean()
                plot_combined_data(filtered_df, datetime_column, parameter_column, 'EWMA')

def plot_data(df, datetime_column, parameter_column, title="Data"):
    fig = px.line(df, x=datetime_column, y=parameter_column, title=f"{title}: {parameter_column} over time")
    st.plotly_chart(fig)

def plot_scatter(df, datetime_column, parameter_column, title="Scatter Plot"):
    fig = px.scatter(df, x=datetime_column, y=parameter_column, title=f"{title}: {parameter_column} over time")
    st.plotly_chart(fig)

def plot_bar(df, datetime_column, parameter_column, title="Bar Chart"):
    fig = px.bar(df, x=datetime_column, y=parameter_column, title=f"{title}: {parameter_column} over time")
    st.plotly_chart(fig)

def plot_histogram(df, parameter_column, title="Histogram"):
    fig = px.histogram(df, x=parameter_column, title=f"{title}: {parameter_column} Distribution")
    st.plotly_chart(fig)

def plot_heatmap(df, datetime_column, parameter_column, title="Heatmap"):
    fig = px.density_heatmap(df, x=datetime_column, y=parameter_column, title=f"{title}: {parameter_column} Heatmap")
    st.plotly_chart(fig)

def plot_combined_data(df, datetime_column, original_column, ewma_column):
    fig = px.line(df, x=datetime_column, y=[original_column, ewma_column], title=f"{original_column} and {ewma_column} over time")
    st.plotly_chart(fig)

# Sidebar for navigation```python
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Data Quality Checker", "Data Plotting"])

# Conditional display of each tab
if selection == "Data Quality Checker":
    data_quality_tab()
elif selection == "Data Plotting":
    data_plotting_tab()
