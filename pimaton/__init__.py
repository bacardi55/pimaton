from time import sleep
import logging

logging.basicConfig()
logger = logging.getLogger("Pimaton")

from .Pimaton import Pimaton
from .PimatonCam import PimatonCam
from .PimatonImage import PimatonImage
from .Singleton import Singleton
from ._version import version_str

def main():
    """
    Main program loop
    """
    # TODO : Manage --debug
    configure_logging(True)
    logger.info('Welcome to pimaton!')

    # TODO v0.0.1 : Manage arguments

    pimaton = Pimaton()
    # configure
    logger.info('Starting configuring Pimaton')
    # TODO v0.0.1 : Add possibility to give alternative config file.
    pimaton.set_config()

    # start app
    logger.info('Starting Pimaton')
    pimaton.run()

def configure_logging(debug=None):
    """
    Prepare log folder in current home directory.
    :param debug: If true, set the lof level to debug
    """
    logger = logging.getLogger("Pimaton")
    logger.addFilter(AppFilter())
    logger.propagate = False

    formatter = logging.Formatter('%(asctime)s :: %(app_version)s :: %(message)s', "%Y-%m-%d %H:%M:%S")

    syslog = logging.StreamHandler()
    syslog.setLevel(logging.DEBUG)
    syslog.setFormatter(formatter)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # add the handlers to logger
    logger.addHandler(syslog)

    logger.debug("Logger ready")


class AppFilter(logging.Filter):
    """
    Class used to add a custom entry into the logger
    """
    def filter(self, record):
        record.app_version = "Pimaton-%s" % version_str
        return True

