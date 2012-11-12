'''
Created on 2012-11-5

@author: Lion
'''
from django.conf import settings
import logging
def getlog(): 
    logger = logging.getLogger() 
    hdlr = logging.FileHandler(settings.LOG_FILE) 
    formatter = logging.Formatter('%(asctime)s %(levelname)s % (message)s') 
    hdlr.setFormatter(formatter) 
    logger.addHandler(hdlr) 
    logger.setLevel(logging.NOTSET) 
    return logger 

