import logging

def get_logger(name, level=logging.DEBUG) -> logging.Logger:
    FORMAT = "[%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s() - %(asctime)s]\n\t %(message)s \n"
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    FILENAME = './log.log'
    # FILENAME_SQLALCHEMY = './sqlalchemy.log'
    # FILENAME_UVICORN = 'wlog/uvicorn.log'


    # if name == 'sqlalchemy.engine.Engine':
    #     logging.basicConfig(format=FORMAT, datefmt=TIME_FORMAT, level=level, filename=FILENAME_UVICORN)
    #     logger = logging.getLogger(name)

    # # elif name == 'sqlalchemydsd':
    # #     logging.basicConfig(format=FORMAT, datefmt=TIME_FORMAT, level=level, filename=FILENAME_SQLALCHEMY)
    # #     logger = logging.getLogger(name)

    # else:
    logging.basicConfig(format=FORMAT, datefmt=TIME_FORMAT, level=level, filename=FILENAME)
    logger = logging.getLogger(name)

    return logger