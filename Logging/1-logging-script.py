import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s :: %(levelname)s :: %(message)s"
)

logger = logging.getLogger(name="__name__")

logger.debug(msg="debug")
logger.info(msg="INFO")
logger.warning(msg="warning")
logger.error(msg="error")
logger.critical(msg="critical")