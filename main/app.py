# Import sys module for system path modifications
import sys
# Import os module for file system operations
import os
# Import Streamlit for web application interface
import streamlit as st

# Add the project root directory to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import custom classes and utilities from respective modules
from lib.groq_handler import GroqHandler
from lib.text_processor import TextProcessor
from lib.resume_analyzer import ResumeAnalyzer
from utils.file_utils import save_text_to_file, remove_file
from utils.logger import setup_logger
from utils.config import Config
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

# Cache components to prevent re-initialization
@st.cache_resource
def get_grok_handler():
    """Initialize and cache GroqHandler instance."""
    return GroqHandler(loggers["groq_handler"], PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))

@st.cache_resource
def get_text_processor():
    """Initialize and cache TextProcessor instance."""
    return TextProcessor(loggers["text_processor"])

@st.cache_resource
def get_resume_analyzer(_grok_handler):
    """Initialize and cache ResumeAnalyzer instance.
    
    Args:
        _grok_handler: Cached GroqHandler instance
    """
    return ResumeAnalyzer(_grok_handler, loggers["resume_analyzer"], PromptLoader(Config.PROMPTS_FILE, loggers["prompt_loader"]))

# Initialize cached components
grok_handler = get_grok_handler()
text_processor = get_text_processor()
resume_analyzer = get_resume_analyzer(grok_handler)

def main():
    """Main function to run the Streamlit Resume Analyzer app."""
    # Initialize session state variables if not present
    if 'page' not in st.session_state:
        st.session_state.page = "upload"
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None
    if 'processed' not in st.session_state:
        st.session_state.processed = False

    # Upload page logic
    if st.session_state.page == "upload":
        st.title("Resume Analyzer")
        st.subheader("Upload a PDF or Word Resume")

        # File uploader widget
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
        
        # Create three columns for input selections
        col1, col2, col3 = st.columns(3)
        with col1:
            designation = st.selectbox("Select Desired Designation", 
                                     ["Data Scientist", "Data Analyst", "MLOps Engineer", 
                                      "Machine Learning Engineer"])
        with col2:
            experience = st.selectbox("Select Experience Level", 
                                    ["Fresher", "<1 Year Experience", "1-2 Years Experience", 
                                     "2-5 Years Experience", "5-8 Years Experience", 
                                     "8-10 Years Experience"])
        with col3:
            domain = st.selectbox("Select Domain", 
                                ["Finance", "Healthcare", "Automobile", "Real Estate"])

        # Handle analyze button click
        if st.button("Analyze") and uploaded_file:
            loggers["app"].debug("User clicked Analyze button for file: %s", uploaded_file.name)
            # Store inputs in session state and switch page
            st.session_state.uploaded_file = uploaded_file
            st.session_state.designation = designation
            st.session_state.experience = experience
            st.session_state.domain = domain
            st.session_state.page = "results"
            st.session_state.processed = False
            st.rerun()

    # Results page logic
    elif st.session_state.page == "results":
        uploaded_file = st.session_state.uploaded_file
        file_extension = uploaded_file.name.split(".")[-1].lower()
        temp_path = f"temp_resume.{file_extension}"

        try:
            # Process file only if not already processed
            if not st.session_state.processed:
                loggers["app"].debug("Processing uploaded file: %s", uploaded_file.name)
                # Save uploaded file temporarily
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # Extract text
                extracted_text = text_processor.extract_text(temp_path, file_extension)
                # Clean up temporary file
                remove_file(temp_path)

                if extracted_text:
                    loggers["app"].debug("Text extracted successfully, length: %d characters", len(extracted_text))
                    with st.spinner("Analyzing resume... Please wait"):
                        # Perform analysis and store in session state
                        st.session_state.analysis = resume_analyzer.analyze_resume(
                            extracted_text, st.session_state.designation, 
                            st.session_state.experience, st.session_state.domain
                        )
                        st.session_state.processed = True
                    loggers["app"].debug("Resume analysis completed")
                else:
                    st.error("Could not extract text. Please check the file format.")
                    loggers["app"].error("Failed to extract text from %s", uploaded_file.name)

            # Display results if analysis exists
            if st.session_state.analysis:
                # Button to return to upload page
                if st.button("Upload New Resume"):
                    loggers["app"].debug("User clicked Upload New Resume")
                    st.session_state.page = "upload"
                    st.session_state.analysis = None
                    st.session_state.processed = False
                    st.rerun()

                # Display analysis
                st.markdown("# Resume Analysis")
                st.write(st.session_state.analysis)

                # Save analysis to file and provide download option
                output_filename = "resume_analysis.txt"
                save_text_to_file(st.session_state.analysis, output_filename)
                with open(output_filename, "rb") as file:
                    st.download_button(label="Download Analysis", data=file, 
                                     file_name=output_filename, mime="text/plain")
                remove_file(output_filename)

        except Exception as e:
            # Handle and log any errors during processing
            loggers["app"].error("Error processing resume: %s", str(e))
            st.error(f"Error processing resume: {str(e)}")
            remove_file(temp_path)

if __name__ == "__main__":
    main()