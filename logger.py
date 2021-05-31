import logging

error_logger = logging.getLogger("error")
error_logger.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


error_file_handler = logging.FileHandler("./log/error.log")
error_file_handler.setFormatter(formatter)
error_logger.addHandler(error_file_handler)


