from ..build.ConfigLoader import (call_basic_function as raw_call_basic_function)
#==========================================================
# BASE MODULE TEMPLATE
#==========================================================

from ..build.ConfigLoader import (
    call_basic_function as raw_basic_function
)

import os
from configparser import ConfigParser, NoSectionError, NoOptionError


class ConfigloaderModule:
    """!
    ConfigLoader class.
    
    @brief Class for loading and managing configuration files.
                    
    """
    def __init__(self, config_file: str):
        """!
        Constructor.
        
        @param config_file Path to the configuration file.
        
        """

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file {config_file} not found")
        
        # Read the configuration file
        self.config_file = config_file
        self.config = ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        for section in self.config.sections():
            setattr(self, section, self._get_section(section))

    def _get_section(self, section: str):
        """!
        Retrieve all key-value pairs in a section of the configuration file.

        @param section The section name to retrieve the key-value pairs for.

        @return A dictionary containing all key-value pairs in the specified section.
        """
        section_data = {}
        for key in self.config.options(section):
            section_data[key] = self.config.get(section, key)
        return section_data

    def get(self, section: str, key: str, default: str = None) -> str:
        """!
        Retrieve a value from the configuration.

        @param section The section in the configuration file.
        @param key The key within the section to retrieve the value for.
        @param default The default value to return if the section or key is not found.

        @return The value associated with the specified section and key, or the default value if an error occurs.
        """

        try:
            return self.config.get(section, key)
        except (NoSectionError, NoOptionError):
            return default
    
    def getint(self, section: str, key: str, default: int = None) -> int:
        """!
        Retrieve an integer value from the configuration.

        @param section The section in the configuration file.
        @param key The key within the section to retrieve the integer value for.
        @param default The default value to return if the section or key is not found, or if the value cannot be converted to an integer.

        @return The integer value associated with the specified section and key, or the default value if an error occurs.
    
        """
        try:
            return self.config.getint(section, key)
        except (NoSectionError, NoOptionError, ValueError):
            return default
    
    def getfloat(self, section: str, key: str, default: float = None) -> float:
        """!
        Retrieve a float value from the configuration.

        @param section The section in the configuration file.
        @param key The key within the section to retrieve the float value for.
        @param default The default value to return if the section or key is not found, or if the value cannot be converted to a float.

        @return The float value associated with the specified section and key, or the default value if an error occurs.
        
        """
        
        try:
            return self.config.getfloat(section, key)
        except (NoSectionError, NoOptionError, ValueError):
            return default
    
    def getboolean(self, section: str, key: str, default: bool = None) -> bool:
        """!
        Retrieve a boolean value from the configuration.

        @param section The section in the configuration file.
        @param key The key within the section to retrieve the boolean value for.
        @param default The default value to return if the section or key is not found, or if the value cannot be converted to a boolean.

        @return The boolean value associated with the specified section and key, or the default value if an error occurs.
        """

        try:
            return self.config.getboolean(section, key)
        except (NoSectionError, NoOptionError, ValueError):
            return default
    
    def set(self, section: str, key: str, value: str) -> None:
        """!
        Set a value in the configuration.

        @param section The section in the configuration file.
        @param key The key within the section to set the value for.
        @param value The value to set.
        
        @return None
        """

        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
    
    def save(self) -> None:
        
        """!
        Save the configuration to the file.
        
        This method saves the current configuration to the file specified in `self.config_file`.
        The configuration is written to the file in the format specified in the `ConfigParser`

        @return None
        """
        
        with open(self.config_file, 'w', encoding='utf-8') as file:
            self.config.write(file)
    
    def print_config(self) -> None:
        
        """!
        Print the configuration to the console.
        
        @return None
        
        """
        for section in self.config.sections():
            print(f"[{section}]")
            for key, value in self.config.items(section):
                print(f"{key} = {value}")
            print()

    def call_basic_function(self):
        return raw_basic_function()

def sample_function():
    instance = ConfigloaderModule()
    instance.call_basic_function()
    return "basic_function worked."
