from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    @abstractmethod
    def chat(self, prompt):
        raise NotImplementedError

    @abstractmethod
    def parse_response(self, raw_response):
        raise NotImplementedError
