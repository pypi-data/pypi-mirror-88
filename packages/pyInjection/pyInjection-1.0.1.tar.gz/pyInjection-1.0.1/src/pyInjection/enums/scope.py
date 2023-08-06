from enum import Enum

class Scope(Enum):
    TRANSIENT: int = 0
    SINGLETON: int = 1