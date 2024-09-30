import logging

def configure_logging(logfile):
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the overall logging level

    # Create handlers
    file_handler = logging.FileHandler(logfile, encoding="utf-8")  # Logs to file
    console_handler = logging.StreamHandler()    # Logs to console

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)