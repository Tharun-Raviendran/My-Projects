import streamlit as st
import sys
import os
import io
import pandas as pd

sys.path.append("/Users/tharun/Documents/Personal/Coding")

from my_app.classes.personal_finance_visualizer_class import MyData

st.title("Expense Analysis App")


uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

with open("/Users/tharun/Documents/School/AP Comp Sci/Performance Task/sample_expenses_f.csv", "rb") as file:
    sample_csv = file.read()

st.markdown("### Download Sample Data")
st.download_button(
    label="Download Sample CSV",
    data=sample_csv,
    file_name="sample_expenses.csv",
    mime="text/csv"
)

st.markdown('### Formating Your Data')
st.write("Please ensure that the CSV file you upload is formatted as shown below.")
sample_csv_str = io.StringIO(sample_csv.decode("utf-8"))
df = pd.read_csv(sample_csv_str)
st.dataframe(df.head())

if uploaded_file:
    data = MyData(uploaded_file)
    
    
    option = st.selectbox(
        "Select the type of graph",
        ["Total Expenses Pie Chart", "Expenses for a Year", "Categorical Expenses per Month"]
    )

    
    if st.checkbox("Show DataFrame"):
        st.write(data.print_df())
        
    
    if option == "Total Expenses Pie Chart":
        st.pyplot(data.total_expenses_pie())

    
    elif option == "Expenses for a Year":
        year = st.selectbox("Select Year", data.get_years())
        st.pyplot(data.expenses_for_year(year))

    
    elif option == "Categorical Expenses per Month":
        catergories = st.multiselect("Select Categories", data.unique_catergories())
        year = st.selectbox("Select Year", data.get_years())
        if catergories:
            st.pyplot(data.catergorical_expenses_per_month_for_a_year(catergories, year))