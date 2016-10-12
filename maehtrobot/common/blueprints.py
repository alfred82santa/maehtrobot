import asyncio
import logging
import signal
from asyncio.tasks import ensure_future
from logging import Logger

import weakref
from collections import OrderedDict, Mapping
from dirty_loader import import_class
from dirty_loader.factories import BaseFactory, instance_params, register_logging_factories


class NoResourceFound(Exception):
    pass


class BaseBlueprint:
    def __init__(self, config=None, logger=None):
        """
        """
        self._resources = {}
        self._children = OrderedDict()
        self.config = config or {}
        self._logger = logger

    def create_resources(self):
        pass

    def create_children(self):
        pass

    def prepare_class_loader(self):
        pass

    def get_resource(self, name: str):
        if '.' in name:
            child, cname = name.split('.', 1)
            try:
                return self._children[child].get_resource(cname)
            except (KeyError, NoResourceFound) as ex:
                print(ex, self, child, cname)
                pass

        try:
            return self._resources[name]
        except KeyError:
            print(self, self._resources.keys())
            raise NoResourceFound("Resource '{}' not found".format(name))

    def add_resource(self, name, resource):
        self._resources[name] = resource

    def add_child(self, name, blueprint):
        self._children[name] = blueprint
        blueprint.parent = self
        blueprint.name = name

    async def bootstrap(self):
        for resource in self._resources.values():
            try:
                await resource.bootstrap()
            except (AttributeError, TypeError):
                pass

        for child in self._children.values():
            await child.bootstrap()

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def set_logger(self, logger):
        self._logger = logger

    def run(self):
        pass


class Blueprint(BaseBlueprint):
    def __init__(self, *args, **kwargs):
        """
        Blueprint allows to group functionality.
        """
        self._parent = None
        self.name = None
        super(Blueprint, self).__init__(*args, **kwargs)

    @property
    def parent(self) -> BaseBlueprint:
        """
        Reference to parent blueprint or application.
        """
        return self._parent()

    @parent.setter
    def parent(self, parent: BaseBlueprint):
        self._parent = weakref.ref(parent)

    def get_resource(self, name: str):
        try:
            return super(Blueprint, self).get_resource(name)
        except NoResourceFound:
            return self.parent.get_resource(name)

    @property
    def loop(self):
        return self.parent.loop

    @property
    def class_loader(self):
        return self.parent.class_loader

    @BaseBlueprint.logger.getter
    def logger(self):
        if self._logger:
            return self._logger
        else:
            return self.parent.logger


class Application(BaseBlueprint):
    def __init__(self, class_loader, loop=None, logger=None, *args, **kwargs):
        self.class_loader = class_loader
        self.prepare_class_loader()
        self.loop = loop or asyncio.get_event_loop()
        kwargs['logger'] = logger or logging.getLogger()

        super(Application, self).__init__(*args, **kwargs)

    def prepare_class_loader(self):
        register_logging_factories(self.class_loader)

    def run(self):
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)
        ensure_future(self.bootstrap(), loop=self.loop)
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()

    def stop(self):
        self.loop.stop()


class BaseBlueprintFactory(BaseFactory):
    def __call__(self, resources=None, blueprints=None, class_namespaces=None, register_factories=None, **kwargs):
        try:
            for namespace, module in class_namespaces.items():
                self.loader.register_namespace(namespace, module)
        except AttributeError:
            pass

        try:
            for register_factory in register_factories:
                import_class(register_factory)(self.loader)
        except TypeError:
            pass

        blueprint = self.load_blueprint(**kwargs)

        def load_dependencies(params):
            return {name: (blueprint.get_resource(value.split(':', 1)[1])
                           if isinstance(value, str) and
                              value.startswith('resource:')
                           else getattr(blueprint, value.split(':', 1)[1])
            if isinstance(value, str) and
               value.startswith('blueprint:')
            else value)
                    for name, value in params.items()}

        deferred_resources = []
        try:
            for name, item in resources.items():
                if not isinstance(item, (str, dict, Mapping)):
                    return item
                klass, params = instance_params(item)
                try:
                    blueprint.add_resource(name, self.loader.factory(klass, **load_dependencies(params)))
                except NoResourceFound as ex:
                    deferred_resources.append((name, klass, params))

            limit = len(deferred_resources)
            if limit:
                it = 0
                name, klass, params = deferred_resources.pop()
                while name:
                    if it > limit:
                        print(repr(deferred_resources), it, limit, name)
                        raise RuntimeError("Impossible to load resources.")
                    try:
                        blueprint.add_resource(name, self.loader.factory(klass, **load_dependencies(params)))
                        it = 0
                        limit = len(deferred_resources)
                    except NoResourceFound:
                        deferred_resources.append((name, klass, params))
                        it += 1

                    try:
                        name, klass, params = deferred_resources.pop()
                    except IndexError:
                        name = None

        except AttributeError:
            pass

        self.create_children(blueprint, **(blueprints or {}))

        return blueprint

    def load_item(self, item, allowed_classes=tuple(), extra_params=None):
        if isinstance(item, allowed_classes):
            return item
        klass, params = instance_params(item)
        if extra_params:
            params.update(extra_params)
        return self.loader.factory(klass, **params)

    def iter_loaded_named_item_list(self, item_list, allowed_classes=tuple(), extra_params=None):
        try:
            for name, item in item_list.items():
                yield name, self.load_item(item, allowed_classes, extra_params=extra_params)
        except AttributeError:
            pass

    def create_children(self, blueprint, **children):
        for name, child in self.iter_loaded_named_item_list(children, BaseBlueprint,
                                                            extra_params={'parent': blueprint}):

            blueprint.add_child(name, child)
            child.create_resources()
            child.create_children()

    def load_blueprint(self, logger=None, **kwargs):
        return super(BaseBlueprintFactory, self).__call__(logger=self.load_item(logger, Logger) if logger else None,
                                                          config=kwargs)


class BlueprintFactory(BaseBlueprintFactory):
    def load_blueprint(self, parent, **kwargs):
        blueprint = super(BlueprintFactory, self).load_blueprint(**kwargs)
        blueprint.parent = parent
        blueprint.prepare_class_loader()
        return blueprint


class ApplicationFactory(BaseBlueprintFactory):
    def load_blueprint(self, logger=None, **kwargs):
        return BaseFactory.__call__(self, logger=self.load_item(logger, Logger) if logger else None,
                                    class_loader=self.loader,
                                    config=kwargs)

    def create_children(self, blueprint, core, **children):
        core_bp = self.load_item(core, BaseBlueprint, extra_params={'parent': blueprint})
        blueprint.add_child('core', core_bp)

        core_bp.create_resources()
        core_bp.create_children()

        super(ApplicationFactory, self).create_children(blueprint, **children)


def register_blueprints_factories(loader):
    loader.register_factory(Application, ApplicationFactory)
    loader.register_factory(Blueprint, BlueprintFactory)
