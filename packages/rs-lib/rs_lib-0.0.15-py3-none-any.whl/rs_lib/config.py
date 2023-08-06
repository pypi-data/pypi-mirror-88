import os
import configparser
from .constants.config import config_structure

class Config:
    def __init__(self):
        self.__config = None

    def use(self, path):        
        config = configparser.ConfigParser()
        config.read_file(open(path))

        missing = self.__confirm(config)
        if len(missing) > 0:
            raise ValueError("The following values are missing in the config file: " + str(missing).strip('[]').replace('\'', ''))

        self.__config = config
        
    def __confirm(self, config):
        missing = []
        
        sections = config.sections()
        structure_keys = config_structure.keys()

        # Get the shared values
        # This filters away the variables in the config file, that do not relate to this library
        intersection = list(set(sections).intersection(structure_keys))

        for section in intersection:
            for key in config_structure[section]:
                if not config.has_option(section, key):
                    missing.append(section + "." + key)

        # Sort is technically unnecessary, but makes the output more readable
        missing.sort()

        return missing
    

    def get(self):
        if self.__config == None:
            raise UnboundLocalError("The config file hasnt been set with 'config.use(path)'")

        return self.__config