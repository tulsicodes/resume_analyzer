# Import logging module for application logging
import logging
# Import os module for file system operations
import os

def setup_logger(name, log_file, level=logging.DEBUG):
    """Set up and configure a logger with console and file handlers.
    
    Args:
        name (str): Name of the logger
        log_file (str): Path to the log file
        level (int): Logging level (default: logging.DEBUG)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create a logger instance with the specified name
    logger = logging.getLogger(name)
    
    # Set the logging level for the logger
    logger.setLevel(level)
    
    # Create the directory for the log file if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Create a console handler for logging to stdout
    console_handler = logging.StreamHandler()
    # Set the logging level for console output
    console_handler.setLevel(level)
    
    # Create a file handler for logging to the specified file
    file_handler = logging.FileHandler(log_file)
    # Set the logging level for file output
    file_handler.setLevel(level)
    
    # Define the log message format with timestamp, name, level, and message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Apply the formatter to both handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger only if they haven't been added yet
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    # Return the configured logger
    return logger