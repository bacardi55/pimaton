from PimatonCam import PimatonCam 
from time import time, sleep, strftime

import yaml
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

    def set_config(self, config_file=None):
        """
        Class method to set the configuration of the application
        """
        # TODO v0.0.1 : Manage configuration.
        if config_file is None:
            config_file = './assets/default_config.yaml'
            logging.debug('No given config, loading default one %s' % config_file)

        # Overriding all config, so be sure when not using default one :).
        self.config = self.load_config(config_file)
        logger.debug('self config = %s' % self.config)
        
    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            data = yaml.load(f)

        logger.debug("Loaded configuration: %s" % data)

        return data


    def __get_fullpath_thumbnails_list(self, taken_pictures):
        fpp = []
        for pic in taken_pictures:
            fpp.append(self.config['picamera']['photo_directory'] + '/' + pic)

        return fpp
