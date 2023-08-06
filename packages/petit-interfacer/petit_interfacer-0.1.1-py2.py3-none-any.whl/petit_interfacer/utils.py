from __future__ import annotations

from abc import ABC, abstractstaticmethod
from dataclasses import is_dataclass
from typing import Any, List, Optional, TypeVar, Union, get_args, get_origin

T = TypeVar('T')
U = TypeVar('U')


class ClassProxyTest(ABC):
    """This class can be used to handle some types which can't be handle with issubclass

    It was written to handle dataclasses at the origin
    """
    @abstractstaticmethod
    def is_correct_type(t: Any) -> bool: ...


def is_proxy_class(cls: Any) -> bool:
    return issubclass(cls, ClassProxyTest)


class _RealOptional:
    ...


def is_real_optional(t: Any) -> bool:
    return get_origin(t) is Union and _RealOptional in get_args(t)


class _BlindBind:
    ...


def is_blindbind(t: Any) -> bool:
    return get_origin(t) is Union and _BlindBind in get_args(t)


def clean_union_type(l: list) -> None:
    if _BlindBind in l:
        l.remove(_BlindBind)
    if _RealOptional in l:
        l.remove(_RealOptional)


RealOptional = Union[T, _RealOptional]
BlindBind = Union[T, _BlindBind]


class Dataclass(ClassProxyTest):
    """As dataclasses does not provide a class to be used with issubclass, we use this proxy to handle it
    """
    def is_correct_type(t: Any) -> bool:
        return is_dataclass(t)


def validate_blindbind(names: List[str], classes: List[Any]) -> Optional[str]:
    # check if only one BlindBind
    blind_param: Optional[str] = None
    for name, v in zip(names, classes):
        if is_blindbind(v):
            if blind_param is None:
                blind_param = name
            else:
                raise Exception(
                    'Invalid prototype, you can only have one BlindBind')
    return blind_param

