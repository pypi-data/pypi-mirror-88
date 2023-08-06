from abc import abstractmethod


class BaseCommand:

    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass
