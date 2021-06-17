import logging

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log_dir = './log/'

error_file_handler = logging.FileHandler("{}error.log".format(log_dir))
error_file_handler.setFormatter(formatter)

ipr_error_logger = logging.getLogger("iprcv_Err")
ipr_error_logger.setLevel(logging.ERROR)
ipr_error_logger.addHandler(error_file_handler)

inter_error_logger = logging.getLogger("interlocker_Err")
inter_error_logger.setLevel(logging.ERROR)
inter_error_logger.addHandler(error_file_handler)

interlocker_logger = logging.getLogger("interlocker")
interlocker_logger.setLevel(logging.INFO)

interlocker_handler = logging.FileHandler(
    ".{}}interlocker.log".format(log_dir))
interlocker_handler.setFormatter(formatter)
interlocker_logger.addHandler(interlocker_handler)

iprcv_logger = logging.getLogger("iprcv")
iprcv_logger.setLevel(logging.INFO)

iprcv_handler = logging.FileHandler("{}iprcv.log".format(log_dir))
iprcv_handler.setFormatter(formatter)
iprcv_logger.addHandler(iprcv_handler)
