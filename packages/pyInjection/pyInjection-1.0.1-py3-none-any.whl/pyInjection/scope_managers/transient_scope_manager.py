from typing import Type, Any, Dict, List
from ..enums import Scope
from ..interfaces import IScopeManager
from ..dtos import Registration

class TransientScopeManager(IScopeManager):

    __base_types: List[Type]

    def __init__(self, base_types: List[Type]):
        self.__base_types = base_types

    def can_resolve(self, scope: Scope) -> bool:
        return scope == Scope.TRANSIENT

    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        if interface in container.keys():
            implementation: Any = container[interface].implementation
            if(type(implementation) in self.__base_types):
                return implementation()
            elif(type(implementation) == type(lambda: '')):
                return implementation()
            else:
                return implementation
        else:
            raise Exception('Cannot resolve type: {0}'.format(str(interface)));