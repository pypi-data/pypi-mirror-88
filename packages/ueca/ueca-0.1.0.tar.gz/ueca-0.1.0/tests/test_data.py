import sympy

from ueca.data import PhysicsData, as_physicsdata, ureg


class TestPhysicsData:
    def test_add_physicsdata(self):
        length_values = [2.3, 6.7, 9.0]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit)
        length2 = PhysicsData(length_values[1], unit)
        length3 = length1 + length2
        assert length3.value == length_values[2]
        assert str(length3.unit) == unit

    def test_add_except_physicsdata(self):
        unit = "dimensionless"
        length1 = PhysicsData(11, unit)
        length2 = (length1 + 2) + 2.0
        assert length2.value == 15.0
        assert str(length2.unit) == unit

    def test_radd_except_physicsdata(self):
        unit = "dimensionless"
        length1 = PhysicsData(3, unit)
        length2 = 10.0 + (5 + length1)
        assert length2.value == 18.0
        assert str(length2.unit) == unit

    def test_sub_physicsdata(self):
        length_values = [6.3, 2.5, 3.8]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit)
        length2 = PhysicsData(length_values[1], unit)
        length3 = length1 - length2
        assert length3.value == length_values[2]
        assert str(length3.unit) == unit

    def test_sub_except_physicsdata(self):
        unit = "dimensionless"
        length1 = PhysicsData(11, unit)
        length2 = (length1 - 2) - 2.0
        assert length2.value == 7.0
        assert str(length2.unit) == unit

    def test_rsub_except_physicsdata(self):
        unit = "dimensionless"
        length1 = PhysicsData(3, unit)
        length2 = 10.0 - (5 - length1)
        assert length2.value == 8.0
        assert str(length2.unit) == unit

    def test_mul_physicsdata(self):
        length_values = [7.0, 3.0, 21.0]
        units = ["meter", "meter ** 2"]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = PhysicsData(length_values[1], units[0])
        length3 = length1 * length2
        assert length3.value == length_values[2]
        assert str(length3.unit) == units[1]

    def test_mul_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(11, unit)
        length2 = (length1 * 2) * 2.0
        assert length2.value == 44.0
        assert str(length2.unit) == unit

    def test_rmul_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(3, unit)
        length2 = 10.0 * (5 * length1)
        assert length2.value == 150.0
        assert str(length2.unit) == unit

    def test_floordiv_physicsdata(self):
        length_values = [9.3, 4.0, 2.0]
        units = ["meter", "dimensionless"]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = PhysicsData(length_values[1], units[0])
        length3 = length1 // length2
        assert length3.value == length_values[2]
        assert str(length3.unit) == units[1]

    def test_floordiv_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(11, unit)
        length2 = (length1 // 2) // 2.0
        assert length2.value == 2
        assert str(length2.unit) == unit

    def test_rfloordiv_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(3, unit)
        length2 = 10.0 // (5 // length1)
        assert length2.value == 10
        assert str(length2.unit) == unit

    def test_truediv_physicsdata(self):
        length_values = [9.3, 4.0, 2.325]
        units = ["meter", "dimensionless"]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = PhysicsData(length_values[1], units[0])
        length3 = length1 / length2
        assert length3.value == length_values[2]
        assert str(length3.unit) == units[1]

    def test_truediv_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(11, unit)
        length2 = (length1 / 2) / 2.0
        assert length2.value == 2.75
        assert str(length2.unit) == unit

    def test_rtruediv_except_physicsdata(self):
        unit = "meter"
        length1 = PhysicsData(2, unit)
        length2 = 10.0 / (5 / length1)
        assert length2.value == 4.0
        assert str(length2.unit) == unit

    def test_pow_physicsdata(self):
        units = ["meter", "dimensionless", "meter ** 5"]
        length_values = [2, 32]
        length1 = PhysicsData(length_values[0], units[0])
        value = PhysicsData(5, units[1])
        length2 = length1 ** value
        assert length2.value == length_values[1]
        assert str(length2.unit) == units[2]

    def test_pow_except_physicsdata(self):
        units = ["meter", "meter ** 5"]
        length_values = [2, 32]
        length1 = PhysicsData(length_values[0], units[0])
        length2 = length1 ** 5
        assert length2.value == length_values[1]
        assert str(length2.unit) == units[1]

    def test_is_symbolic(self):
        length1 = PhysicsData(2, "meter")
        length2 = PhysicsData(2, "meter", symbol=sympy.Symbol("x"))
        assert not length1.is_symbolic()
        assert length2.is_symbolic()

    def test_uncertainty(self):
        uncertainty = 0.3939
        length1 = PhysicsData(2.345, "meter", uncertainty=uncertainty)
        assert length1.uncertainty == uncertainty
        assert isinstance(length1.data, ureg.Measurement)

    def test_subs(self):
        mass1 = PhysicsData(1.2, "kg", symbol="m")
        mass2_symbolic = 2 * mass1
        mass2 = mass2_symbolic.subs()
        assert str(mass2_symbolic) == "2*m kilogram"
        assert str(mass2) == "2.4 kilogram"

    def test_to_latex(self):
        mass = PhysicsData(1.2, "kg")
        assert mass.to_latex() == r"$1.2\ \mathrm{kg}$"
        length = PhysicsData(113.241, "m", uncertainty=0.672)
        assert length.to_latex() == r"$\left(113.2 \pm 0.7\right)\ \mathrm{m}$"
        length = PhysicsData(2.2, "dimensionless", uncertainty=0.6)
        assert length.to_latex() == r"$\left(2.2 \pm 0.6\right)$"

    def test_unit_to(self):
        power1 = PhysicsData(1, "N", symbol="x")
        power2 = power1.unit_to("kg*m/s^2")
        assert power1.value == power2.value
        assert power1.unit == "newton"
        assert power2.unit == "kilogram * meter / second ** 2"
        assert power1.symbol == power2.symbol
        assert power1._base_symbols == power2._base_symbols


class TestPhysicsDataSymbol:
    def test_add(self):
        length_values = [4, 7, 15]
        length_symbols = ["x_1", "y", "2*x_1 + y"]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit, symbol=length_symbols[0])
        length2 = PhysicsData(length_values[1], unit, symbol=length_symbols[1])
        length3 = length1 + length2 + length1
        assert str(length1.symbol) == length_symbols[0]
        assert str(length2.symbol) == length_symbols[1]
        assert str(length3.symbol) == length_symbols[2]
        assert length1.value == length_values[0]
        assert length2.value == length_values[1]
        assert length3.value == length_values[2]
        assert str(length3._base_symbols[length_symbols[0]].units) == unit
        assert str(length3._base_symbols[length_symbols[1]].units) == unit
        assert len(length1._base_symbols) == 1
        assert len(length2._base_symbols) == 1
        assert len(length3._base_symbols) == 2

    def test_radd(self):
        values = [5, 3, 8]
        symbols = ["x", "x + 3"]
        unit = "dimensionless"
        value1 = PhysicsData(values[0], unit, symbol=symbols[0])
        value2 = values[1] + value1
        assert str(value1.symbol) == symbols[0]
        assert str(value2.symbol) == symbols[1]
        assert value1.value == values[0]
        assert value2.value == values[2]
        assert str(value1._base_symbols[symbols[0]].units) == unit
        assert str(value2._base_symbols[symbols[0]].units) == unit
        assert len(value1._base_symbols) == 1
        assert len(value2._base_symbols) == 1

    def test_sub(self):
        length_values = [1, 2, -3]
        length_symbols = ["x", "y_n", "x - 2*y_n"]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit, symbol=length_symbols[0])
        length2 = PhysicsData(length_values[1], unit, symbol=length_symbols[1])
        length3 = length1 - length2 - length2
        assert str(length1.symbol) == length_symbols[0]
        assert str(length2.symbol) == length_symbols[1]
        assert str(length3.symbol) == length_symbols[2]
        assert length1.value == length_values[0]
        assert length2.value == length_values[1]
        assert length3.value == length_values[2]
        assert str(length3._base_symbols[length_symbols[0]].units) == unit
        assert str(length3._base_symbols[length_symbols[1]].units) == unit
        assert len(length1._base_symbols) == 1
        assert len(length2._base_symbols) == 1
        assert len(length3._base_symbols) == 2

    def test_rsub(self):
        values = [5, 2, -3]
        symbols = ["x", "2 - x"]
        unit = "dimensionless"
        value1 = PhysicsData(values[0], unit, symbol=symbols[0])
        value2 = values[1] - value1
        assert str(value1.symbol) == symbols[0]
        assert str(value2.symbol) == symbols[1]
        assert value1.value == values[0]
        assert value2.value == values[2]
        assert str(value1._base_symbols[symbols[0]].units) == unit
        assert str(value2._base_symbols[symbols[0]].units) == unit
        assert len(value1._base_symbols) == 1
        assert len(value2._base_symbols) == 1

    def test_mul(self):
        length_values = [3, 5, 75]
        length_symbols = ["x_a", "y_b", "x_a*y_b**2"]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit, symbol=length_symbols[0])
        length2 = PhysicsData(length_values[1], unit, symbol=length_symbols[1])
        length3 = length2 * length1 * length2
        assert str(length1.symbol) == length_symbols[0]
        assert str(length2.symbol) == length_symbols[1]
        assert str(length3.symbol) == length_symbols[2]
        assert length1.value == length_values[0]
        assert length2.value == length_values[1]
        assert length3.value == length_values[2]
        assert str(length3._base_symbols[length_symbols[0]].units) == unit
        assert str(length3._base_symbols[length_symbols[1]].units) == unit
        assert len(length1._base_symbols) == 1
        assert len(length2._base_symbols) == 1
        assert len(length3._base_symbols) == 2

    def test_rmul(self):
        values = [5, 3, 75]
        symbols = ["x_a", "3*x_a**2"]
        unit = "meter"
        length = PhysicsData(values[0], unit, symbol=symbols[0])
        area = values[1] * length * length
        assert str(length.symbol) == symbols[0]
        assert str(area.symbol) == symbols[1]
        assert length.value == values[0]
        assert area.value == values[2]
        assert len(length._base_symbols) == 1
        assert str(length._base_symbols[symbols[0]].units) == unit
        assert str(area._base_symbols[symbols[0]].units) == unit
        assert len(area._base_symbols) == 1

    def test_floordiv(self):
        length_values = [3, 25, 2]
        length_symbols = ["x", "y", "floor(floor(y/x)/x)"]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit, symbol=length_symbols[0])
        length2 = PhysicsData(length_values[1], unit, symbol=length_symbols[1])
        length3 = length2 // length1 // length1
        assert str(length1.symbol) == length_symbols[0]
        assert str(length2.symbol) == length_symbols[1]
        assert str(length3.symbol) == length_symbols[2]
        assert length1.value == length_values[0]
        assert length2.value == length_values[1]
        assert length3.value == length_values[2]
        assert str(length3._base_symbols[length_symbols[0]].units) == unit
        assert str(length3._base_symbols[length_symbols[1]].units) == unit
        assert len(length1._base_symbols) == 1
        assert len(length2._base_symbols) == 1
        assert len(length3._base_symbols) == 2

    def test_rfloordiv(self):
        values = [2, 11, 5]
        symbols = ["x_a", "floor(11/x_a)"]
        units = ["meter", "1 / meter"]
        length = PhysicsData(values[0], units[0], symbol=symbols[0])
        result = values[1] // length
        assert str(length.symbol) == symbols[0]
        assert str(result.symbol) == symbols[1]
        assert length.value == values[0]
        assert result.value == values[2]
        assert len(length._base_symbols) == 1
        assert str(length._base_symbols[symbols[0]].units) == units[0]
        assert str(result._base_symbols[symbols[0]].units) == units[0]
        assert len(result._base_symbols) == 1

    def test_truediv(self):
        length_values = [3, 22.5, 2.5]
        length_symbols = ["x_n", "y_n", "y_n/x_n**2"]
        unit = "meter"
        length1 = PhysicsData(length_values[0], unit, symbol=length_symbols[0])
        length2 = PhysicsData(length_values[1], unit, symbol=length_symbols[1])
        length3 = length2 / length1 / length1
        assert str(length1.symbol) == length_symbols[0]
        assert str(length2.symbol) == length_symbols[1]
        assert str(length3.symbol) == length_symbols[2]
        assert length1.value == length_values[0]
        assert length2.value == length_values[1]
        assert length3.value == length_values[2]
        assert str(length3._base_symbols[length_symbols[0]].units) == unit
        assert str(length3._base_symbols[length_symbols[1]].units) == unit
        assert len(length1._base_symbols) == 1
        assert len(length2._base_symbols) == 1
        assert len(length3._base_symbols) == 2

    def test_rtruediv(self):
        values = [2.5, 14, 5.6]
        symbols = ["x_a", "14/x_a"]
        units = ["meter", "1 / meter"]
        length = PhysicsData(values[0], units[0], symbol=symbols[0])
        result = values[1] / length
        assert str(length.symbol) == symbols[0]
        assert str(result.symbol) == symbols[1]
        assert length.value == values[0]
        assert result.value == values[2]
        assert len(length._base_symbols) == 1
        assert str(length._base_symbols[symbols[0]].units) == units[0]
        assert str(result._base_symbols[symbols[0]].units) == units[0]
        assert len(result._base_symbols) == 1

    def test_pow(self):
        values = [4, 3, 64]
        symbols = ["x", "x**3"]
        units = ["meter", "dimensionless"]
        length1 = PhysicsData(values[0], units[1], symbol=symbols[0])
        value = PhysicsData(values[1], "dimensionless")
        length2 = length1 ** value
        assert str(length1.symbol) == symbols[0]
        assert str(length2.symbol) == symbols[1]
        assert length1.value == values[0]
        assert length2.value == values[2]
        assert len(length1._base_symbols) == 1
        assert len(length2._base_symbols) == 1

    def test_uncertainty(self):
        uncertainty = 0.3939
        length1 = PhysicsData(2.345, "meter", symbol="x", uncertainty=uncertainty)
        assert length1.uncertainty == uncertainty
        assert isinstance(length1._base_symbols["x"], ureg.Measurement)
        assert not isinstance(length1.data, ureg.Measurement)

    def test_repr_latex_(self):
        length1 = PhysicsData(82.39, "meter", symbol="Delta lambda_i")
        text = length1._repr_latex_()
        assert text == r"\Delta \lambda_{i}\ \mathrm{m}"

    def test_repr_latex__dimensionless(self):
        length1 = PhysicsData(82.39, "dimensionless", symbol="Delta theta")
        text = length1._repr_latex_()
        assert text == r"\Delta \theta"

    def test_repr_latex__force_value(self):
        length1 = PhysicsData(2.39, "meter", symbol="Delta lambda_i", uncertainty=0.46)
        text = length1._repr_latex_(force_value=True)
        assert text == r"\left(2.4 \pm 0.5\right)\ \mathrm{m}"


def test_as_physicsdata_physicsdata():
    unit = "meter"
    value = 2
    x = PhysicsData(value, unit)
    assert isinstance(x, PhysicsData)
    assert x.value == value
    assert x.unit == unit


def test_as_physicsdata_except_physicsdata():
    unit = "dimensionless"
    value = 2
    x = as_physicsdata(value)
    assert isinstance(x, PhysicsData)
    assert x.value == value
    assert x.unit == unit
