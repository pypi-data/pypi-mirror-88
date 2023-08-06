from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)
from unittest import mock

import httpx

from .patterns import M, Pattern
from .types import (
    ByteStream,
    CallableSideEffect,
    HeaderTypes,
    RequestTypes,
    Response,
    SideEffectTypes,
)


def decode_request(request: RequestTypes) -> httpx.Request:
    """
    Build a httpx Request from httpcore request args.
    """
    if isinstance(request, httpx.Request):
        return request  # pragma: nocover
    method, url, headers, stream = request
    return httpx.Request(method, url, headers=headers, stream=stream)


def encode_response(response: httpx.Response) -> Response:
    """
    Builds a raw response tuple from httpx Response.
    """
    return (
        response.status_code,
        response.headers.raw,
        response.stream,
        response.ext,
    )


def clone_response(response: httpx.Response, request: httpx.Request) -> httpx.Response:
    """
    Clones a httpx Response for given request.
    """
    response = httpx.Response(
        response.status_code,
        headers=response.headers,
        stream=response.stream,
        request=request,
        ext=dict(response.ext),
    )
    response.read()
    return response


class Call(NamedTuple):
    request: httpx.Request
    response: Optional[httpx.Response]


class CallList(list, mock.NonCallableMock):
    @property
    def called(self) -> bool:  # type: ignore
        return bool(self)

    @property
    def call_count(self) -> int:  # type: ignore
        return len(self)

    @property
    def last(self) -> Optional[Call]:
        return self[-1] if self else None

    def record(
        self, request: httpx.Request, response: Optional[httpx.Response]
    ) -> Call:
        call = Call(request=request, response=response)
        self.append(call)
        return call


class MockResponse(httpx.Response):
    def __init__(
        self,
        status_code: Optional[int] = None,
        *,
        content: Optional[Union[str, bytes, ByteStream]] = None,
        content_type: Optional[str] = None,
        http_version: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        if callable(content) or isinstance(content, (dict, Exception)):  # type: ignore
            raise ValueError(
                f"MockResponse content can only be str, bytes or byte stream"
                f"got {content!r}. Please use json=... or side effects."
            )

        super().__init__(status_code or 200, content=content, **kwargs)

        if content_type:
            self.headers["Content-Type"] = content_type
        if http_version:
            self.ext["http_version"] = http_version


class Route:
    def __init__(
        self,
        *patterns: Pattern,
        **lookups: Any,
    ) -> None:
        self._pattern = M(*patterns, **lookups)
        self._return_value: Optional[httpx.Response] = None
        self._side_effect: Optional[SideEffectTypes] = None
        self._pass_through: bool = False
        self._name: Optional[str] = None
        self._snapshots: List[Tuple] = []
        self.calls = CallList()
        self.snapshot()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Route):
            return False  # pragma: nocover
        return self.pattern == other.pattern

    def __repr__(self):  # pragma: nocover
        name = f"name={self._name!r} " if self._name else ""
        return f"<Route {name}{self.pattern!r}>"

    def __call__(self, side_effect: CallableSideEffect) -> CallableSideEffect:
        self.side_effect = side_effect
        return side_effect

    def __mod__(self, response: Union[int, Dict[str, Any]]) -> "Route":
        if isinstance(response, int):
            self.return_value = httpx.Response(status_code=response)

        elif isinstance(response, dict):
            response.setdefault("status_code", 200)
            self.return_value = httpx.Response(**response)

        elif isinstance(response, httpx.Response):
            self.return_value = response

        else:
            raise ValueError(
                f"Route can only % with int, dict or Response, got {response!r}"
            )

        return self

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        raise NotImplementedError("Can't set name on route.")

    @property
    def pattern(self) -> Optional[Pattern]:
        return self._pattern

    @pattern.setter
    def pattern(self, pattern: Pattern) -> None:
        raise NotImplementedError("Can't change route pattern.")

    @property
    def return_value(self) -> Optional[httpx.Response]:
        return self._return_value

    @return_value.setter
    def return_value(self, return_value: Optional[httpx.Response]) -> None:
        self.pass_through(False)
        self._return_value = return_value

    @property
    def side_effect(self) -> Optional[SideEffectTypes]:
        return self._side_effect

    @side_effect.setter
    def side_effect(self, side_effect: Optional[SideEffectTypes]) -> None:
        self.pass_through(False)
        if not side_effect:
            self._side_effect = None
        elif isinstance(side_effect, (tuple, list, Iterator)):
            self._side_effect = iter(side_effect)
        else:
            self._side_effect = side_effect

    def snapshot(self) -> None:
        # Clone iterator-type side effect to not get pre-exhausted when rolled back
        side_effect = self._side_effect
        if isinstance(side_effect, Iterator):
            side_effects = tuple(side_effect)
            self._side_effect = iter(side_effects)
            side_effect = iter(side_effects)

        self._snapshots.append(
            (
                self._pattern,
                self._name,
                self._return_value,
                side_effect,
                self._pass_through,
                CallList(self.calls),
            ),
        )

    def rollback(self) -> None:
        if not self._snapshots:
            return

        snapshot = self._snapshots.pop()
        pattern, name, return_value, side_effect, pass_through, calls = snapshot

        self._pattern = pattern
        self._name = name
        self._return_value = return_value
        self._side_effect = side_effect
        self.pass_through(pass_through)
        self.calls[:] = calls

    def reset(self) -> None:
        self.calls.clear()

    def mock(
        self,
        return_value: Optional[httpx.Response] = None,
        *,
        side_effect: Optional[SideEffectTypes] = None,
    ) -> "Route":
        self.return_value = return_value
        self.side_effect = side_effect
        return self

    def respond(
        self,
        status_code: int = 200,
        *,
        headers: Optional[HeaderTypes] = None,
        content: Optional[Union[str, bytes, ByteStream]] = None,
        text: Optional[str] = None,
        html: Optional[str] = None,
        json: Optional[Union[str, List, Dict]] = None,
        stream: Optional[ByteStream] = None,
        content_type: Optional[str] = None,
        http_version: Optional[str] = None,
        **kwargs: Any,
    ) -> "Route":
        response = MockResponse(
            status_code,
            headers=headers,
            content=content,
            text=text,
            html=html,
            json=json,
            stream=stream,
            content_type=content_type,
            http_version=http_version,
            **kwargs,
        )
        return self.mock(return_value=response)

    def pass_through(self, value: bool = True) -> "Route":
        self._pass_through = value
        return self

    @property
    def is_pass_through(self) -> bool:
        return self._pass_through

    @property
    def called(self) -> bool:
        return self.calls.called

    @property
    def call_count(self) -> int:
        return self.calls.call_count

    def _next_side_effect(
        self,
    ) -> Union[Callable, Exception, Type[Exception], httpx.Response]:
        effect: Union[Callable, Exception, Type[Exception], httpx.Response]
        if isinstance(self._side_effect, Iterator):
            effect = next(self._side_effect)
        else:
            effect = cast(
                Union[Callable, Exception, Type[Exception]], self._side_effect
            )

        return effect

    def _call_side_effect(
        self, effect: CallableSideEffect, request: httpx.Request, **kwargs: Any
    ) -> Optional[Union[httpx.Request, httpx.Response]]:
        try:
            # Call side effect
            result = effect(request, **kwargs)
        except Exception as error:
            raise SideEffectError(self, origin=error) from error

        # Validate result
        if result and not isinstance(result, (httpx.Response, httpx.Request)):
            raise ValueError(
                f"Side effects must return; either a `httpx.Response`,"
                f"a `httpx.Request` for pass-through, "
                f"or `None` for a non-match. Got {result!r}"
            )

        return result

    def _resolve_side_effect(
        self, request: httpx.Request, **kwargs: Any
    ) -> Optional[Union[httpx.Request, httpx.Response]]:
        effect = self._next_side_effect()

        # Handle Exception `instance` side effect
        if isinstance(effect, Exception):
            raise SideEffectError(self, origin=effect)

        # Handle Exception `type` side effect
        Error: Type[Exception] = cast(Type[Exception], effect)
        if isinstance(effect, type) and issubclass(Error, Exception):
            raise SideEffectError(
                self,
                origin=(
                    Error("Mock Error", request=request)
                    if issubclass(Error, httpx.HTTPError)
                    else Error()
                ),
            )

        # Handle `Callable` side effect
        if callable(effect):
            result = self._call_side_effect(effect, request, **kwargs)
            return result

        return effect

    def resolve(
        self, request: httpx.Request, **kwargs: Any
    ) -> Optional[Union[httpx.Request, httpx.Response]]:
        result: Optional[Union[httpx.Response, httpx.Request]] = None

        if self._side_effect:
            result = self._resolve_side_effect(request, **kwargs)
            if result is None:
                return None  # Side effect resolved as a non-matching route

        elif self._return_value:
            result = self._return_value

        else:
            # Auto mock a new response
            result = httpx.Response(200, request=request)

        if isinstance(result, httpx.Response) and not result._request:
            # Clone reused Response for immutability
            result = clone_response(result, request)

        return result

    def match(
        self, request: httpx.Request
    ) -> Optional[Union[httpx.Request, httpx.Response]]:
        """
        Matches and resolves request with given patterns and optional side effect.

        Returns None for a non-matching route, mocked response for a match,
        or input request for pass-through.
        """
        context = {}

        if self._pattern:
            match = self.pattern.match(request)
            if not match:
                return None
            context = match.context

        if self._pass_through:
            return request

        result = self.resolve(request, **context)
        return result


class RouteList:
    _routes: List[Route]
    _names: Dict[str, Route]

    def __init__(self, routes: Optional["RouteList"] = None) -> None:
        if routes is None:
            self._routes = []
            self._names = {}
        else:
            self._routes = list(routes._routes)
            self._names = dict(routes._names)

    def __repr__(self) -> str:
        return repr(self._routes)  # pragma: nocover

    def __iter__(self) -> Iterator[Route]:
        return iter(self._routes)

    def __bool__(self) -> bool:
        return bool(self._routes)

    def __len__(self) -> int:
        return len(self._routes)

    def __contains__(self, name: str) -> bool:
        return name in self._names

    def __getitem__(self, key: Union[int, str]) -> Optional[Route]:
        if isinstance(key, int):
            return self._routes[key]
        else:
            return self._names[key]

    def __setitem__(self, i: slice, routes: "RouteList") -> None:
        """
        Re-set all routes to given routes.
        """
        self._routes = list(routes._routes)
        self._names = dict(routes._names)

    def clear(self) -> None:
        self._routes.clear()
        self._names.clear()

    def add(self, route: Route, name: Optional[str] = None) -> Route:
        # Find route with same name
        existing_route = self._names.pop(name, None)

        if route in self._routes:
            if existing_route and existing_route != route:
                # Re-use existing route with same name, and drop any with same pattern
                index = self._routes.index(route)
                same_pattern_route = self._routes.pop(index)
                if same_pattern_route.name:
                    del self._names[same_pattern_route.name]
                    same_pattern_route._name = None
            elif not existing_route:
                # Re-use existing route with same pattern
                index = self._routes.index(route)
                existing_route = self._routes[index]
                if existing_route.name:
                    del self._names[existing_route.name]
                    existing_route._name = None

        if existing_route:
            # Update existing route's pattern and mock
            existing_route._pattern = route._pattern
            existing_route.return_value = route.return_value
            existing_route.side_effect = route.side_effect
            existing_route.pass_through(route.is_pass_through)
            route = existing_route
        else:
            # Add new route
            self._routes.append(route)

        if name:
            route._name = name
            self._names[name] = route

        return route

    def pop(self, name, default=...):
        """
        Removes a route by name and returns it.

        Raises KeyError when `default` not provided and name is not found.
        """
        try:
            route = self._names.pop(name)
            self._routes.remove(route)
            return route
        except KeyError as ex:
            if default is ...:
                raise ex
            return default


class SideEffectError(Exception):
    def __init__(self, route: Route, origin: Exception) -> None:
        self.route = route
        self.origin = origin


class PassThrough(Exception):
    def __init__(self, message: str, *, request: httpx.Request) -> None:
        super().__init__(message)
        self.request = request
