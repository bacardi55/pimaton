from six import with_metaclass
from Singleton import Singleton
import logging

logging.basicConfig()
logger = logging.getLogger("Pimaton")

class PimatonImage(with_metaclass(Singleton, object)):
    """
    Class that handles the image manipulation capabilities for the Pimaton app.
    """
    def __init__(self):
        logger.debug('Instantiate PimatonImage')

    def render_image_to_print(self, taken_pictures, output_dir, filename):
        logger.info('Generating image to be printed: %s/%s' % (output_dir, filename))
        logger.debug('Taken Pictures: %s' % taken_pictures)
        # TODO v0.0.1 : Create the 1 picture with the taken picture.
        # TODO v0.0.1 : Benchamark between using Pillow library or an imagemagick wrapper.
