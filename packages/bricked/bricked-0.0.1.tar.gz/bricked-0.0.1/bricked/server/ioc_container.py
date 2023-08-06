import inspect
from typing import Any, Callable, Dict, List, Type

from aiohttp import web


class IOCContainer(object):

    def __init__(self):
        self._ioc_container: Dict[Type, Any] = dict()

    def update_ioc_container(self, update_dict: dict):
        self._ioc_container.update(update_dict)

    def _get_temp_ioc_container(self, middleware_results, request):
        ioc_container_instance = self._ioc_container.copy()
        ioc_container = {
            web.Request.__name__: request,
        }
        ioc_container.update(middleware_results)
        return ioc_container_instance

    def inject_dependencies(
        self,
        to_inject: Callable,
        request: web.Request,
        middleware_results: Dict[Type, Any],
    ) -> List[Any]:
        arg_spec = inspect.getfullargspec(to_inject)
        positional_args = arg_spec.args[1:]  # ignore `self`
        annotations = arg_spec.annotations
        if 'return' in annotations:  # ignore return type
            annotations.pop('return')
        if len(positional_args) != len(annotations):
            raise ValueError  # TODO: better error message

        ioc_container_instance = self._get_temp_ioc_container(middleware_results, request)
        ioc_container_instance.update({web.Request.__name__: request})
        ioc_container_instance.update(middleware_results)

        arguments = []
        for arg_name, type_annotation in arg_spec.annotations.items():
            type_name = type_annotation.__name__
            if type_name in ioc_container_instance:
                arguments.append(ioc_container_instance[type_name])
            else:
                raise ValueError("Not in IoC container")
        return arguments
