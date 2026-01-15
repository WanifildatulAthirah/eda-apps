import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io 

st.set_page_config(page_title="EDA App - Wani", layout="wide", page_icon="🌼")

st.title("📊 Data Science EDA App")
st.write("Upload A **CSV or Excel** File And Start Explore Your Data Interactively")

# for uploading csv file
uploaded_file = st.file_uploader("📂Upload Your CSV or Excel File", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # convert boolean column as string
        bool_cols = df.select_dtypes(include=['bool']).columns
        df[bool_cols] = df[bool_cols].astype(str)

        st.success("✅ File Uploaded Successfully!")
        st.write("**🔍 Data Overview**")
        st.dataframe(df.head())

        st.write("👉Number Of Missing Values : ", df.isnull().sum().sum())
        st.write("👉Number Of Duplicate Records : ", df.duplicated().sum())

        st.write("**📍Complete Summary of Dataset**")
        buffer = io.StringIO()
        df.info(buf=buffer)
        info = buffer.getvalue()
        st.text(info)

        st.write("**📈 Statistical Summary Of Dataset**")
        st.dataframe(df.describe())

        st.write("**📈 Statistical Summary For Non Numerical Features**")
        st.dataframe(df.describe(include='object'))

        st.write("**🕵🏾‍♂️ Select Your Desired Columns**")
        column = st.multiselect("Choose Column", df.columns.tolist())
        st.write("**📄 Preview**")
        if column:
            st.dataframe(df[column].head())
        else:
            st.info("No Columns Selected. Showing Full Dataset")
            st.dataframe(df.head())

        st.write("**🧮 Data Visualization**")
        columns = df.columns.tolist()
        x_axis = st.selectbox("Select Column For the X-Axis", options=columns)
        y_axis = st.selectbox("Select Column For the Y-Axis", options=columns)

        # Create buttons for chart types
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            lin_btn = st.button("Click Here To Generate A Line Graph")
        with col2:
            bar_btn = st.button("Click Here To Generate A Bar Graph")
        with col3:
            scatter_btn = st.button("Click Here To Generate A Scatter Plot")
        with col4:
            box_btn = st.button("Click Here To Generate A Box Plot")

        # Plot The Graphs
        if lin_btn:
            st.write("Line Graph")
            fig, ax = plt.subplots()
            ax.plot(df[x_axis], df[y_axis], marker='o')
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Line Graph of {y_axis} vs {x_axis}")
            st.pyplot(fig)
            
        if bar_btn:
            st.write("Bar Graph")
            fig, ax = plt.subplots()
            ax.bar(df[x_axis], df[y_axis], color ='skyblue')
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Bar Graph of {y_axis} vs {x_axis}")
            st.pyplot(fig)
            
        if scatter_btn:
            st.write("Scatter Plot Graph")
            fig, ax = plt.subplots()
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
            ax.set_title(f"Scatter Plot Graph of {y_axis} vs {x_axis}")
            st.pyplot(fig)
            
        if box_btn:
            st.write("Box Plot Graph")
            fig, ax = plt.subplots()
            sns.boxplot(x=df[x_axis],y=df[y_axis], ax=ax)
            ax.set_title(f"Box Plot Graph of {y_axis} vs {x_axis}")
            st.pyplot(fig)
        

        # Ask user for some query
        st.write("**❓EDA FAQs**")

        query = st.selectbox("Choose a query",
                            ["Show top 5 categories",
                             "Show all records where customer service calls > 5"
                            ])

        if query == "Show top 5 categories":
            cat_col = st.selectbox("Select categorical column", df.select_dtypes(include="object").columns)
            result = df[cat_col].value_counts().head(5).reset_index()
            result.columns = [cat_col, "Count"]
            st.write("**Top 5 Categories**")
            st.dataframe(result)

        elif query == "Show all records where customer service calls > 5": 
            num_col = "customer service calls"
            result = df[df[num_col] > 5]
            st.write("**All Records where Customer Service Calls > 5**")
            st.dataframe(result)


    except Exception as e:
        st.error("Could not read the file. Please Upload A CVS or Excel file again")
        st.exception(e)
        st.stop()