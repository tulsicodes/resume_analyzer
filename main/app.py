# Import sys module for system path modifications
import sys
# Import os module for file system operations
import os
# Import Streamlit for web application interface
import streamlit as st
# Add parent directory to system path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Import GroqHandler for API interactions
from lib.groq_handler import GroqHandler
# Import TextProcessor for text extraction
from lib.text_processor import TextProcessor
# Import ResumeAnalyzer for resume analysis
from lib.resume_analyzer import ResumeAnalyzer
# Import Config for configuration settings
from utils.config import Config
# Import PromptLoader for prompt management
from utils.prompt_loader import PromptLoader

def main():
    """Main function to run the Resume Analyzer web application."""
    # Display application title
    st.title("Resume Analyzer")
    
    # Display subheader for file upload section
    st.subheader("Upload a PDF or Word Resume")
    
    # Create file uploader widget for PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Create three columns for input selections
    col1, col2, col3 = st.columns(3)
    
    # Designation selection in first column
    with col1:
        designation = st.selectbox("Select Desired Designation", 
                                 ["Data Scientist", "Data Analyst", "MLOps Engineer", 
                                  "Machine Learning Engineer"])
    
    # Experience level selection in second column
    with col2:
        experience = st.selectbox("Select Experience Level", 
                                ["Fresher", "<1 Year Experience", "1-2 Years Experience", 
                                 "2-5 Years Experience", "5-8 Years Experience", 
                                 "8-10 Years Experience"])
    
    # Domain selection in third column
    with col3:
        domain = st.selectbox("Select Domain", 
                            ["Finance", "Healthcare", "Automobile", "Real Estate"])
    
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
        text_processor = TextProcessor()
        extracted_text = text_processor.extract_text(temp_path, file_extension)
        
        # Remove temporary file
        os.remove(temp_path)
        
        # Proceed if text was extracted successfully
        if extracted_text:
            # Initialize GroqHandler for API calls
            grok_handler = GroqHandler()
            
            # Initialize PromptLoader with prompts file from Config
            prompt_loader = PromptLoader(Config.PROMPTS_FILE)
            
            # Initialize ResumeAnalyzer with handlers
            resume_analyzer = ResumeAnalyzer(grok_handler, prompt_loader)
            
            # Show spinner during analysis
            with st.spinner("Analyzing resume... Please wait"):
                # Analyze resume with selected parameters
                analysis = resume_analyzer.analyze_resume(extracted_text, 
                                                        designation, experience, domain)
            
            # Display analysis header
            st.markdown("# Resume Analysis")
            
            # Display analysis result
            st.write(analysis)
        else:
            # Display error if text extraction failed
            st.error("Could not extract text.")

# Standard Python idiom to run main function
if __name__ == "__main__":
    main()