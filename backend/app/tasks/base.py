from abc import ABC, abstractmethod


class BaseDownloadScript(ABC):
    @abstractmethod
    def start_download(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def map_nodes(self):
        pass
