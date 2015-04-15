"""
Defines the config variable.

The config variable is a dictionary containing the {'name': 'value'} key value pairs defined in the section relevant to the service in which the config variable is defined. To ensure the correct section is identifed as relevant, ensure it has the same name as the module calling it. For instance, the email_service.py module will pick up anything defined in section [email_service].
"""

import configparser
import os


# TODO Change config_local to be a local variable. I only want config to be accessible to functions that import this module.
config_local = configparser.ConfigParser()
config_local.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
# I somehow need to get the name of the script or service that's importing this module so I know what section of the config file to import.
# TODO Find a way of determining the name of the module importing this package and use this in place of variable service_name.
# config = dict(config_local.items(service_name))

