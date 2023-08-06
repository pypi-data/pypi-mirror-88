# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from ..units import ElectricCurrentUnit


class ElectricCurrent:
    base_unit = ElectricCurrentUnit.AMPERE
    factors = {
        ElectricCurrentUnit.MEGAAMPERE: 1e6,
        ElectricCurrentUnit.KILOAMPERE: 1e3,
        ElectricCurrentUnit.AMPERE: 1e0,
        ElectricCurrentUnit.CENTIAMPERE: 1e-2,
        ElectricCurrentUnit.MILLIAMPERE: 1e-3,
        ElectricCurrentUnit.MICROAMPERE: 1e-6,
        ElectricCurrentUnit.NANOAMPERE: 1e-9,
        ElectricCurrentUnit.PICOAMPERE: 1e-12,
    }
    abbreviations = {
        ElectricCurrentUnit.MEGAAMPERE: 'MA',
        ElectricCurrentUnit.KILOAMPERE: 'kA',
        ElectricCurrentUnit.AMPERE: 'A',
        ElectricCurrentUnit.CENTIAMPERE: 'cA',
        ElectricCurrentUnit.MILLIAMPERE: 'mA',
        ElectricCurrentUnit.MICROAMPERE: 'μA',
        ElectricCurrentUnit.NANOAMPERE: 'nA',
        ElectricCurrentUnit.PICOAMPERE: 'pA',
    }

    def __init__(self, value: float, unit: 'ElectricCurrentUnit') -> None:
        self._value = value
        self._unit = unit

    def __str__(self):
        return "{value} {unit}".format(
            value=str(self._value),
            unit=ElectricCurrent.abbreviations[self._unit])

    def __repr__(self):
        return str(self)

    # Comparison operators
    def __eq__(self, other):
        return self._value == other.as_unit(self._unit)

    # Unary operators
    def __neg__(self):
        return ElectricCurrent(-self._value, self._unit)

    # Arithmetic operators
    def __add__(self, other):
        if type(other) is ElectricCurrent:
            return ElectricCurrent(self._value + other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '+')

    def __sub__(self, other):
        if type(other) is ElectricCurrent:
            return ElectricCurrent(self._value - other.as_unit(self._unit), self._unit)

        self._raise_type_error_for_undefined_operator(other, '-')

    def __mul__(self, other):
        if type(other) in (float, int):
            return ElectricCurrent(self._value * other, self._unit)

        self._raise_type_error_for_undefined_operator(other, '*')

    def __rmul__(self, other):
        if type(other) in (float, int):
            return self * other

        self._raise_type_error_for_undefined_operator(other, '*')

    def __truediv__(self, other):
        if type(other) is ElectricCurrent:
            return (self._get_value_in_base_unit()
                    / other.as_unit(other.base_unit))
        if type(other) in (float, int):
            return ElectricCurrent(self._value / other, self._unit)

        self._raise_type_error_for_undefined_operator(other, '/')

    def _raise_type_error_for_undefined_operator(
            self, other, operator: str) -> None:
        raise TypeError(
            'unsupported operand type(s) for {0}: \'{1}\' and \'{2}\''
            .format(operator, type(self).__name__, type(other).__name__))

    @staticmethod
    def zero() -> 'ElectricCurrent':
        return ElectricCurrent(0, ElectricCurrent.base_unit)

    @property
    def unit(self) -> ElectricCurrentUnit:
        return self._unit

    @property
    def value(self) -> float:
        return self._value

    def as_unit(self, unit: ElectricCurrentUnit) -> float:
        if unit == self._unit:
            return self._value

        return self._get_value_as(unit)

    def to_unit(self, unit: ElectricCurrentUnit) -> 'ElectricCurrent':
        converted_value = self._get_value_as(unit)

        return ElectricCurrent(converted_value, unit)

    # Generation shorthands
    @staticmethod
    def from_megaamperes(value: float) -> 'ElectricCurrent':
        return ElectricCurrent(value, ElectricCurrentUnit.MEGAAMPERE)

    @staticmethod
    def from_kiloamperes(value: float) -> 'ElectricCurrent':
        return ElectricCurrent(value, ElectricCurrentUnit.KILOAMPERE)

    @staticmethod
    def from_amperes(value: float) -> 'ElectricCurrent':
        return ElectricCurrent(value, ElectricCurrentUnit.AMPERE)

    @staticmethod
    def from_centiamperes(value: float) -> 'ElectricCurrent':
        return ElectricCurrent(value, ElectricCurrentUnit.CENTIAMPERE)

    @staticmethod
    def from_milliamperes(value: float) -> 'ElectricCurrent':
        return ElectricCurrent(value, ElectricCurrentUnit.MILLIAMPERE)

    @staticmethod
    def from_microamperes(value: float) -> 'ElectricCurrent':
        return ElectricCurrent(value, ElectricCurrentUnit.MICROAMPERE)

    @staticmethod
    def from_nanoamperes(value: float) -> 'ElectricCurrent':
        return ElectricCurrent(value, ElectricCurrentUnit.NANOAMPERE)

    @staticmethod
    def from_picoamperes(value: float) -> 'ElectricCurrent':
        return ElectricCurrent(value, ElectricCurrentUnit.PICOAMPERE)

    # Conversion shorthands
    @property
    def megaamperes(self) -> float:
        return self.as_unit(ElectricCurrentUnit.MEGAAMPERE)

    @property
    def kiloamperes(self) -> float:
        return self.as_unit(ElectricCurrentUnit.KILOAMPERE)

    @property
    def amperes(self) -> float:
        return self.as_unit(ElectricCurrentUnit.AMPERE)

    @property
    def centiamperes(self) -> float:
        return self.as_unit(ElectricCurrentUnit.CENTIAMPERE)

    @property
    def milliamperes(self) -> float:
        return self.as_unit(ElectricCurrentUnit.MILLIAMPERE)

    @property
    def microamperes(self) -> float:
        return self.as_unit(ElectricCurrentUnit.MICROAMPERE)

    @property
    def nanoamperes(self) -> float:
        return self.as_unit(ElectricCurrentUnit.NANOAMPERE)

    @property
    def picoamperes(self) -> float:
        return self.as_unit(ElectricCurrentUnit.PICOAMPERE)

    def _to_base_unit(self) -> 'ElectricCurrent':
        return self.to_unit(self.base_unit)

    def _get_value_in_base_unit(self) -> float:
        try:
            return self._value * ElectricCurrent.factors[self._unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to base units.'.format(self._unit.name))

    def _get_value_as(self, unit: ElectricCurrentUnit) -> float:
        base_unit_value = self._get_value_in_base_unit()

        try:
            return base_unit_value / ElectricCurrent.factors[unit]
        except KeyError:
            raise NotImplementedError(
                'Can not convert {0} to {1}.'.format(self._unit.name, unit))
