import functools
import inspect
from typing import (Any, Callable, Dict, Final, List, Optional, Set, TypeVar, Union,
                    get_args, get_origin)

from .utils import (ClassProxyTest, clean_union_type,
                    is_blindbind, is_proxy_class, is_real_optional, validate_blindbind)

T = TypeVar('T')
U = TypeVar('U')

base_code: Final[str] = "lambda {all_params}: func({reduced_params})"


def adapt_for(all_args: List[str], args: Dict[str, str]) -> Callable[[Callable], Callable]:
    def decorator(func: Callable):
        # TODO: bind remaining params if `func` has more default params than all_args
        string = base_code.format(
            all_params=','.join(all_args),
            reduced_params=','.join(
                f'{new_name}={old_name}' for old_name, new_name in args.items())
        )
        # print(string)
        f1: Callable = eval(
            string,
            {'func': func},
        )
        return functools.wraps(func)(f1)
    return decorator

# TODO: not enough type hint


def make_transfomer(all_args: List[str]) -> Callable[[Callable], Callable]:
    return functools.partial(adapt_for, all_args)

# TODO: type hint seems false


def transformer_from_prototype(func: Callable[[T], U]) -> Callable[[Dict[str, str]], Callable[[T], Any]]:
    return make_transfomer(inspect.signature(func).parameters.keys())


def interface_binder_for(func: T) -> Callable[[Callable], T]:
    """Will try to bind two interfaces together by using type hinting:

    You can use special annotations for this, such as RealOptional and BlindBind

    ### RealOptional

    The decorator won't force the bind the parameter if it is missing in the decorated function

    ### BlindBind

    If an annotation is missing, then the decorator will bind the unknown parameter on the BlindBind parameter

    As such you can only have one BindBind parameter per function prototype
    """
    parameters = inspect.signature(func).parameters

    required_names: Set[str] = {
        name for name, value in parameters.items() if not is_real_optional(value.annotation)
    }
    names = [
        name for name in parameters.keys()
    ]
    classes = [
        cls.annotation for cls in parameters.values()
    ]

    # check if only one BlindBind
    blind_param = validate_blindbind(names, classes)
    transformer = transformer_from_prototype(func)

    def f(func: Callable):
        res: Dict[str, str] = {}
        sig = inspect.signature(func)
        handled_params = 0
        for param_name, value in sig.parameters.items():
            annotation = value.annotation
            if inspect.isclass(annotation):
                for i, cls in enumerate(classes):
                    if get_origin(cls) is Union:
                        cls = list(get_args(cls))
                        clean_union_type(cls)
                    # kinda ugly, but this is compile time
                    a = cls
                    if not isinstance(cls, list):
                        a = [cls]
                    for c in a:
                        if is_proxy_class(c):
                            # c: ClassProxyTest
                            if c.is_correct_type(annotation):
                                res[names[i]] = param_name
                                handled_params += 1
                                break
                        elif issubclass(annotation, c):
                            res[names[i]] = param_name
                            handled_params += 1
                            break
                #     else:
                #         break
                # else:
                #     raise Exception(
                #         f'Invalid type hint in {func.__name__}, {annotation}')

            elif annotation is None:
                res[blind_param] = param_name
        keys = set(res.keys())

        if len(sig.parameters) == handled_params + 1:
            for key in sig.parameters.keys():
                if key not in keys:
                    res[blind_param] = key

        # validate required names
        for name in required_names:
            if name not in res:
                raise Exception(
                    f"Wasn't able to bind all parameters based on annotations for function: {func.__name__}"
                )

        return transformer(res)(func)
    return f
