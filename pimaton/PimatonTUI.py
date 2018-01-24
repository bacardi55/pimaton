import logging

from PimatonUI import PimatonUI
from PimatonExceptions import PimatonExceptions

logging.basicConfig()
logger = logging.getLogger("Pimaton")


class PimatonTUI(PimatonUI, object):
    def __init__(self, pimaton):
        super(PimatonTUI, self).__init__(pimaton)

    def mainloop(self):
        while True:
            if self.is_triggered() is False:
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

    def is_triggered(self):
        if 'keyboard' in self.pimaton.config['pimaton']['inputs']:
            logger.debug('Waiting for start key to be pressed')
            # TODO: This will need to change for being able to manage both
            # keyboard and GPIO.
            input = raw_input("Press enter to start")
            return True
        else:
            # No other input compatible with TUI yet, raise an alert.
            raise PimatonTUIExceptions(
                'TUI mode has no compatible inputs configured.')


class PimatonTUIExceptions(PimatonExceptions):
    pass
