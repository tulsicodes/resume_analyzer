# Import os module for file system operations
import os

def save_text_to_file(text, output_path):
    """Save text to a file with UTF-8 encoding.
    
    Args:
        text (str): Text content to save
        output_path (str): Path where the file will be saved
    """
    # Open file in write mode with UTF-8 encoding
    with open(output_path, "w", encoding="utf-8") as file:
        # Write text to the file
        file.write(text)

def remove_file(file_path):
    """Remove a file if it exists.
    
    Args:
        file_path (str): Path to the file to be removed
    """
    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file if it exists
        os.remove(file_path)