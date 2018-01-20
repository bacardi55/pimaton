import abc
import logging

logging.basicConfig()
logger = logging.getLogger("Pimaton")


class PimatonUI():
    __metaclass__ = abc.ABCMeta

    def __init__(self, pimaton):
        self.pimaton = pimaton

    @abc.abstractmethod
    def mainloop(self):
        pass
