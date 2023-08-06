from typing import Type, Any, Dict, List
from inspect import Signature, signature
from ..enums import Scope
from ..interfaces import IScopeManager
from ..dtos import Registration

class SingletonScopeManager(IScopeManager):
    __resolved_instances: Dict[Type, Any]
    __base_types: List[Type]

    def __init__(self, base_types: List[Type]) -> None:
        self.__resolved_instances = {}
        self.__base_types = base_types

    def can_resolve(self, scope: Scope) -> bool:
        return scope == Scope.SINGLETON

    def resolve(self, interface: Type, container: Dict[Type, Registration]) -> Any:
        if interface in self.__resolved_instances.keys():
            return self.__resolved_instances[interface]
        else:
            if interface in container.keys():
                implementation: Any = container[interface].implementation
                if(type(implementation) in self.__base_types): # Class Registration
                    kwargs: Any = {}
                    sig: Signature = signature(implementation)
                    for p in sig.parameters:
                        if(p != 'self'):
                            instance = self.resolve(interface= sig.parameters[p].annotation, container= container)
                            kwargs[p] = instance
                    self.__resolved_instances[interface] = implementation(**kwargs)
                elif(type(implementation) == type(lambda: '')):
                    self.__resolved_instances[interface] = implementation()
                else:
                    self.__resolved_instances[interface] = implementation
                return self.__resolved_instances[interface]
            else:
                raise Exception('Cannot resolve type: {0}'.format(str(interface)));

    @property
    # Exposed for Unit Testing
    def resolved_instances(self) -> Dict[Type, Any]:
        return self.__resolved_instances