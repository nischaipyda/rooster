import logging


class Logger:

    @classmethod
    def get_logger(cls, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
        file_handler = logging.FileHandler('./logs/parser3.log')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger
