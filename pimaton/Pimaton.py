from PimatonCam import PimatonCam 
from time import time, sleep, strftime
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
            unique_key = str(int(time()))
	    taken_pictures = pimatoncam.take_pictures(unique_key)

            if len(taken_pictures) != self.config['picamera']['number_of_pictures_to_take']:
                logger.warning("The number of taken pictures is incorrect")
                # TODO v0.0.1 : Manage Exception.
                return False

            # TODO v0.0.1 : Manage exception.
            filename = self.config['picamera']['generated_prefix_name'] + '_' + unique_key + '_' + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + ".jpg"
            to_print = PimatonImage().render_image_to_print(self.__get_fullpath_thumbnails_list(taken_pictures), filename, self.config['image'])

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
                'number_of_pictures_to_take': 6,
                'time_before_first_picture': 2,
                'time_between_pictures': 1,
                'picture_prefix_name': 'test_pimaton',
                'generated_prefix_name': 'pimaton_'
            },
            'pimaton': {
                'time_between_loop': 2
            },
            'image': {
                'print_pic': {
                    'template': None,
                    'output_dir': '/home/pi/pimaton_pictures',
                    'width': 1754,
                    'height': 1241,
                    'rows': 3,
                    'cols': 2
                },
                'thumbnails': {
                    'width': 560,
                    'height': 496
                },
            }
        }

        logging.debug('Loading default config %s' % config)
        self.config = config
        
    def __get_fullpath_thumbnails_list(self, taken_pictures):
        fpp = []
        for pic in taken_pictures:
            fpp.append(self.config['picamera']['photo_directory'] + '/' + pic)

        return fpp
