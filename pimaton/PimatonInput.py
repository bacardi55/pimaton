import abc
import logging

logging.basicConfig()
logger = logging.getLogger("Pimaton")


class PimatonInput:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_triggered(self):
        """ Indicate if the triggerd has been pressed. """


class PimatonInputKeyboard(PimatonInput):
    def is_triggered(self):
        logger.debug('Waiting for start key to be pressed')
        input = raw_input("Press enter to start")
        return True


class PimatonInputGPIO(PimatonInput):
    pass
