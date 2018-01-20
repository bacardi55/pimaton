import logging
from PimatonUI import PimatonUI

logging.basicConfig()
logger = logging.getLogger("Pimaton")


class PimatonTUI(PimatonUI, object):
    def __init__(self, pimaton):
        super(PimatonTUI, self).__init__(pimaton)

    def mainloop(self):
        while True:
            if self.pimaton.pimatoninput.is_triggered() is False:
                continue

            logger.info(
                '*** Pimaton trigger has been pressed, starting taking pictures!')
            self.pimaton.run()
