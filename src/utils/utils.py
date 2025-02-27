"""
The utils module contains utility functions that are used throughout
the project.

Functions:
    load_config: Load a YAML configuration file.
"""

import yaml


def load_config(config_path):
    """
    Load a YAML configuration file.
    """

    # Load the configuration file
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
