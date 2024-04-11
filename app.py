import streamlit as st
from data_processing import process_csv_file
from generate_wordcloud import generate_word_cloud
from piechart import generate_dashboard
import pandas as pd
import config

def main():
    st.title("Fino Payments Bank Marketing Tool by Aayush Jain")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file is not None:
        config.organisation = st.text_input("Enter your Orgs Name")
        api_key = st.text_input("Enter your API key")
        config.apikey= api_key
        df = process_csv_file(uploaded_file)

        st.subheader("Word Clouds for all applications")
        word_cloud_file_paths = generate_word_cloud(df)
        sources = list(df['Source'].unique())
        sources.insert(0, "Cummulative")  
        num_cols = 3  
        rows = [st.columns(num_cols) for _ in range((len(word_cloud_file_paths) + num_cols - 1) // num_cols)]
        for file_path, header, col in zip(word_cloud_file_paths, sources, sum(rows, [])):
            with col:
                st.header(header)
                st.image(file_path)

        st.subheader("Dashboard for all applications")
        dashboard_file_paths = generate_dashboard(df)
        num_cols = 3  
        rows = [st.columns(num_cols) for _ in range((len(dashboard_file_paths) + num_cols - 1) // num_cols)]
        for file_path, header, col in zip(dashboard_file_paths, sources, sum(rows, [])):
            with col:
                st.header(header)
                st.image(file_path)


if __name__ == "__main__":
    main()