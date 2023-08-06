import pytest

from ueca.data import PhysicsData
from ueca.symbolf import (physicsdata_symbolic_exception,
                          as_symbolic_physicsdata_and_dimensionless_exception,
                          cancel, diff,
                          Rational, exp, log, ln, sqrt, sin, cos, tan, asin, acos, atan,
                          sinh, cosh, tanh, asinh, acosh, atanh)


def test_physicsdata_symbolic_exception_input_unexpected_type():
    with pytest.raises(TypeError):
        physicsdata_symbolic_exception(lambda x: x)(1)


def test_physicsdata_symbolic_exception_input_physicsdata_non_symbolic_mode():
    length = PhysicsData(1, "meter")
    with pytest.raises(ValueError):
        physicsdata_symbolic_exception(lambda x: x)(length)


def test_physicsdata_symbolic_dimensionless_exception():
    length = PhysicsData(1, "meter", symbol="x")
    with pytest.raises(ValueError):
        as_symbolic_physicsdata_and_dimensionless_exception(lambda x: x)(length)


def test_cancel():
    symbols = ["x", "4*(x + y)**2/(4*x + 4*y)", "x + y"]
    length1 = PhysicsData(2, "meter", symbol=symbols[0])
    length2 = PhysicsData(2, "meter", symbol="y")
    length3 = 4 * (length1 + length2) ** 2 / (4 * (length1 + length2))
    assert str(length3.symbol) == symbols[1]
    length4 = cancel(length3)
    assert str(length4.symbol) == symbols[2]


class TestDiffSymbol:  # test for diff
    def test_input_physicsdata_atom(self):
        values = [1, 1]
        symbols = ["l1", "1"]
        units = ["meter", "dimensionless"]
        length = PhysicsData(values[0], units[0], symbol=symbols[0])
        value = diff(length, length, 1)
        assert str(value.symbol) == symbols[1]
        assert value.value == values[1]
        assert value.unit == units[1]
        assert value._base_symbols == dict()

    def test_input_physicsdata_add(self):
        length1 = PhysicsData(1, "meter", symbol="x")
        length2 = PhysicsData(2, "meter", symbol="y")
        length3 = 2 * length1 + 3 * length2
        value1 = diff(length3, length1, 1)
        assert value1.value == 2
        assert value1.unit == "dimensionless"
        value2 = diff(length3, length2, 1)
        assert value2.value == 3
        assert value2.unit == "dimensionless"

    def test_input_physicsdata_sub(self):
        length1 = PhysicsData(1, "meter", symbol="x")
        length2 = PhysicsData(2, "meter", symbol="y")
        length3 = 4 * length1 - 5 * length2
        value1 = diff(length3, length1, 1)
        assert value1.value == 4
        assert value1.unit == "dimensionless"
        value2 = diff(length3, length2, 1)
        assert value2.value == -5
        assert value2.unit == "dimensionless"

    def test_input_physicsdata_mul(self):
        values = [2, 3, 6]
        symbols = ["m", "a", "a*m"]
        units = ["kilogram", "meter / second**2", "kilogram * meter / second ** 2"]
        mass = PhysicsData(values[0], units[0], symbol=symbols[0])
        acceleration = PhysicsData(values[1], units[1], symbol=symbols[1])
        power = mass * acceleration
        assert str(power.symbol) == symbols[2]
        assert power.value == values[2]
        assert power.unit == units[2]
        acceleration2 = diff(power, mass, 1)
        assert acceleration.symbol == acceleration2.symbol
        assert acceleration.value == acceleration2.value
        assert acceleration.unit == acceleration2.unit
        assert acceleration._base_symbols == acceleration2._base_symbols
        mass2 = diff(power, acceleration, 1)
        assert mass.symbol == mass2.symbol
        assert mass.value == mass2.value
        assert mass.unit == mass2.unit
        assert mass._base_symbols == mass2._base_symbols

    def test_input_physicsdata_pow(self):
        values = [3, 27, 18]
        symbols = ["l1", "3*l1**2", "6*l1"]
        units = ["meter", "meter ** 2", "meter ** 3"]
        length = PhysicsData(values[0], units[0], symbol=symbols[0])
        area = length * length
        volume = length * length * length
        area2 = diff(volume, length, 1)
        assert str(area2.symbol) == symbols[1]
        assert area.unit == area2.unit
        assert area2.value == values[1]
        assert area._base_symbols == area2._base_symbols
        length2 = diff(volume, length, 2)
        assert str(length2.symbol) == symbols[2]
        assert length2.value == values[2]
        assert length.unit == length2.unit
        assert length._base_symbols == length2._base_symbols

    def test_input_string_symbol(self):
        values = [2, 3, 18, 9, 6, 2]
        symbols = ["l1", "l2", "l1*l2**2", "l2**2", "2*l2", "2"]
        units = ["meter", "meter ** 2", "meter ** 3", "dimensionless"]
        length1 = PhysicsData(values[0], units[0], symbol=symbols[0])
        length2 = PhysicsData(values[1], units[0], symbol=symbols[1])
        volume = length1 * length2 * length2
        assert str(volume.symbol) == symbols[2]
        assert volume.value == values[2]
        assert volume.unit == units[2]
        area = diff(volume, length1, 1)
        assert str(area.symbol) == symbols[3]
        assert area.value == values[3]
        assert area.unit == units[1]
        assert len(area._base_symbols) == 1
        assert str(area._base_symbols[symbols[1]].units) == units[0]
        length3 = diff(area, length2, 1)
        assert str(length3.symbol) == symbols[4]
        assert length3.value == values[4]
        assert length3.unit == units[0]
        assert len(area._base_symbols) == 1
        assert str(area._base_symbols[symbols[1]].units) == units[0]
        value = diff(length3, length2, 1)
        assert str(value.symbol) == symbols[5]
        assert value.value == values[5]
        assert value.unit == units[3]
        assert value._base_symbols == dict()

    def test_input_unexpected_type(self):
        length = PhysicsData(1, "meter", symbol="l1")
        with pytest.raises(TypeError):
            diff(length, 3.0, 1)

    def test_input_physicsdata_non_symbolic_mode(self):
        length = PhysicsData(1, "meter")
        with pytest.raises(ValueError):
            diff(length, 3.0, 1)

    def test_input_string_non_symbol(self):
        length = PhysicsData(1, "meter", symbol="l1")
        with pytest.raises(ValueError):
            diff(length, "l2", 1)

    def test_input_string_non_symbol_dimensionless(self):
        unit = "dimensionless"
        value = PhysicsData(3, unit, symbol="l1")
        value2 = diff(value, "l2", 1)
        assert str(value2.symbol) == "0"
        assert value2.value == 0
        assert value2.unit == unit
        assert value2._base_symbols == dict()


def test_Rational():
    value1 = Rational(1, 2)
    assert str(value1.symbol) == "1/2"
    assert value1.unit == "dimensionless"
    value2 = Rational(0.5)
    assert str(value2.symbol) == "1/2"
    assert value2.unit == "dimensionless"
    value3 = Rational("3", "4")
    assert str(value3.symbol) == "3/4"
    assert value3.unit == "dimensionless"


def test_exp():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = exp(length1)
    assert str(length2.symbol) == "exp(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        exp(PhysicsData(1, "meter", symbol="x"))


def test_log():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = log(length1)
    assert str(length2.symbol) == "log(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        log(PhysicsData(1, "meter", symbol="x"))


def test_ln():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = ln(length1)
    assert str(length2.symbol) == "log(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        ln(PhysicsData(1, "meter", symbol="x"))


def test_sqrt():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = sqrt(length1)
    assert str(length2.symbol) == "sqrt(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        sqrt(PhysicsData(1, "meter", symbol="x"))


def test_sqrt_apply_dim():
    units = ["meter ** 2", "meter"]
    area = PhysicsData(5, units[0], symbol="x")
    length = sqrt(area, apply_dim=True)
    assert str(length.symbol) == "sqrt(x)"
    assert length.unit == units[1]
    assert area._base_symbols == length._base_symbols


def test_sin():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = sin(length1)
    assert str(length2.symbol) == "sin(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        sin(PhysicsData(1, "meter", symbol="x"))


def test_cos():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = cos(length1)
    assert str(length2.symbol) == "cos(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        cos(PhysicsData(1, "meter", symbol="x"))


def test_tan():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = tan(length1)
    assert str(length2.symbol) == "tan(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        tan(PhysicsData(1, "meter", symbol="x"))


def test_asin():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = asin(length1)
    assert str(length2.symbol) == "asin(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        asin(PhysicsData(1, "meter", symbol="x"))


def test_acos():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = acos(length1)
    assert str(length2.symbol) == "acos(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        acos(PhysicsData(1, "meter", symbol="x"))


def test_atan():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = atan(length1)
    assert str(length2.symbol) == "atan(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        atan(PhysicsData(1, "meter", symbol="x"))


def test_sinh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = sinh(length1)
    assert str(length2.symbol) == "sinh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        sinh(PhysicsData(1, "meter", symbol="x"))


def test_conh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = cosh(length1)
    assert str(length2.symbol) == "cosh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        cosh(PhysicsData(1, "meter", symbol="x"))


def test_tanh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = tanh(length1)
    assert str(length2.symbol) == "tanh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        tanh(PhysicsData(1, "meter", symbol="x"))


def test_asinh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = asinh(length1)
    assert str(length2.symbol) == "asinh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        asinh(PhysicsData(1, "meter", symbol="x"))


def test_acosh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = acosh(length1)
    assert str(length2.symbol) == "acosh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        acosh(PhysicsData(1, "meter", symbol="x"))


def test_atanh():
    length1 = PhysicsData(1, "dimensionless", symbol="x")
    length2 = atanh(length1)
    assert str(length2.symbol) == "atanh(x)"
    assert length2.unit == length1.unit
    assert length2._base_symbols == length1._base_symbols
    with pytest.raises(ValueError):
        atanh(PhysicsData(1, "meter", symbol="x"))
