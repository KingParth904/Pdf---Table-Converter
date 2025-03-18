import streamlit as st
import pandas as pd
import os
from main import extract_tables_from_pdf, save_to_excel

def main():
    st.title("PDF Table Extractor")
    st.write("Upload a PDF file to extract tables and download the results as an Excel file.")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_file:
        temp_pdf_path = f"temp_{uploaded_file.name}"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        tables = extract_tables_from_pdf(temp_pdf_path)
        
        if tables:
            excel_path = "extracted_tables.xlsx"
            save_to_excel(tables, excel_path)
            st.success(f"Extracted {len(tables)} tables successfully!")
            
            df_list = [pd.DataFrame(table[1:], columns=table[0]) for _, table in tables]
            for i, df in enumerate(df_list):
                st.write(f"### Table {i+1}")
                st.dataframe(df)
            
            with open(excel_path, "rb") as f:
                st.download_button(label="Download Excel File", data=f, file_name=excel_path, mime="application/vnd.ms-excel")
            
            os.remove(temp_pdf_path)
            os.remove(excel_path)
        else:
            st.warning("No tables found in the PDF.")

if __name__ == "__main__":
    main()