import logging


class UserFilter(logging.Filter):
    def filter(self, record):
        return True
