# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
# pylint: disable=missing-docstring
import unittest
from ayuabtu.quantities import Length
from ayuabtu.units import LengthUnit


class LengthTests(unittest.TestCase):
    def setUp(self):
        self._zero = Length.zero()
        self._kilometers = Length(1, LengthUnit.KILOMETER)
        self._hectometers = Length(1, LengthUnit.HECTOMETER)
        self._decameters = Length(1, LengthUnit.DECAMETER)
        self._meters = Length(1, LengthUnit.METER)
        self._decimeters = Length(1, LengthUnit.DECIMETER)
        self._centimeters = Length(1, LengthUnit.CENTIMETER)
        self._millimeters = Length(1, LengthUnit.MILLIMETER)
        self._micrometers = Length(1, LengthUnit.MICROMETER)
        self._nanometers = Length(1, LengthUnit.NANOMETER)

    def test_base_unit_is_meter(self):
        self.assertEqual(LengthUnit.METER, Length.base_unit)

    def test_zero_object_has_zero_value(self):
        self.assertAlmostEqual(0, self._zero.as_unit(LengthUnit.METER))

    def test_zero_object_has_base_unit(self):
        self.assertEqual(LengthUnit.METER, self._zero.unit)

    def test_equality(self):
        self.assertTrue(
            Length(1000, LengthUnit.METER) == Length(1, LengthUnit.KILOMETER))

    # Unary operators
    def test_negation_negates_value(self):
        self.assertEqual(-1, (-self._meters).value)

    def test_negation_does_not_change_unit(self):
        self.assertEqual(LengthUnit.METER, (-self._meters).unit)

    # Arithmetic operators
    def test_addition_of_length_adds_values(self):
        result = self._decimeters + self._decameters
        self.assertAlmostEqual(101, result.value)

    def test_addition_of_length_uses_unit_of_left_operand(self):
        result = self._decimeters + self._decameters
        self.assertAlmostEqual(LengthUnit.DECIMETER, result.unit)

    def test_addition_fails_for_non_length_operand(self):
        with self.assertRaises(TypeError):
            self._meters + 1

    def test_reflected_addition_fails_for_non_length_operand(self):
        with self.assertRaises(TypeError):
            1 + self._meters

    def test_subtraction_of_length_subtracts_values(self):
        result = self._kilometers - self._meters
        self.assertAlmostEqual(0.999, result.value)

    def test_subtraction_of_length_uses_unit_of_left_operand(self):
        result = self._kilometers - self._meters
        self.assertEqual(LengthUnit.KILOMETER, result.unit)

    def test_subtraction_fails_for_non_length_operand(self):
        with self.assertRaises(TypeError):
            self._meters - 1

    def test_reflected_subtraction_fails_for_non_length_operand(self):
        with self.assertRaises(TypeError):
            1 - self._meters

    def test_reflected_multiplication_with_float_multiplies_values(self):
        result = 3 * Length(2, LengthUnit.METER)
        self.assertAlmostEqual(6, result.value)

    def test_reflected_multiplication_with_float_preserves_unit(self):
        result = 3 * Length(2, LengthUnit.METER)
        self.assertEqual(LengthUnit.METER, result.unit)

    def test_multiplication_with_float_multiplies_values(self):
        result = Length(2, LengthUnit.METER) * 3
        self.assertAlmostEqual(6, result.value)

    def test_multiplication_with_float_preserves_unit(self):
        result = Length(2, LengthUnit.METER) * 3
        self.assertEqual(LengthUnit.METER, result.unit)

    def test_division_with_float_divides_values(self):
        result = Length(3, LengthUnit.METER) / 2
        self.assertAlmostEqual(1.5, result.value)

    def test_division_with_float_preserves_unit(self):
        result = Length(3, LengthUnit.METER) / 2
        self.assertEqual(LengthUnit.METER, result.unit)

    def test_division_with_length_divides_values_and_removes_unit(self):
        result = Length(30, LengthUnit.METER) / Length(2, LengthUnit.DECAMETER)
        self.assertAlmostEqual(1.5, result)

    def test_reflected_division_fails(self):
        with self.assertRaises(TypeError):
            1 / self._meters

