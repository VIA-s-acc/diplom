from configparser import ConfigParser, NoSectionError, NoOptionError
import os


class ConfigLoader:
    def __init__(self, config_file: str):
        """
        Initialize the ConfigLoader with a config file.

        Args:
            config_file (str): Path to the configuration file to load.

        Raises:
            FileNotFoundError: If the specified config file does not exist.

        """
        
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file {config_file} not found")
        
        self.config_file = config_file
        self.config = ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        
        for section in self.config.sections():
            setattr(self, section, self._get_section(section))

    def _get_section(self, section: str):
        """
        Helper method to retrieve a section of the configuration.

        Args:
            section (str): The section in the configuration file.

        Returns:
            dict: A dictionary containing the key-value pairs of the section.
        """
        section_data = {}
        for key in self.config.options(section):
            section_data[key] = self.config.get(section, key)
        return section_data

    def get(self, section: str, key: str, default: str = None) -> str:
        """
        Retrieve a string value from the configuration.

        Args:
            section (str): The section in the configuration file.
            key (str): The key within the section to retrieve the string value for.
            default (str, optional): The default value to return if the section or key 
                                    is not found.

        Returns:
            str: The string value associated with the specified section and key, or the default value if an error occurs.
        """

        try:
            return self.config.get(section, key)
        except (NoSectionError, NoOptionError):
            return default
    
    def getint(self, section: str, key: str, default: int = None) -> int:
        """
        Retrieve an integer value from the configuration.

        Args:
            section (str): The section in the configuration file.
            key (str): The key within the section to retrieve the integer value for.
            default (int, optional): The default value to return if the section or key 
                                    is not found, or if the value cannot be converted to an integer.

        Returns:
            int: The integer value associated with the specified section and key, or the default value if an error occurs.
        """
        try:
            return self.config.getint(section, key)
        except (NoSectionError, NoOptionError, ValueError):
            return default
    
    def getfloat(self, section: str, key: str, default: float = None) -> float:
        """
        Retrieve a float value from the configuration.

        Args:
            section (str): The section in the configuration file.
            key (str): The key within the section to retrieve the float value for.
            default (float, optional): The default value to return if the section or key 
                                    is not found, or if the value cannot be converted to a float.

        Returns:
            float: The float value associated with the specified section and key.
        """
        
        try:
            return self.config.getfloat(section, key)
        except (NoSectionError, NoOptionError, ValueError):
            return default
    
    def getboolean(self, section: str, key: str, default: bool = None) -> bool:
        """
        Retrieve a boolean value from the configuration.

        Args:
            section (str): The section in the configuration file.
            key (str): The key within the section to retrieve the boolean value for.
            default (bool, optional): The default value to return if the section or key 
                                    is not found, or if the value cannot be converted to a boolean.

        Returns:
            bool: The boolean value associated with the specified section and key, or 
                the default value if an error occurs.
        """

        try:
            return self.config.getboolean(section, key)
        except (NoSectionError, NoOptionError, ValueError):
            return default
    
    def set(self, section: str, key: str, value: str) -> None:
        """
        Set a value in the configuration.

        Args:
            section (str): The section in the configuration file.
            key (str): The key within the section to set the value for.
            value (str): The value to associate with the specified section and key.

        Raises:
            None

        Returns:
            None
        """

        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
    
    def save(self) -> None:
        
        """
        Save the current configuration to a file.
        
        This method writes the current configuration to the file specified in the
        `config_file` attribute. The file is opened in text mode with UTF-8 encoding.
        """
        
        with open(self.config_file, 'w', encoding='utf-8') as file:
            self.config.write(file)
    
    def print_config(self) -> None:
        
        """
        Print the current configuration to the console.
        
        This method prints the current configuration to the console. The output is
        formatted like a configuration file, with each section on a line by itself
        and each key-value pair on a separate line, with the key and value separated
        by an equals sign.
        """
        for section in self.config.sections():
            print(f"[{section}]")
            for key, value in self.config.items(section):
                print(f"{key} = {value}")
            print()
        
# Пример использования
if __name__ == "__main__":
    loader = ConfigLoader("../config.ini")
    
    
    