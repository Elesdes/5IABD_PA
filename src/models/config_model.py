from dataclasses import dataclass

from ..models.path_model import PathModel
from ..utils.files_utils import get_extension, empty_file_content
import os


@dataclass
class ConfigModel(PathModel):
    def _find_variable_origin(self, variable_name: str) -> bool:
        """
        Inspect the class hierarchy to find out where the specified variable is originally defined.
        """
        # Initialize with the current class type
        cls = self.__class__

        # Iterate over the current class and all base classes
        while cls is not object:
            # Direct fields (excluding inherited) of the current class
            direct_fields = list(cls.__dict__.get("__annotations__", {}).keys())

            # If variable_name is a directly defined field of cls
            if variable_name in direct_fields:
                return True

            # Move to the next base class in the hierarchy
            cls = cls.__bases__[0]

        return False

    def _generate_file_structure(self) -> None:
        """
        Generate elementary files for the project.
        """
        for attr_name in self.__annotations__:
            if self._find_variable_origin(attr_name):
                attr_value = getattr(self, attr_name)
                if get_extension(attr_value):
                    empty_file_content(file_path=attr_value)
                else:
                    os.makedirs(attr_value, exist_ok=True)

    def __post_init__(self):
        self._generate_file_structure()
