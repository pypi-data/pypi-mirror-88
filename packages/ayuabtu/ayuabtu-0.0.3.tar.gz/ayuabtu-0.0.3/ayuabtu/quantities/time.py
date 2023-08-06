# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from ..units import TimeUnit


class Time:
    base_unit = TimeUnit.SECOND
    factors = {
        TimeUnit.WEEK: 604800,
        TimeUnit.DAY: 86400,
        TimeUnit.HOUR: 3600,
        TimeUnit.MINUTE: 60,
        TimeUnit.SECOND: 1e0,
        TimeUnit.MILLISECOND: 1e-3,
        TimeUnit.MICROSECOND: 1e-6,
        TimeUnit.NANOSECOND: 1e-9,
    }
    abbreviations = {
        TimeUnit.WEEK: 'wk',
        TimeUnit.DAY: 'day',
        TimeUnit.HOUR: 'hr',
        TimeUnit.MINUTE: 'min',
        TimeUnit.SECOND: 's',
        TimeUnit.MILLISECOND: 'ms',
        TimeUnit.MICROSECOND: 'μs',
        TimeUnit.NANOSECOND: 'ns',
    }

    def __init__(self, value: float, unit: 'TimeUnit') -> None:
        self._value = value
        self._unit = unit

    def __str__(self):
        return "{value} {unit}".format(
            value=str(self._value),
            unit=Time.abbreviations[self._unit])

    def __repr__(self):
        return str(self)

    # Comparison operators
    def __eq__(self, other):
        return self._value == other.as_unit(self._unit)

    # Unary operators
    def __neg__(self):
        return Time(-self._value, self._unit)

    # Arithmetic operators
    def __add__(self, other):
        if type(other) is Time:
            return Time(self._value + other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '+')

    def __sub__(self, other):
        if type(other) is Time:
            return Time(self._value - other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '-')

    def __mul__(self, other):
        if type(other) in (float, int):
            return Time(self._value * other, self._unit)

        self._raise_type_error_for_undefined_operator(other, '*')

    def __rmul__(self, other):
        if type(other) in (float, int):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):
        if type(other) is Time:
            return (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        if type(other) in (float, int):
            return Time(self._value / other, self._unit)

        self._raise_type_error_for_undefined_operator(other, '/')

    def _raise_type_error_for_undefined_operator(
            self, other, operator: str) -> None:
        raise TypeError(
            'unsupported operand type(s) for {0}: \'{1}\' and \'{2}\''
            .format(operator, type(self).__name__, type(other).__name__))

    @staticmethod
    def zero() -> 'Time':
        return Time(0, Time.base_unit)

    @property
    def unit(self) -> TimeUnit:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def as_unit(self, unit: TimeUnit) -> float:
        if unit == self._unit:
            return self._value

        return self._get_value_as(unit)

    def to_unit(self, unit: TimeUnit) -> 'Time':
        converted_value = self._get_value_as(unit)

        return Time(converted_value, unit)

    # Generation shorthands
    @staticmethod
    def from_weeks(value: float) -> 'Time':
        return Time(value, TimeUnit.WEEK)

    @staticmethod
    def from_days(value: float) -> 'Time':
        return Time(value, TimeUnit.DAY)

    @staticmethod
    def from_hours(value: float) -> 'Time':
        return Time(value, TimeUnit.HOUR)

    @staticmethod
    def from_minutes(value: float) -> 'Time':
        return Time(value, TimeUnit.MINUTE)

    @staticmethod
    def from_seconds(value: float) -> 'Time':
        return Time(value, TimeUnit.SECOND)

    @staticmethod
    def from_milliseconds(value: float) -> 'Time':
        return Time(value, TimeUnit.MILLISECOND)

    @staticmethod
    def from_microseconds(value: float) -> 'Time':
        return Time(value, TimeUnit.MICROSECOND)

    @staticmethod
    def from_nanoseconds(value: float) -> 'Time':
        return Time(value, TimeUnit.NANOSECOND)

    # Conversion shorthands
    @property
    def weeks(self) -> float:
        return self.as_unit(TimeUnit.WEEK)

    @property
    def days(self) -> float:
        return self.as_unit(TimeUnit.DAY)

    @property
    def hours(self) -> float:
        return self.as_unit(TimeUnit.HOUR)

    @property
    def minutes(self) -> float:
        return self.as_unit(TimeUnit.MINUTE)

    @property
    def seconds(self) -> float:
        return self.as_unit(TimeUnit.SECOND)

    @property
    def milliseconds(self) -> float:
        return self.as_unit(TimeUnit.MILLISECOND)

    @property
    def microseconds(self) -> float:
        return self.as_unit(TimeUnit.MICROSECOND)

    @property
    def nanoseconds(self) -> float:
        return self.as_unit(TimeUnit.NANOSECOND)

    def _to_base_unit(self) -> 'Time':
        return self.to_unit(self.base_unit)

    def _get_value_in_base_unit(self) -> float:
        try:
            return self._value * Time.factors[self._unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to base units.'.format(self._unit.name))

    def _get_value_as(self, unit: TimeUnit) -> float:
        base_unit_value = self._get_value_in_base_unit()

        try:
            return base_unit_value / Time.factors[unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to {1}.'.format(self._unit.name, unit))
