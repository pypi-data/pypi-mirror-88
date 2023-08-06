import numpy as np
import pytest

from ueca.data import PhysicsData
from ueca.symbolf import Rational
from ueca.uncertainty import combined_standard_uncertainty


def test_combined_standard_uncertainty_calculation():
    mass = PhysicsData(2.5, "kilogram", symbol="M", uncertainty=1.3)
    outer_diameter = PhysicsData(3.1, "meter", symbol="D_1", uncertainty=0.81)
    inner_diameter = PhysicsData(4.2, "meter", symbol="D_2", uncertainty=1.1)
    moment_of_inertia = Rational(1, 8) * mass * (outer_diameter ** 2 + inner_diameter ** 2)
    delta_I = combined_standard_uncertainty(moment_of_inertia)
    assert delta_I.unit == "kilogram * meter ** 2"
    expectation = np.sqrt((mass.uncertainty * (outer_diameter.value ** 2
                          + inner_diameter.value ** 2) / 8) ** 2
                          + (mass.value * outer_diameter.value
                             * outer_diameter.uncertainty / 4) ** 2
                          + (mass.value * inner_diameter.value
                             * inner_diameter.uncertainty / 4) ** 2)
    assert pytest.approx(delta_I.value) == expectation
    delta_I_relative = combined_standard_uncertainty(moment_of_inertia, relative=True)
    expectation = np.sqrt((mass.uncertainty / mass.value) ** 2
                          + ((2 * outer_diameter.value * outer_diameter.uncertainty) ** 2
                              + (2 * inner_diameter.value * inner_diameter.uncertainty) ** 2)
                          / (outer_diameter.value ** 2 + inner_diameter.value ** 2) ** 2)
    assert pytest.approx(delta_I_relative.value) == expectation
    assert delta_I_relative.unit == "dimensionless"
