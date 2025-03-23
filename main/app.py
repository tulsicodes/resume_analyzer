# Import the Streamlit library for creating web applications
import streamlit as st

# Define the main function that runs the application
def main():
    # Display a title on the web page
    st.title("Resume Analyzer")
    
    # Display a subheader below the title
    st.subheader("Upload a PDF or Word Resume")
    
    # Create a file uploader widget that accepts PDF and Word documents
    # Returns the uploaded file object or None if no file is uploaded
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    
    # Check if a file has been uploaded
    if uploaded_file:
        # Display the name of the uploaded file
        st.write("File uploaded:", uploaded_file.name)
        
        # Display a placeholder message indicating future functionality
        st.write("Text extraction coming soon!")

# Standard Python idiom to run the main function when script is executed
if __name__ == "__main__":
    main()