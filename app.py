import streamlit as st
import pandas as pd
from collections import Counter
import string
from io import BytesIO
import fitz  # PyMuPDF for PDF text extraction

# Set the page title and layout
st.set_page_config(page_title="PDF Letter & Word Frequency Analyzer", layout="centered")

# Title and Instructions
st.title("PDF Letter & Word Frequency Analyzer")
st.write("Upload a PDF document to analyze the frequency of each English letter (A-Z) and word count.")

# File uploader for PDF
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_file):
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf_document:
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
    return text

# Function to analyze letter frequency
def analyze_letter_frequency(text):
    # Filter only alphabetic characters and convert to uppercase
    text = ''.join([char.upper() for char in text if char.isalpha()])
    # Count the frequency of each letter
    frequency = Counter(text)
    # Ensure all letters from A to Z are included in the result with a frequency of 0 if missing
    frequency = {letter: frequency.get(letter, 0) for letter in string.ascii_uppercase}
    return frequency

# Function to analyze word frequency
def analyze_word_count(text):
    # Remove punctuation and split text into words
    words = ''.join([char if char.isalnum() else ' ' for char in text]).split()
    word_count = Counter(words)
    return word_count

# Process the PDF file if uploaded
if uploaded_file:
    # Extract text from the uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    # Analyze letter frequency from the extracted text
    letter_frequency_data = analyze_letter_frequency(pdf_text)
    letter_frequency_df = pd.DataFrame(list(letter_frequency_data.items()), columns=["Letter", "Frequency"])
    letter_frequency_df = letter_frequency_df.sort_values("Letter").reset_index(drop=True)
    
    # Analyze word count from the extracted text
    word_count_data = analyze_word_count(pdf_text)
    word_count_df = pd.DataFrame(word_count_data.items(), columns=["Word", "Count"]).sort_values(by="Count", ascending=False).reset_index(drop=True)
    
    # Display frequency tables
    st.write("### Letter Frequency Table")
    st.write("You can copy and paste this table into a spreadsheet.")
    st.dataframe(letter_frequency_df)
    
    st.write("### Word Count Table")
    st.write("This table shows the count of each word found in the PDF.")
    st.dataframe(word_count_df)
    
    

    
else:
    st.write("Please upload a PDF file to analyze.")
