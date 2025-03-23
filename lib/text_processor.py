# Import PyMuPDF library for PDF processing
import fitz  # PyMuPDF

# Import Document class from python-docx library for Word document processing
from docx import Document

class TextProcessor:
    """A class to process and extract text from PDF and DOCX files."""
    
    def __init__(self):
        """Initialize the TextProcessor class."""
        # Empty constructor as no initialization is needed
        pass

    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from all pages
        """
        # Open the PDF file
        doc = fitz.open(pdf_path)
        # Extract text from each page and join with newlines
        text = "\n".join([page.get_text("text") for page in doc])
        # Close the document to free resources
        doc.close()
        # Return the extracted text
        return text

    def extract_text_from_docx(self, docx_path):
        """Extract text from a DOCX file.
        
        Args:
            docx_path (str): Path to the DOCX file
            
        Returns:
            str: Extracted text from all paragraphs
        """
        # Open the Word document
        doc = Document(docx_path)
        # Extract text from each paragraph and join with newlines
        text = "\n".join([para.text for para in doc.paragraphs])
        # Return the extracted text
        return text

    def extract_text(self, file_path, file_extension):
        """Extract text based on file extension.
        
        Args:
            file_path (str): Path to the file
            file_extension (str): File extension ('pdf' or 'docx')
            
        Returns:
            str: Extracted text or empty string if extension not supported
        """
        # Check file extension and call appropriate extraction method
        if file_extension == "pdf":
            return self.extract_text_from_pdf(file_path)
        elif file_extension == "docx":
            return self.extract_text_from_docx(file_path)
        # Return empty string for unsupported file types
        return ""