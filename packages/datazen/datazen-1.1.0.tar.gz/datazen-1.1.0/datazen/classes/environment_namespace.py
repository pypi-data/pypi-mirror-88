
"""
datazen - A data structure for runtime data.
"""

# built-in
from copy import copy, deepcopy
import logging
import os
from typing import List

# internal
from datazen.paths import resolve_dir
from datazen.enums import DataType

LOG = logging.getLogger(__name__)


class EnvironmentNamespace:
    """ The base class for management of the environment data structure. """

    def __init__(self):
        """ Base constructor. """

        self.directories = {
            DataType.CONFIG: [],
            DataType.SCHEMA: [],
            DataType.TEMPLATE: [],
            DataType.VARIABLE: [],
        }

        self.data = {
            DataType.CONFIG: {},
            DataType.SCHEMA: {},
            DataType.TEMPLATE: {},
            DataType.VARIABLE: {},
        }

        self.valid = True

    def get_to_load(self, dir_type: DataType) -> List[str]:
        """
        Build a list of the yet-to-be-loaded directories for a given data
        type.
        """

        dir_data = self.directories[dir_type]

        to_load = []
        for dir_inst in dir_data:
            if not dir_inst["loaded"]:
                to_load.append(dir_inst["path"])
        return to_load

    def unload(self, dir_type: DataType) -> None:
        """ Mark all directories for a given type as un-loaded. """

        for dir_inst in self.directories[dir_type]:
            dir_inst["loaded"] = False

    def unload_all(self) -> None:
        """ Mark all directories as unloaded. """

        for key in self.data:
            self.unload(key)

    def update_load_state(self, dir_type: DataType, to_load: List[str]) -> int:
        """
        Update the load states of directories in 'to_load' for a given
        data type.
        """

        dir_data = self.directories[dir_type]
        loaded = 0

        for dir_inst in dir_data:
            if dir_inst["path"] in to_load:
                LOG.debug("loaded '%s' as '%s'", dir_inst["path"],
                          dir_type.value)
                dir_inst["loaded"] = True
                loaded = loaded + 1

        LOG.debug("loaded %d new directories for '%s'", loaded, dir_type.value)

        return loaded

    def add_dir(self, dir_type: DataType, dir_path: str,
                rel_path: str = ".", allow_dup: bool = False) -> bool:
        """ Add a directory to be loaded for a given data type. """

        dir_list = self.directories[dir_type]
        dir_path = resolve_dir(dir_path, rel_path)

        for dir_data in dir_list:
            if dir_path == dir_data["path"]:
                def noop(*_, **__):
                    pass
                log_fn = noop if allow_dup else noop
                log_fn("not adding duplicate directory '%s' to '%s'", dir_path,
                       dir_type.value)
                return allow_dup

        if not os.path.isdir(dir_path):
            LOG.error("'%s' isn't a directory, not adding to '%s'", dir_path,
                      dir_type.value)
            return False

        dir_list.append({"path": dir_path, "loaded": False})
        LOG.debug("added '%s' to '%s'", dir_path, dir_type.value)
        return True

    def add_dirs(self, dir_type: DataType, dir_paths: List[str],
                 rel_path: str = ".", allow_dup: bool = False) -> int:
        """
        Add multiple directories for a given data type, return the number of
        directories added.
        """

        dirs_added = 0
        for dir_path in dir_paths:
            if self.add_dir(dir_type, dir_path, rel_path, allow_dup):
                dirs_added = dirs_added + 1

        if dirs_added != len(dir_paths):
            LOG.error("only loaded %d / %d directories, marking invalid",
                      dirs_added, len(dir_paths))
            self.valid = False

        return dirs_added


def clone(env: EnvironmentNamespace,
          update: EnvironmentNamespace) -> EnvironmentNamespace:
    """ Create a clone (deep copy) of an existing Environment. """

    # all we need to do is copy all of the attributes
    update.directories = deepcopy(env.directories)
    update.data[DataType.CONFIG] = deepcopy(env.data[DataType.CONFIG])
    update.data[DataType.SCHEMA] = deepcopy(env.data[DataType.SCHEMA])
    update.data[DataType.VARIABLE] = deepcopy(env.data[DataType.VARIABLE])
    update.data[DataType.TEMPLATE] = copy(env.data[DataType.TEMPLATE])
    update.valid = env.valid

    return update
