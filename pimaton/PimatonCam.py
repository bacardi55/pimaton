from picamera import PiCamera
from time import sleep, strftime
import datetime
import logging

logging.basicConfig()
logger = logging.getLogger("Pimaton")

class PimatonCam:
    """
    Class that handles the PiCamera for the Pimaton app
    """

    config = {}

    def __init__(self, config):
        self.picamera = PiCamera()
        self.config_picamera()
        logger.debug('Instanciating PimatonCam with config %s' % config)
        self.config = config

    def take_pictures(self, unique_key):
	"""
	This function takes picture via the pi camera
	"""
        logger.debug("Starting taking picture")
        taken_pictures = []
        for i in range(self.config['number_of_pictures_to_take']):  
            filename = self.config['picture_prefix_name'] + "_" + unique_key + '_' + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + ".jpg"
            taken_pictures.append(filename)

            sleep(self.config['time_between_pictures'])
	    self.capture(filename)
            logger.debug("Photo (" + filename + ") saved: " + filename)

        logger.debug("The following pictures were taken %s" % taken_pictures)
        return taken_pictures

    def capture(self, filename):
        logger.debug("Capturing picture %s in %s" % (filename, self.config['photo_directory']))
        # TODO v0.0.1 : Manage exception.
        self.picamera.capture(self.config['photo_directory'] + '/' + filename)

    def config_picamera(self):
        logger.debug('Configuring Pi Camera')
        logger.debug('No config passed, default config used')
        # TODO v0.0.1 : Manage camera configuration.

