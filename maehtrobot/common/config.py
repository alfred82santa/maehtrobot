import os
from collections import Mapping
from configure import Configuration


def load_configuration(environment, config_name, config_dir):
    """

    :param environment: Environment name
    :type environment: str
    :param config_name: Config file prefix
    :type config_name: str
    :param config_dir: Config directory
    :type config_dir: str
    :return: Configuration
    """
    config_filename = '{}_{}.yaml'.format(config_name, environment)
    config_filename = os.path.join(config_dir, config_filename)

    if not os.path.isfile(config_filename):
        config_filename = '{}.yaml'.format(config_name)
        config_filename = os.path.join(config_dir, config_filename)

    config = Configuration.from_file(config_filename)
    config.configure()

    def to_dict(mapping):
        return {k: (to_dict(v) if isinstance(v, Mapping) else v) for k, v in mapping.items()}

    return to_dict(config)