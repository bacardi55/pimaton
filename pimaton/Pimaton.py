from PimatonCam import PimatonCam 
from time import sleep, strftime
import datetime
import logging

from PimatonImage import PimatonImage

logging.basicConfig()
logger = logging.getLogger("Pimaton")

class Pimaton:
    """
    This Class is the main Pimaton class that manage the whole application.
    """

    def __init__(self):
        logger.debug('Instantiate Pimaton class')
        self.config = {}

    def run(self):
        """
        Class method that run the main loop of the application.
        """
        pimatoncam = PimatonCam(config=self.config['picamera'])

        while True:
            # TODO v0.0.2 : Manage button to start taking picture.
            logger.debug('In Loop')
	    taken_pictures = pimatoncam.take_pictures()

            if len(taken_pictures) != self.config['picamera']['number_of_pictures_to_take']:
                logger.warning("The number of taken pictures is incorrect")
                # TODO v0.0.1 : Manage Exception.
                return False

            # TODO v0.0.1 : Manage exception.
            filename = self.config['picamera']['generated_prefix_name'] + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + ".jpg"
            to_print = PimatonImage().render_image_to_print(taken_pictures, self.config['picamera']['photo_directory'], filename)

            # TODO v0.0.3 : Manage print.
            # pimatonprint = PimatonPrint()

            logger.debug('Sleeping %s second' % self.config['pimaton']['time_between_loop'])
	    sleep(self.config['pimaton']['time_between_loop'])

    def set_config(self, config):
        """
        Class method to set the configuration of the application
        """
        logger.debug('Set configuration')
        # TODO v0.0.1 : Manage configuration.
        config = {
            'picamera': {
                'photo_directory': '/home/pi/pimaton_pictures',
                'number_of_pictures_to_take': 3,
                'time_before_first_picture': 4,
                'time_between_pictures': 2,
                'picture_prefix_name': 'test_pimaton',
                'generated_prefix_name': 'pimaton_'
            },
            'pimaton': {
                'time_between_loop': 2
            }
        }
        logging.debug('Loading default config %s' % config)
        self.config = config
        
