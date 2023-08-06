import logging


def init_logger():
    logger = logging.getLogger("Py2Crawl")
    logger.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    return logger


LOGGER = init_logger()
