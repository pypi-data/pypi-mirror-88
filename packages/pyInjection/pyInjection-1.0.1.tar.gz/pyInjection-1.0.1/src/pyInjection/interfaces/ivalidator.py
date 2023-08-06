from typing import Type, Callable, Any

class IValidator():
    def is_valid(self, interface: Type, implementation: Any) -> bool:
        pass