import datetime
import json
import re
import functools
import typing


def _raise_value_error(*args, **kwargs):
    """Simply raise a value error."""
    raise ValueError()


def _unhandled_exceptions_return(return_value: bool) -> typing.Callable:
    """
    Create a decorator that converts all unhandled exceptions to the given
    return value.
    """

    def decorator(func: typing.Callable) -> typing.Callable:
        """Decorate the given input function."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Convert all non keyboard interupt exceptions to the given
            value
            """
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt as err:
                raise err
            except Exception:
                return return_value
        return wrapper

    return decorator


class BaseCheck():
    """Base class for a check."""

    @property
    def args(self) -> dict:
        """The arguments that were used to construct the check."""
        return getattr(self, '_args', {})


class JsonString(BaseCheck):
    """Check for validating that an incoming string is json deserializable."""

    name = 'json'

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value can be deserialized to json."""
        json.loads(value, parse_constant=_raise_value_error)
        return True


class JsonArrayString(BaseCheck):
    """
    Check for validating that a string is json deserializable and
    deserializes into an array.
    """

    name = 'json_array'

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value can be json deserialized to an array."""
        result = json.loads(value, parse_constant=_raise_value_error)
        return isinstance(result, list)


class JsonObjectString(BaseCheck):
    """
    Check for validating that an incoming string is json deserializable and
    deserializes into an object.
    """

    name = 'json_object'

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value can be json deserialized to an object."""
        result = json.loads(value, parse_constant=_raise_value_error)
        return isinstance(result, dict)


class Between(BaseCheck):
    """Check for confirming that an incoming value is between two values"""

    name = 'between'

    def __init__(
            self,
            lower: typing.Union[str, int, float],
            upper: typing.Union[str, int, float],
    ):
        """
        Initialize the checker with its configured values.

        :param lower:
            The minimum value to allow.
        :param upper:
            The maximum value to allow.
        """
        self._upper_limit = upper
        self._lower_limit = lower
        self._args = {'lower': lower, 'upper': upper}

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm that a given value is between the specified limits."""
        return self._lower_limit <= value <= self._upper_limit


class Choice(BaseCheck):
    """
    Check for confirming that an incoming value is within a set of
    options.
    """

    name = 'choice'

    def __init__(self, options: list = None):
        self._options = set(options)
        self._args = {'options': list(options)}

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value is a valid choice"""
        return value in self._options


class IsoTimestamp(BaseCheck):
    """Check for confirming an incoming string is an iso timestamp."""

    name = 'iso_timestamp'

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value is a valid iso timestamp."""
        datetime.datetime.fromisoformat(value)
        return True


class Maximum(BaseCheck):
    """
    Check for confirming that an incoming value is less than the given
    limit.
    """

    name = 'maximum'

    def __init__(
            self, limit: typing.Union[str, int, float], inclusive: bool = True
    ):
        """
        Initialize the checker with its configured values.

        :param limit:
            The maximum value to allow.
        :param inclusive:
            Whether to allow the input value to be be exactly the limit or
            if the limit should be exclusive.
        """
        self._limit = limit
        self._inclusive = inclusive
        self._args = {'limit': limit, 'inclusive': inclusive}

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm that a given value is less than the specified limit."""
        return value <= self._limit if self._inclusive else value < self._limit


class Minimum(BaseCheck):
    """
    Check for confirming that an incoming value is greater than the given
    limit.
    """

    name = 'minimum'

    def __init__(
            self, limit: typing.Union[str, int, float], inclusive: bool = True
    ):
        """
        Initialize the checker with its configured values.

        :param limit:
            The minimum value to allow.
        :param inclusive:
            Whether to allow the input value to be be exactly the limit or
            if the limit should be exclusive.
        """
        self._limit = limit
        self._inclusive = inclusive
        self._args = {'limit': limit, 'inclusive': inclusive}

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm that a given value is greater than the specified limit."""
        return value >= self._limit if self._inclusive else value > self._limit


class Regex(BaseCheck):
    """Check for confirming that an incoming string matches a regex."""

    name = 'regex'

    def __init__(self, regex: str = None, ignore_case=False):
        flags = re.IGNORECASE if ignore_case else 0
        self._regex = re.compile(regex, flags)
        self._args = {'regex': regex, 'ignore_case': ignore_case}

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value matches the regex."""
        return bool(self._regex.match(value))


class Email(Regex):
    """Check for confirming that an incoming value is a valid email."""

    name = 'email'

    def __init__(self):
        super().__init__(
            regex=r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,63}$',
            ignore_case=True
        )
        self._args = {}


class Uuid(Regex):
    """Check for confirming that an incoming string is a valid uuid."""

    name = 'uuid'

    def __init__(self):
        pat = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        super().__init__(regex=pat, ignore_case=True)
        self._args = {}


class MaxLength(BaseCheck):
    """Check for the maximum length of an incoming string."""

    name = 'maximum_length'

    def __init__(self, limit: int):
        """
        Initialize the checker with its configured values.

        :param limit:
            The maximum value length to allow.
        """
        self._limit = limit
        self._args = {'limit': limit}

    @_unhandled_exceptions_return(False)
    def __call__(self, value: typing.Any) -> bool:
        """Confirm the given value is within the max length."""
        return len(value) <= self._limit


CHECKS = [
    Between,
    Choice,
    Email,
    IsoTimestamp,
    JsonArrayString,
    JsonObjectString,
    JsonString,
    Maximum,
    MaxLength,
    Minimum,
    Regex,
    Uuid,
]
CHECK_MAP = {c.name: c for c in CHECKS}
