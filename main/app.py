# Import os module for operating system interactions
import os
# Import sys module for system-specific parameters and functions
import sys
# Add parent directory to system path to allow importing from lib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import Streamlit library for web application
import streamlit as st
# Import TextProcessor class from custom lib module
from lib.text_processor import TextProcessor

def main():
    """Main function to run the Resume Analyzer web application."""
    # Display main title on the page
    st.title("Resume Analyzer")
    
    # Display subheader for file upload section
    st.subheader("Upload a PDF or Word Resume")
    
    # Create file uploader widget accepting PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Check if file is uploaded and extract button is clicked
    if uploaded_file and st.button("Extract Text"):
        # Get file extension from uploaded filename
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        # Define temporary file path for processing
        temp_path = f"temp_resume.{file_extension}"
        
        # Save uploaded file to temporary location
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Create instance of TextProcessor
        processor = TextProcessor()
        
        # Extract text using TextProcessor
        extracted_text = processor.extract_text(temp_path, file_extension)
        
        # Clean up temporary file
        os.remove(temp_path)
        
        # Display header for extracted text
        st.write("Extracted Text:")
        
        # Display extracted text in a scrollable text area
        st.text_area("Text", extracted_text, height=300)

# Standard Python idiom to run main function when script is executed
if __name__ == "__main__":
    main()