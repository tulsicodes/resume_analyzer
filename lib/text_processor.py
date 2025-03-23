# Import PyMuPDF library for PDF processing
import fitz
# Import Document class from python-docx for Word document processing
from docx import Document

class TextProcessor:
    """Class to process and extract text from PDF and DOCX files with logging."""
    
    def __init__(self, logger):
        """Initialize TextProcessor with a logger instance.
        
        Args:
            logger (logging.Logger): Logger instance for logging operations
        """
        # Store the logger instance
        self.logger = logger

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file with logging.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from all pages
            
        Raises:
            Exception: If text extraction fails
        """
        # Log the start of PDF text extraction
        self.logger.debug("Extracting text from PDF: %s", pdf_path)
        try:
            # Open the PDF file
            doc = fitz.open(pdf_path)
            # Extract text from each page and join with newlines
            text = "\n".join([page.get_text("text") for page in doc])
            # Close the document
            doc.close()
            # Log successful extraction
            self.logger.debug("Text extracted from PDF: %s", pdf_path)
            return text
        except Exception as e:
            # Log error if extraction fails
            self.logger.error("Error extracting text from PDF %s: %s", pdf_path, str(e))
            # Raise exception with error message
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def extract_text_from_docx(self, docx_path):
        """Extract text from a DOCX file with logging.
        
        Args:
            docx_path (str): Path to the DOCX file
            
        Returns:
            str: Extracted text from all paragraphs
            
        Raises:
            Exception: If text extraction fails
        """
        # Log the start of DOCX text extraction
        self.logger.debug("Extracting text from DOCX: %s", docx_path)
        try:
            # Open the Word document
            doc = Document(docx_path)
            # Extract text from each paragraph and join with newlines
            text = "\n".join([para.text for para in doc.paragraphs])
            # Log successful extraction
            self.logger.debug("Text extracted from DOCX: %s", docx_path)
            return text
        except Exception as e:
            # Log error if extraction fails
            self.logger.error("Error extracting text from DOCX %s: %s", docx_path, str(e))
            # Raise exception with error message
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    def extract_text(self, file_path, file_extension):
        """Extract text based on file extension with logging.
        
        Args:
            file_path (str): Path to the file
            file_extension (str): File extension ('pdf' or 'docx')
            
        Returns:
            str: Extracted text or empty string if extension not supported
        """
        # Log the start of text extraction
        self.logger.debug("Extracting text from file: %s", file_path)
        # Handle PDF files
        if file_extension == "pdf":
            return self.extract_text_from_pdf(file_path)
        # Handle DOCX files
        elif file_extension == "docx":
            return self.extract_text_from_docx(file_path)
        # Log warning for unsupported extensions
        self.logger.warning("Unsupported file extension: %s", file_extension)
        # Return empty string for unsupported files
        return ""