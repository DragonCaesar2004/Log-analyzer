import abc

from src.project_types import InputArgs


class UserInterface(abc.ABC):

    @abc.abstractmethod
    def get_init_data(self) -> InputArgs: ...
