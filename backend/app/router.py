import json
import re
from typing import Callable, Dict, List, Tuple, Any

class Router:
    def __init__(self):
        self.routes: List[Tuple[str, re.Pattern, Callable]] = []

    def add_route(self, method: str, path_pattern: str, handler: Callable):
        regex_pattern = re.sub(r"{([a-zA-Z0-9_]+)}", r"(?P<\1>[^/]+)", path_pattern)
        regex = re.compile(f"^{regex_pattern}$")
        self.routes.append((method.upper(), regex, handler))

    def get(self, path: str):
        def decorator(handler: Callable):
            self.add_route("GET", path, handler)
            return handler
        return decorator

    def post(self, path: str):
        def decorator(handler: Callable):
            self.add_route("POST", path, handler)
            return handler
        return decorator

    def patch(self, path: str):
        def decorator(handler: Callable):
            self.add_route("PATCH", path, handler)
            return handler
        return decorator

    def delete(self, path: str):
        def decorator(handler: Callable):
            self.add_route("DELETE", path, handler)
            return handler
        return decorator

    def resolve(self, method: str, path: str) -> Tuple[Optional[Callable], Dict[str, str]]:
        for r_method, regex, handler in self.routes:
            if r_method == method.upper():
                match = regex.match(path)
                if match:
                    return handler, match.groupdict()
        return None, {}
