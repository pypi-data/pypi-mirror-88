import logging, sys

def error(message):
    """print error in logger, then wait for input and exit"""
    logging.error(message)
    input('press enter to quit')
    sys.exit(message)