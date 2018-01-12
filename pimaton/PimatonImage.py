from six import with_metaclass
from Singleton import Singleton
import logging

from PIL import Image, ImageDraw, ImageFont
import math

logging.basicConfig()
logger = logging.getLogger("Pimaton")

class PimatonImage(with_metaclass(Singleton, object)):
    """
    Class that handles the image manipulation capabilities for the Pimaton app.
    """
    def __init__(self):
        logger.debug('Instantiate PimatonImage')

    def render_image_to_print(self, taken_pictures, filename, config):
        """
        This method create the final image to be printed.
        """

        logger.info('Generating image to be printed: %s/%s' % (config['print_pic']['output_dir'], filename))
        logger.debug('Taken Pictures: %s' % taken_pictures)

        dimensions = self.__calculate_dimensions(config)

        thumbnails = []
        for file in taken_pictures:
            try:
                # TODO: change path via config.
                im = Image.open(file)
                im.thumbnail(dimensions['thumbnail_size'])
                thumbnails.append(im)
                # im.save('./thumbnail_' + file, "JPEG")

            except IOError as e:
                # TODO
                print("Error: %s" % e)

        logger.debug(config['print_pic']['template'])
        if config['print_pic']['template'] is not None:
            # TODO: Check if file exists or raise exception.
            logger.debug("Loading template file: %s" % config['print_pic']['template'])
            generated = Image.open(config['print_pic']['template'])
        else:
            logger.debug("No template file, creating empty image")
            generated = Image.new('RGB', dimensions['print_pic_size'], 'white')

        for idx, thumbnail in enumerate(thumbnails):
            current_col = idx % config['print_pic']['cols'] + 1
            current_row = int(math.floor((idx / config['print_pic']['cols']))) + 1
            x_position = (current_col * dimensions['x_border']) + ((current_col - 1) * config['thumbnails']['width']) 
            y_position = (current_row * dimensions['y_border']) + ((current_row - 1) * config['thumbnails']['height'])
            generated.paste(thumbnail, (x_position, y_position))
     
            # TODO: TMP code to be removed.
            tmp = ImageDraw.Draw(generated)
            tmp.rectangle([(x_position, y_position), (x_position + config['thumbnails']['width'], y_position + config['thumbnails']['height'])], outline="black")

        
        # TODO: change path via config.
        generated.save(config['print_pic']['output_dir'] + '/' + filename, 'JPEG')
        logger.debug('Final picture has been generated')


    def __calculate_dimensions(self, config):
        """
        This private method calculate different variables needed to create the final image
        """
        logger.debug('Calculating dimensions with these values: %s' % config)
        # TODO: Add try to make sure numbers are right
        dim = {
            'thumbnail_size': (config['thumbnails']['width'], config['thumbnails']['height']),
            'print_pic_size': (config['print_pic']['width'], config['print_pic']['height']),
            'x_border': (config['print_pic']['width'] - config['print_pic']['cols'] * config['thumbnails']['width']) / (config['print_pic']['cols'] + 1),
            'y_border': (config['print_pic']['height'] - config['print_pic']['rows'] * config['thumbnails']['height']) / (config['print_pic']['rows'] + 1)
        }

        logger.debug('Calculated dimensions: %s' % dim)
        return dim
