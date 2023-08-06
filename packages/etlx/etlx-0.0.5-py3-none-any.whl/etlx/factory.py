from typing import Mapping
import yaml
from copy import deepcopy
from importlib import import_module
from collections import OrderedDict


class ServiceFactory:

    def __init__(self, configFile=None):
        self.configFile = configFile
        self._catalog = None

    @property
    def catalog(self) -> Mapping:
        if self._catalog is None:
            self.load(self.configFile)
        return self._catalog

    def load(self, config):
        if self._catalog is None:
            self._catalog = OrderedDict()
        if not config:
            return
        config = loadYAML(config)
        for name, kwargs in config.items():
            if isinstance(kwargs, str):
                self.add(name, factory=kwargs)
            else:
                self.add(name, **kwargs)

    def add(self, name: str, factory=None, **kwargs):
        """Adds/replaces service entry"""
        if self._catalog is None:
            self._catalog = OrderedDict()
        if isinstance(factory, str):
            entry = self._catalog.get(factory, None)
            if entry:
                factory = entry[0]
                kwargs = self.mergeArgs(entry[1], **kwargs)
            else:
                func = self.findCallable(factory)
                if not callable(func):
                    raise ValueError(f"can't resolve {factory} into callable")
                factory = func
        self._catalog[name] = (factory, kwargs)

    def mergeArgs(self, base, **kwargs):
        """Compose result kwargs from base + optional kwags"""
        result = deepcopy(base)
        # adjust params
        for k, v in kwargs.items():
            c = result.get(k, None)
            if isinstance(c, dict) and isinstance(v, dict):
                c.update(v)
            else:
                result[k] = v
        return result

    def findCallable(self, factory: str):
        """Resolves factory name into callable: module.function"""
        s = factory.split('.')
        moduleName = '.'.join(s[:-1])
        funcName = s[-1:][0]
        if not moduleName or not funcName:
            return None
        module = import_module(name=moduleName)
        return getattr(module, funcName)

    def __getitem__(self, name):
        entry = self.catalog[name]
        return entry[1]

    def __getattr__(self, name):
        entry = self.catalog[name]

        def factory(**kwargs):
            kwargs = self.mergeArgs(entry[1], **kwargs)
            return entry[0](**kwargs)
        return factory


def loadYAML(filePath) -> Mapping:
    """Loads yaml as OrderedDict"""
    class Loader(yaml.SafeLoader):
        pass

    def constructMapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))
    Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, constructMapping)
    with open(filePath) as file:
        return yaml.load(file, Loader)
