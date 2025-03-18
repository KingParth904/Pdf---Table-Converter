PDF Table Extractor

This project is a PDF Table Extractor built using Streamlit for the UI and pdfplumber for table extraction. The tool allows users to upload a PDF, extract tabular data, preview it, and download the extracted tables as an Excel file.

Features

📂 Upload a PDF file

🔍 Extract tables from the document

👀 Preview extracted tables in the UI

📥 Download the extracted tables as an Excel file

Installation

To run this project, ensure you have Python 3.7+ installed, then install the required dependencies:

pip install -r requirements.txt

Dependencies

The project requires the following libraries:

streamlit
pdfplumber
pandas
openpyxl

How to Run

Start the Streamlit app with the following command:

streamlit run app.py

Project Structure

📂 PDF-Table-Extractor
├── 📄 main.py       # Core functions for table extraction
├── 📄 app.py        # Streamlit UI
├── 📄 requirements.txt  # List of dependencies
├── 📄 README.md     # Project documentation

Usage

Run the application.

Upload a PDF file.

Extracted tables will be displayed.

Click on Download Excel File to save the results.

Troubleshooting

If no tables are extracted, ensure the PDF contains structured tables.

If you get an error "At least one sheet must be visible", update save_to_excel() to handle empty tables.

Contributing