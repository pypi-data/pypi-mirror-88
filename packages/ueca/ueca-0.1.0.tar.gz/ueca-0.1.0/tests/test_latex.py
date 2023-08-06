import sympy

from ueca.latex import translate_space_latex


def test_translate_space_latex():
    delta_lambda = sympy.Symbol("Delta lambda")

    assert sympy.latex(delta_lambda) == "Delta lambda"

    with translate_space_latex():
        assert sympy.latex(delta_lambda) == r"\Delta \lambda"
