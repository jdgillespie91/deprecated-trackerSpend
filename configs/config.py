""" 
Defines the Config() class. 
 
Summary: When instantiated, the Config() class provides an object that has as its attributes the properties defined in config.ini. The properties are taken from the section defined when instantiating the class.  
  
Usage: Suppose that we are interested in the [email_service] section of config.ini (ensure that the config file is in the same directory as this module). We instantiate the class with 
   
    from configs import config 
    config = config.Config('email_service') 

We now have an object config whose attributes are those properties defined in the config file. For instance, the username is given by 
 
    config.username 
""" 
import configparser
import os


class Config(object):
    """
    When instantiated, the Config() class provides an object whose attributes are the properties defined in [section] of config.ini (where config.ini is a configuration file in the same directory as this module).
    """
    def __init__(self, section):
        """ Sets the properties of the config file as attributes of the class. """
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
        for key, value in config.items(section):
            setattr(self, key, value)

