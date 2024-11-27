import configparser

class ConfigParserWrapper:
    def __init__(self, config_file):
        """
        Initialize the ConfigParserWrapper with the path to the configuration file.
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, section, option, default=None):
        """
        Get a value from the configuration file, optionally providing a default if not found.
        """
        try:
            return self.config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def get_int(self, section, option, default=None):
        """
        Get an integer value from the configuration file.
        Returns the default value if the option does not exist or cannot be converted.
        """
        try:
            return self.config.getint(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return default

    def get_boolean(self, section, option, default=None):
        """
        Get a boolean value from the configuration file.
        Returns the default value if the option does not exist or cannot be converted.
        """
        try:
            return self.config.getboolean(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return default

    def get_list(self, section, option, default=None):
        """
        Get a list of values (comma-separated) from the configuration file.
        Example: key = value1,value2,value3
        """
        value = self.get(section, option, default)
        if value:
            return [item.strip() for item in value.split(',')]
        return default
    
    def get_list_from_key_value_pairs(self, section, option, index, default=None):
        """
        Get a list of key-value pairs from the configuration file.
        Example: key = value1:value2
        """
        value = self.get(section, option, default)
        if value:
            return [item.split(':')[index] for item in value.split(',')]
        return default
    
    def get_dict(self, section, option, default=None):
        """
        Get a dictionary of key-value pairs from the configuration file.
        Example: key = value1:value2
        """
        value = self.get(section, option, default)
        if value:
            return dict(item.split(':') for item in value.split(','))
        return default

    def sections(self):
        """
        Get the sections in the configuration file.
        """
        return self.config.sections()

    def options(self, section):
        """
        Get the options available in a given section.
        """
        return self.config.options(section)
    
