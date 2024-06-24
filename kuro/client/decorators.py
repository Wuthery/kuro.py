"""Decorators for kuro clients."""

import functools
import typing

if typing.TYPE_CHECKING:
    from kuro import types

T = typing.TypeVar("T")
CallableT = typing.TypeVar("CallableT", bound="typing.Callable[..., object]")
AsyncCallableT = typing.TypeVar(
    "AsyncCallableT", bound="typing.Callable[..., typing.Awaitable[object]]"
)


def region_specific(region: "types.Region") -> typing.Callable[[AsyncCallableT], AsyncCallableT]:
    """Prevent function to be ran with unsupported regions."""

    def decorator(func: AsyncCallableT) -> AsyncCallableT:
        @functools.wraps(func)
        async def wrapper(self: typing.Any, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            if not hasattr(self, "region"):
                raise TypeError("Cannot use @region_specific on a plain function.")
            if region != self.region:
                raise RuntimeError(
                    "The method can only be used with client region set to " + region
                )

            return await func(self, *args, **kwargs)

        return typing.cast("AsyncCallableT", wrapper)

    return decorator
