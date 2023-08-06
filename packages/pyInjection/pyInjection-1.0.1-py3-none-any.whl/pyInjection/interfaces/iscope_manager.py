from typing import Type, Any, Dict
from ..enums import Scope
from ..dtos import Registration

class IScopeManager():

    def can_resolve(self, scope: Scope) -> bool:
        pass

    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        pass