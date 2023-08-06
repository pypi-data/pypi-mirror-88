from inspect import Signature, signature
from typing import List, Dict, Type, Any
from ..interfaces import IValidator, IScopeManager
from ..enums import Scope
from ..dtos import Registration

class ContainerInstance():
    __container: Dict[Type, Registration]
    __validators: List[IValidator]
    __scope_managers: List[IScopeManager]
    __base_types: List[Type]

    def __init__(self, validators: List[IValidator], scope_managers: List[IScopeManager], base_types: List[Type]):
        self.__validators = validators
        self.__scope_managers = scope_managers
        self.__base_types = base_types
        self.__container = {}

    def __is_valid(self, interface: Type, implementation: Any) -> bool:
        for validator in self.__validators:
            if(not validator.is_valid(interface= interface, implementation= implementation)):
                return False
        return True

    def __add(self, interface: Type, implementation: Any, scope: Scope) -> None:
        if not interface in self.__container.keys():
            if(self.__is_valid(interface= interface, implementation= implementation)):
                self.__container[interface] = Registration(implementation= implementation, scope= scope)
            else:
                raise Exception("Failed to add mapping \'{0} -> {1}\' to the container".format(
                    interface.__name__, 
                    implementation.__name__))
        else:
            raise Exception("Cannot register a duplicate implementation for \'{0}\'".format(
                interface.__name__))

    def add_transient(self, interface: Type, implementation: Any) -> None:
        self.__add(interface= interface, implementation= implementation, scope= Scope.TRANSIENT)

    def add_singleton(self, interface: Type, implementation: Any) -> None:
        self.__add(interface= interface, implementation= implementation, scope= Scope.SINGLETON)
            # check this resolves, need to write a new class that is not a 
            # decorator and test that the resolve works

    def resolve(self, interface: Type) -> Any:
        if interface in self.__container.keys():
            scope = self.__container[interface].scope
            for scope_manager in self.__scope_managers:
                if scope_manager.can_resolve(scope= scope):
                    return scope_manager.resolve(interface= interface, container= self.__container)
        raise Exception('Cannot resolve type: {0}'.format(str(interface)));

    def validate(self) -> None:
        for registration in self.__container.values():
            if type(registration.implementation) in self.__base_types:
                sig: Signature = signature(registration.implementation)
                for p in sig.parameters:
                    annotation: Any = sig.parameters[p].annotation
                    if(not annotation in self.__container.keys()):
                        raise Exception('Missing registration for: \'{0}\''.format(annotation.__name__))
