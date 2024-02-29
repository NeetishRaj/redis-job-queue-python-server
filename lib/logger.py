import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define log message format
    filename="app.log",  # Specify the filename for the log file
    filemode="a",
)  # Append mode: logs will be appended to the file

# Create a logger object
logger = logging.getLogger()

# Log some messages

# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')