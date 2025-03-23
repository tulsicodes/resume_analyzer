# Import sys module for system path modifications
import sys
# Import os module for file system operations
import os
# Import Streamlit for web application interface
import streamlit as st

# Add the project root directory to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import custom classes from respective modules
from lib.groq_handler import GroqHandler
from lib.text_processor import TextProcessor
from lib.resume_analyzer import ResumeAnalyzer
from utils.config import Config
from utils.logger import setup_logger
from utils.prompt_loader import PromptLoader

# Singleton logger setup (runs only once during session)
if 'loggers' not in st.session_state:
    # Validate configuration settings once
    Config.validate()
    # Initialize loggers dictionary in session state
    st.session_state.loggers = {
        "app": setup_logger("app", f"{Config.LOG_DIR}/app.log"),
        "groq_handler": setup_logger("groq_handler", f"{Config.LOG_DIR}/groq_handler.log"),
        "prompt_loader": setup_logger("prompt_loader", f"{Config.LOG_DIR}/prompt_loader.log"),
        "resume_analyzer": setup_logger("resume_analyzer", f"{Config.LOG_DIR}/resume_analyzer.log"),
        "text_processor": setup_logger("text_processor", f"{Config.LOG_DIR}/text_processor.log")
    }
    # Log application start
    st.session_state.loggers["app"].debug("Starting Resume Analyzer application")

# Reference to loggers from session state
loggers = st.session_state.loggers

def main():
    """Main function to run the Streamlit Resume Analyzer app."""
    # Display application title
    st.title("Resume Analyzer")
    
    # Display subheader for file upload section
    st.subheader("Upload a PDF or Word Resume")
    
    # Create file uploader widget for PDF and DOCX files
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Create three columns for input selections
    col1, col2, col3 = st.columns(3)
    
    # Designation selection dropdown in first column
    with col1:
        designation = st.selectbox("Select Desired Designation", 
                                 ["Data Scientist", "Data Analyst", "MLOps Engineer", 
                                  "Machine Learning Engineer"])
    
    # Experience level selection dropdown in second column
    with col2:
        experience = st.selectbox("Select Experience Level", 
                                ["Fresher", "<1 Year Experience", "1-2 Years Experience", 
                                 "2-5 Years Experience", "5-8 Years Experience", 
                                 "8-10 Years Experience"])
    
    # Domain selection dropdown in third column
    with col3:
        domain = st.selectbox("Select Domain", 
                            ["Finance", "Healthcare", "Automobile", "Real Estate"])
    
    # Process when analyze button is clicked and file is uploaded
    if st.button("Analyze") and uploaded_file:
        # Log user action
        loggers["app"].debug("User clicked Analyze button for file: %s", uploaded_file.name)
        # Extract file extension
        file_extension = uploaded_file.name.split(".")[-1].lower()
        # Define temporary file path
        temp_path = f"temp_resume.{file_extension}"
        try:
            # Save uploaded file temporarily
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Initialize TextProcessor with its logger
            text_processor = TextProcessor(loggers["text_processor"])
            # Extract text from file
            extracted_text = text_processor.extract_text(temp_path, file_extension)
            # Remove temporary file
            os.remove(temp_path)
            
            # Proceed if text was extracted
            if extracted_text:
                # Initialize GroqHandler with its logger and prompt loader
                grok_handler = GroqHandler(loggers["groq_handler"], 
                                         PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))
                # Initialize ResumeAnalyzer with its components
                resume_analyzer = ResumeAnalyzer(grok_handler, loggers["resume_analyzer"], 
                                               PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))
                # Show spinner during analysis
                with st.spinner("Analyzing resume... Please wait"):
                    # Perform resume analysis
                    analysis = resume_analyzer.analyze_resume(extracted_text, designation, 
                                                            experience, domain)
                # Display analysis results
                st.markdown("# Resume Analysis")
                st.write(analysis)
            else:
                # Display and log error if text extraction fails
                st.error("Could not extract text.")
                loggers["app"].error("Failed to extract text from %s", uploaded_file.name)
        except Exception as e:
            # Log and display any processing errors
            loggers["app"].error("Error processing resume: %s", str(e))
            st.error(f"Error processing resume: {str(e)}")
            # Clean up temporary file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)

# Standard Python idiom to run main function
if __name__ == "__main__":
    main()