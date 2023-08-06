import sympy

from ueca.data import PhysicsData, ureg
from ueca.symbolf import cancel, diff, sqrt


def combined_standard_uncertainty(obj: PhysicsData, prefix: str = "Delta",
                                  relative: bool = False, use_cancel: bool = True) -> PhysicsData:
    if relative:
        sum_of_squares = PhysicsData(None, unit="dimensionless", symbol=sympy.S.Zero)
    else:
        sum_of_squares = PhysicsData(None, unit=str(obj.data.units ** 2), symbol=sympy.S.Zero)

    for symbol_name, data in obj._base_symbols.items():
        if isinstance(data, ureg.Measurement):
            unit = str(data.units)
            symbol = PhysicsData(data.magnitude, unit, symbol=symbol_name)
            delta = PhysicsData(data.error.magnitude, unit, symbol=f"{prefix} {symbol_name}")
            square_root = diff(obj, symbol, 1) * delta
            if relative:
                square_root = square_root / obj

            if use_cancel:
                square_root = cancel(square_root)

            sum_of_squares += square_root ** 2

    output = sqrt(sum_of_squares, apply_dim=True)
    return output
