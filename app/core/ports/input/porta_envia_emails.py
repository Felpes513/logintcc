from abc import ABC, abstractmethod

class PortaEnviaEmail(ABC):
    @abstractmethod
    def execute(self, arquivo_em_bytes: bytes) -> int:
        pass