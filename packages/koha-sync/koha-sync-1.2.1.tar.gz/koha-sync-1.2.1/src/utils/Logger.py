from .Singleton import Singleton


class Logger(Singleton):

    def __new__(cls, *args, **kwargs):
        return super(Logger, cls).__new__(cls, *args, **kwargs)


# logger.info('Verifying config file')
# logger.success('Verifying config file')
# logger.warning('Verifying config file')
# logger.error('Verifying config file')
# logger.critical('Verifying config file')
