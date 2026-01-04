import logging

logger = logging.getLogger(name='my-script')
logger.setLevel(logging.DEBUG)

streamer = logging.StreamHandler()
streamer.setLevel(level=logging.INFO)
streamer.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))


file_logger = logging.FileHandler(filename='./Scripts/test.log')
file_logger.setLevel(level=logging.DEBUG)
file_logger.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s"))


logger.addHandler(streamer)
logger.addHandler(file_logger)




logger.debug("Debug goes only to file")
logger.info("Info goes to both console and file")