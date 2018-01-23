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

            unique_key = self.pimaton.get_unique_key()
            taken_pictures = self.pimaton.take_pictures(unique_key)
            filename = self.pimaton.get_filename(unique_key)
            to_print = self.pimaton.generate_picture(
                    taken_pictures,
                    filename)
            self.pimaton.print_picture(to_print)
            self.pimaton.wait_before_next_iteration()
