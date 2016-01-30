import logging
import time
import auxiliary_module

import blescan
import sys

import bluetooth._bluetooth as bluez

from logging.handlers import TimedRotatingFileHandler

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

def init():
	# create logger with 'spam_application'
	logger = logging.getLogger('spam_application')
	logger.setLevel(logging.DEBUG)
	# create file handler which logs even debug messages
	# fh = logging.FileHandler('spam.log')
	# fh.setLevel(logging.DEBUG)
	handler = TimedRotatingFileHandler("timed_test.log",
	                                       when="m",
	                                       interval=1,
	                                       backupCount=5)

	# create console handler with a higher log level
	ch = logging.StreamHandler()
	ch.setLevel(logging.ERROR)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(handler)
	logger.addHandler(ch)

	logger.info('creating an instance of auxiliary_module.Auxiliary')
	a = auxiliary_module.Auxiliary()
	logger.info('created an instance of auxiliary_module.Auxiliary')
	logger.info('calling auxiliary_module.Auxiliary.do_something')
	a.do_something()
	logger.info('finished auxiliary_module.Auxiliary.do_something')
	logger.info('calling auxiliary_module.some_function()')
	auxiliary_module.some_function()
	logger.info('done with auxiliary_module.some_function()')
	return logger;
	
#----------------------------------------------------------------------
if __name__ == "__main__":
	logger = init()
	while True:
		returnedList = blescan.parse_events(sock, 10)
		print "----------"
		for beacon in returnedList:
			logger.info(beacon)