from functools import wraps
from inspect import Signature, signature
from typing import Any, Callable, List, Type
from abc import ABCMeta

from ..container.container_instance import ContainerInstance
from ..interfaces.ivalidator import IValidator
from ..scope_managers import TransientScopeManager, SingletonScopeManager
from ..validators.decorator_validator import DecoratorValidator
from ..validators.primitive_dependency_validator import PrimitiveDependencyValidator

# Change to implement a ContainerInstance (and then keep Container as the static wrapper)
# UnitTests then only need to be on the Instance implementation
# Test specific methods (clear) can be removed and managed within the UnitTest arrange
class Container:
    base_types: List[Type] = [
        type(type),
        ABCMeta
    ]
    container_instance: ContainerInstance = ContainerInstance(
        validators= [
            PrimitiveDependencyValidator(),
            DecoratorValidator()
        ],
        scope_managers= [
            TransientScopeManager(base_types= base_types),
            SingletonScopeManager(base_types= base_types)
        ],
        base_types= base_types)

    @staticmethod
    def inject(implementation: Callable) -> Callable:
        @wraps(implementation)
        def wrapper(*args: Any, **kwargs: Any) -> None:
            # print("Do something before calling the constructor")
            if(len(kwargs) == 0):
                sig: Signature = signature(implementation)
                if(len(sig.parameters) != len(args)):
                    # Need to resolve constructor parameters and append them to args
                    for p in sig.parameters:
                        if(p != 'self'):
                            instance = Container.resolve(interface= sig.parameters[p].annotation)
                            kwargs[p] = instance
                # Get types and collect from Container implementations
            implementation(*args, **kwargs)
            # print("Do something after calling the constructor")
        return wrapper
       
    @staticmethod
    def add_transient(interface: Type, implementation: Any) -> None:
        Container.container_instance.add_transient(interface= interface, implementation= implementation)

    @staticmethod
    def add_singleton(interface: Type, implementation: Any) -> None:
        Container.container_instance.add_singleton(interface= interface, implementation= implementation)

    @staticmethod
    def resolve(interface: Type) -> Any:
        return Container.container_instance.resolve(interface= interface)

    @staticmethod
    def validate() -> None:
        Container.container_instance.validate()