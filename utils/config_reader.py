import os
import configparser


class Config:
    """
    Config class to read values from config.ini file.
    """

    def __init__(self, config_file=None):
        """
        Load config file.
        """

        # Create config parser
        self.config = configparser.ConfigParser()

        # Default config file path
        if config_file is None:
            config_file = os.path.join(
                os.path.dirname(__file__),
                "..",
                "config.ini"
            )

        # Read config file
        self.config.read(config_file)

    def get_config(self, section, key):
        """
        Get a single value from config file.
        """

        # Get value from config
        value = self.config.get(section, key)

        # Replace environment variables if any
        value = os.path.expandvars(value)

        return value

    def get_config_dict(self):
        """
        Return all config values as dictionary.
        """

        result = {}

        # Loop through all sections
        for section in self.config.sections():
            result[section] = dict(self.config[section])

        return result

    @classmethod
    def validate(cls):
        """
        Check if required login credentials are present.
        """

        # Create config object
        config = cls()

        # Read required values
        email = config.get_config("LOGIN CREDENTIALS", "valid_email")
        password = config.get_config("LOGIN CREDENTIALS", "valid_password")

        # Check if values are missing
        if not email or not password:
            raise EnvironmentError(
                "Missing login credentials.\n\n"
                "Set environment variables before running tests:\n\n"
                "Windows:\n"
                "  set ZEN_USERNAME=your_email\n"
                "  set ZEN_PASSWORD=your_password\n\n"
                "Mac/Linux:\n"
                "  export ZEN_USERNAME=your_email\n"
                "  export ZEN_PASSWORD=your_password\n"
            )