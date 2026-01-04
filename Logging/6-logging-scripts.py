import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


file_logger = logging.FileHandler(filename="./Scripts/error_logs.log")
file_logger.setLevel(logging.INFO)
file_logger.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(lineno)s %(message)s"))


logger.addHandler(file_logger)



try:
    res = 5 / 0
except ZeroDivisionError as e:
    logger.exception(msg=f"DIVISION BY ZERO \n\n {e} \n\n")
