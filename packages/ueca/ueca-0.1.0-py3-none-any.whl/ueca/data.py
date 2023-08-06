import pint
import sympy

import copy
from numbers import Real
from typing import Any, Optional, Union

from ueca.latex import translate_space_latex


ureg = pint.UnitRegistry()
ureg.default_system = "SI"


class PhysicsData:
    def __init__(self, value: Any, unit: str, left_side: str = "",
                 symbol: Optional[Union[str, sympy.Basic]] = None,
                 uncertainty: Optional[Real] = None,
                 base_symbols: Optional[dict] = None) -> None:
        if isinstance(symbol, str):
            if not symbol.isdecimal() and symbol != "":
                symbol = sympy.Symbol(symbol)

        if isinstance(symbol, sympy.Basic):
            self.data = ureg.Quantity(symbol, unit)
        else:
            self.data = ureg.Quantity(value, unit)
            if uncertainty:
                self.data = self.data.plus_minus(uncertainty)

        self.symbol = symbol
        self.__uncertainty = uncertainty
        self.left_side = left_side

        if base_symbols is None:
            self._base_symbols = dict()
        else:
            self._base_symbols = base_symbols

        if isinstance(symbol, sympy.Symbol) and str(symbol) not in self._base_symbols:
            data = ureg.Quantity(value, unit)
            if uncertainty:
                data = data.plus_minus(uncertainty)
            self._base_symbols[str(symbol)] = data

    @property
    def value(self) -> Any:
        if self.is_symbolic():
            base_symbols = sorted(self._base_symbols.keys())
            symbol_args = [sympy.Symbol(k) for k in base_symbols]
            values = []
            for k in base_symbols:
                data = self._base_symbols[k]
                if isinstance(data, ureg.Measurement):
                    data = data.value
                values.append(data.magnitude)
            return sympy.lambdify(symbol_args, self.symbol, modules="numpy")(*values)
        return self.data.magnitude

    @property
    def unit(self) -> str:
        return str(self.data.units)

    @property
    def uncertainty(self) -> Optional[Real]:
        if isinstance(self.data, ureg.Measurement):
            return self.data.error.magnitude
        return self.__uncertainty

    def is_symbolic(self) -> bool:
        if isinstance(self.symbol, sympy.Basic):
            return True
        return False

    def __new_instance_updated(self, value: Any, unit: str,
                               other: "PhysicsData") -> "PhysicsData":
        if self.is_symbolic():
            symbols = copy.deepcopy(self._base_symbols)
            symbols.update(other._base_symbols)
            return PhysicsData(None, unit, symbol=value,
                               base_symbols=symbols)
        elif other.is_symbolic():
            return PhysicsData(None, unit, symbol=value,
                               base_symbols=other._base_symbols)
        else:
            return PhysicsData(value, unit)

    def __add__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data + other.data
        return self.__new_instance_updated(new_data.magnitude, str(new_data.units), other)

    __radd__ = __add__

    def __sub__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data - other.data
        return self.__new_instance_updated(new_data.magnitude, str(new_data.units), other)

    def __rsub__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = other.data - self.data
        return self.__new_instance_updated(new_data.magnitude, str(new_data.units), other)

    def __mul__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data * other.data
        return self.__new_instance_updated(new_data.magnitude, str(new_data.units), other)

    __rmul__ = __mul__

    def __floordiv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_value = self.data.magnitude // other.data.magnitude
        new_unit = str(self.data.units / other.data.units)
        return self.__new_instance_updated(new_value, new_unit, other)

    def __rfloordiv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_value = other.data.magnitude // self.data.magnitude
        new_unit = str(other.data.units / self.data.units)
        return self.__new_instance_updated(new_value, new_unit, other)

    def __truediv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = self.data / other.data
        return self.__new_instance_updated(new_data.magnitude, str(new_data.units), other)

    def __rtruediv__(self, other: Any) -> "PhysicsData":
        other = as_physicsdata(other)
        new_data = other.data / self.data
        return self.__new_instance_updated(new_data.magnitude, str(new_data.units), other)

    def __pow__(self, n: Union[int, float]) -> "PhysicsData":
        other = as_physicsdata(n)
        new_data = self.data ** other.data
        return self.__new_instance_updated(new_data.magnitude, str(new_data.units), other)

    def __repr__(self) -> str:
        return str(self.data)

    def _repr_html_(self) -> str:
        return self.__repr__()

    def _repr_latex_(self, force_value: bool = False, symbolic_unit: bool = True) -> str:
        latex_spec = "{:~L}"
        if not symbolic_unit:
            latex_spec = latex_spec.replace("~", "")

        if self.is_symbolic():
            if force_value:
                data = PhysicsData(self.value, self.unit).data
                if self.uncertainty:
                    data = data.plus_minus(self.uncertainty)
            else:
                with translate_space_latex():
                    data = PhysicsData(sympy.latex(self.symbol), self.unit).data
        else:
            data = self.data

        text = latex_spec.format(data)

        if self.unit == "dimensionless":
            text = text.rstrip()
            if text.endswith("\\"):
                text = text[:-1]

        if self.left_side != "":
            text = f"{self.left_side} = {text}"

        return text

    def subs(self) -> "PhysicsData":
        return PhysicsData(self.value, self.unit, uncertainty=self.uncertainty)

    def unit_to(self, unit: str):
        new_data = self.data.to(unit)
        return PhysicsData(new_data.magnitude, str(new_data.units), symbol=self.symbol,
                           base_symbols=self._base_symbols)

    def to_latex(self, force_value: bool = False, symbolic_unit: bool = True) -> str:
        return f"${self._repr_latex_(force_value=force_value, symbolic_unit=symbolic_unit)}$"


def as_physicsdata(obj, symbol=None) -> PhysicsData:
    if not isinstance(obj, PhysicsData):
        obj = PhysicsData(obj, "dimensionless", symbol=symbol)
    return obj
