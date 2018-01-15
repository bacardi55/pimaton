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

    def __init__(self, config):
        logger.debug('Instanciating PimatonCam with config %s' % config)
        self.picamera = PiCamera()
        self.config_picamera()
        self.config = config

    def take_pictures(self, unique_key):
        """
        This function takes picture via the pi camera
        """
        logger.debug("Starting taking_pictures")

        taken_pictures = []
        self.picamera.start_preview()
        sleep(self.config['time_before_first_picture'])

        for i in range(self.config['number_of_pictures_to_take']):
            filename = self.config['picture_prefix_name'] + "_" + unique_key + \
                '_' + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + ".jpg"
            taken_pictures.append(filename)

            sleep(self.config['time_between_pictures'])
            logger.debug('Taking picture %s' % i)
            self.capture(filename)
            logger.debug("Photo (" + filename + ") saved: " + filename)

        self.picamera.stop_preview()

        logger.debug("The following pictures were taken %s" % taken_pictures)
        return taken_pictures

    def capture(self, filename):
        logger.debug("Capturing picture %s in %s" %
                     (filename, self.config['photo_directory']))
        try:
            self.picamera.capture(self.config['photo_directory'] + '/' + filename)
        except Exception as e:
            raise PimatonCamExceptions('An error occured capturing the picture: %s' % e)

    def config_picamera(self):
        logger.debug('Configuring Pi Camera')
        # TODO v0.0.1 : Manage camera configuration.

        try:
            # self.picamera.resolution            = (1920, 1440)
            self.picamera.resolution = (640, 480)
            # self.picamera.framerate             = 24
            # self.picamera.sharpness             = 0
            # self.picamera.contrast              = 0
            # self.picamera.brightness            = 50
            # self.picamera.saturation            = 0
            # self.picamera.iso                   = 0
            # self.picamera.video_stabilization   = False
            # self.picamera.exposure_compensation = 0
            self.picamera.exposure_mode = 'auto'
            self.picamera.meter_mode = 'average'
            self.picamera.awb_mode = 'auto'
            self.picamera.rotation = 0
            self.picamera.hflip = True
            self.picamera.vflip = False
        except:
            raise PimatonCamExceptions('Couldnt config picamera')
