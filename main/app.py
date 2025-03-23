# Import os module for file system operations
import os
# Import sys module for system path modifications
import sys
# Add parent directory to system path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import Streamlit for web application interface
import streamlit as st
# Import TextProcessor for text extraction from files
from lib.text_processor import TextProcessor
# Import GroqHandler for text analysis via Groq API
from lib.groq_handler import GroqHandler

def main():
    """Main function to run the Resume Analyzer web application."""
    # Display application title
    st.title("Resume Analyzer")
    
    # Display subheader for file upload section
    st.subheader("Upload a PDF or Word Resume")
    
    # Create file uploader widget for PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Check if file is uploaded and analyze button is clicked
    if uploaded_file and st.button("Analyze"):
        # Extract file extension from filename
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        # Define temporary file path
        temp_path = f"temp_resume.{file_extension}"
        
        # Save uploaded file temporarily
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Create TextProcessor instance and extract text
        processor = TextProcessor()
        extracted_text = processor.extract_text(temp_path, file_extension)
        
        # Remove temporary file
        os.remove(temp_path)
        
        # Proceed if text was successfully extracted
        if extracted_text:
            # Create GroqHandler instance for analysis
            groq = GroqHandler()
            
            # Define analysis prompt
            prompt = "Analyze this resume text and summarize its key points."
            
            # Show spinner during analysis
            with st.spinner("Analyzing..."):
                # Get analysis from Groq API
                analysis = groq.analyze_text(prompt, extracted_text)
            
            # Display analysis header
            st.write("Analysis:")
            
            # Display analysis in markdown format
            st.markdown(analysis)
        else:
            # Display error if no text was extracted
            st.error("No text extracted from the file.")

# Standard Python idiom to run main function
if __name__ == "__main__":
    main()