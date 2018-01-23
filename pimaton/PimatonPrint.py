import cups
import time
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
        logger.debug('Starting print file %s' % to_print)
        if os.path.exists(to_print) is False:
            raise PimatonPrintExceptions('File to print doesnt exist')

        try:
            # Can't get the "copies" option to work with pycups, so ugly
            # workaround beloow...
            options = dict(self.config['options'])
            del options['copies']
            for c in range(0, int(self.config['options']['copies'])):
                printid = self.conn.printFile(
                    self.printer,
                    to_print,
                    self.config['app_name'],
                    options)

                if self.config['wait_for_finished_job'] is True:
                    while self.conn.getJobs().get(printid, None) is not None:
                        logger.debug('waiting for print job')
                        time.sleep(1)

                logger.debug('allowing time to print')
                time.sleep(self.config['time_between_print'])
                logger.debug('picture should be printed by now.')
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
