import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

error_file_handler = logging.FileHandler("./log/error.log")
error_file_handler.setFormatter(formatter)

ipr_error_logger = logging.getLogger("iprcv_Err")
ipr_error_logger.setLevel(logging.ERROR)
ipr_error_logger.addHandler(error_file_handler)

inter_error_logger = logging.getLogger("interlocker_Err")
inter_error_logger.setLevel(logging.ERROR)
inter_error_logger.addHandler(error_file_handler)

interlocker_logger = logging.getLogger("interlocker")
interlocker_logger.setLevel(logging.INFO)

interlocker_handler = logging.FileHandler("./log/interlocker.log")
interlocker_handler.setFormatter(formatter)
interlocker_logger.addHandler(interlocker_handler)

iprcv_logger = logging.getLogger("iprcv")
iprcv_logger.setLevel(logging.INFO)

iprcv_handler = logging.FileHandler("./log/iprcv.log")
iprcv_handler.setFormatter(formatter)
iprcv_logger.addHandler(iprcv_handler)