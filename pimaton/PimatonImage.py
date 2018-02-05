from six import with_metaclass
from Singleton import Singleton
import logging
import os

from PIL import Image, ImageDraw, ImageFont
import math

from PimatonExceptions import PimatonImageExceptions

logging.basicConfig()
logger = logging.getLogger("Pimaton")


class PimatonImage(with_metaclass(Singleton, object)):
    """
    Class that handles the image manipulation capabilities for the Pimaton app.
    """

    dimensions = {}

    def __init__(self, config):
        logger.debug('Instantiate PimatonImage with config = %s' % config)
        self.config = config
        self.dimensions = self.__calculate_dimensions(config)

    def render_image_to_print(self, taken_pictures, filename, config):
        """
        This method create the final image to be printed.
        """

        logger.info('Generating image to be printed: %s/%s' %
                    (config['print_pic']['output_dir'], filename))
        logger.debug('Taken Pictures: %s' % taken_pictures)

        thumbnails = []
        for file in taken_pictures:
            im = Image.open(file)
            im.thumbnail(self.dimensions['thumbnail_size'])
            thumbnails.append(im)

        if config['print_pic']['template'] is not None and len(
                config['print_pic']['template']) > 0:
            logger.debug(
                "Loading template file: %s" %
                config['print_pic']['template'])
            if os.path.exists(config['print_pic']['template']) is False:
                logger.warning(
                    'Template file given doesnt exists, creating empty image')
                generated = self.__create_new_image(
                    self.dimensions['print_pic_size'])
            else:
                generated = Image.open(config['print_pic']['template'])
        else:
            generated = self.__create_new_image(
                self.dimensions['print_pic_size'])

        for idx, thumbnail in enumerate(thumbnails):
            positions = self.__get_positions(idx, config, self.dimensions)
            generated.paste(thumbnail, positions)

        generated.save(
            config['print_pic']['output_dir'] +
            '/' +
            filename,
            'JPEG')
        logger.debug('Final picture has been generated')

    def __calculate_dimensions(self, config):
        """
        This private method calculate different variables needed to create the final image
        """
        logger.debug('Calculating dimensions with these values: %s' % config)
        try:
            dim = {
                'thumbnail_size': (
                    config['thumbnails']['width'],
                    config['thumbnails']['height']),
                'print_pic_size': (
                    config['print_pic']['width'],
                    config['print_pic']['height']),
                'x_border': (
                    config['print_pic']['width'] -
                    config['print_pic']['cols'] *
                    config['thumbnails']['width']) /
                (
                    config['print_pic']['cols'] +
                    1),
                'y_border': (
                    config['print_pic']['height'] -
                    config['print_pic']['rows'] *
                    config['thumbnails']['height']) /
                (
                    config['print_pic']['rows'] +
                    1)}
        except Exception as e:
            raise PimatonImageExceptions(
                'Cant calculate picture dimensions, something wrong: %s' % e)

        if dim['x_border'] < 0 or dim['y_border'] < 0:
            raise PimatonImageExceptions(
                'X or Y border calculation went wrong, check dimension')

        logger.debug('Calculated dimensions: %s' % dim)
        return dim

    def __create_new_image(self, dimensions):
        logger.debug("Creating empty default image")
        # TODO: Put the background color configurable.
        # Not sure if that's needed with the whole template concept.
        return Image.new('RGB', dimensions, 'white')

    def __get_positions(self, idx, config, dimensions):
        current_col = idx % config['print_pic']['cols'] + 1
        current_row = int(
            math.floor(
                (idx / config['print_pic']['cols']))) + 1
        x_position = (current_col * dimensions['x_border']) + (
            (current_col - 1) * config['thumbnails']['width'])
        y_position = (current_row * dimensions['y_border']) + (
            (current_row - 1) * config['thumbnails']['height'])

        return (x_position, y_position)

    def generate_template_file(self, config):
        logger.debug('Generating template file')
        generated = self.__create_new_image(
            self.dimensions['print_pic_size'])

        for idx in range(config['print_pic']['rows'] * config['print_pic']['cols']):
            positions = self.__get_positions(idx, config, self.dimensions)
            tmp = ImageDraw.Draw(generated)
            tmp.rectangle([positions, (positions[0] +
                                        config['thumbnails']['width'], positions[1] +
                                        config['thumbnails']['height'])], outline="black")
        generated.save('pimaton_template.jpg' , 'JPEG')
        logger.info('Template file has been generated here: ./pimaton_template.jpg')
