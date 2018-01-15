import cups
import os
import logging

from PimatonExceptions import PimatonPrintExceptions

logging.basicConfig()
logger = logging.getLogger("Pimaton")


class PimatonPrint:
    def __init__(self, config):
        logger.debug('Instanciating PimatonPrint with config %s' % config)
        self.config_printer(config)
        self.config = config

    def print_file(self, to_print):
        if os.path.exists(to_print) is False:
            raise PimatonPrintExceptions('File to print doesnt exist')

        try:
            self.conn.printFile(
                self.printer,
                to_print,
                self.config['app_name'],
                self.config['options'])
        except Exception as e:
            raise PimatonPrintExceptions(
                'Couldnt print file, an error occured: %s' % e)

    def config_printer(self, config):
        try:
            conn = cups.Connection()
            printers = conn.getPrinters()
            logger.debug('printers: %s' % printers)
            default_printer = printers.keys()[config['printer_key']]
            cups.setUser(config['user'])
        except (IPPError, HTTPError) as e:
            raise PimatonPrintExceptions('Couldnt connect to cups')

        self.printer = default_printer
        self.conn = conn
