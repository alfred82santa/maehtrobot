from dirty_loader import LoaderNamespaceReversedCached
from dirty_loader.factories import register_logging_factories

from maehtrobot.common.blueprints import register_blueprints_factories, Application
from .config import load_configuration


def create_loader(namespaces=None, factory_registers=None):
    default_namespaces = {'blueprint': 'maehtrobot.blueprints',
                          'core': 'maehtrobot.blueprints.core',
                          'common': 'maehtrobot.common'}

    if namespaces:
        default_namespaces.update(namespaces)

    loader = LoaderNamespaceReversedCached(default_namespaces)

    register_logging_factories(loader)
    register_blueprints_factories(loader)

    try:
        for factory_register in factory_registers:
            factory_register(loader)
    except TypeError:
        pass

    return loader


def create_application(environment, config_name, config_dir,
                       loader=None, application_class='common:blueprints.Application'):
    config = load_configuration(environment, config_name, config_dir)
    loader = loader or create_loader()

    return loader.factory(application_class, **config)
