from ueca.constants import c, e, epsilon_0, g, G, h, k, m_e, m_p, m_u, mu_0, N_A, R


class TestConstants:
    def test_c(self):
        assert c.value == 2.99792458E8
        assert c.unit == "meter / second"

    def test_e(self):
        assert e.value == 1.602176634E-19
        assert e.unit == "coulomb"

    def test_epsilon_0(self):
        assert epsilon_0.value == 8.8541878128E-12
        assert epsilon_0.unit == "farad / meter"

    def test_g(self):
        assert g.value == 9.80665
        assert g.unit == "meter / second ** 2"

    def test_G(self):
        assert G.value == 6.6743E-11
        assert G.unit == "meter ** 2 * newton / kilogram ** 2"

    def test_h(self):
        assert h.value == 6.62607015E-34
        assert h.unit == "joule * second"

    def test_k(self):
        assert k.value == 1.380649E-23
        assert k.unit == "joule / kelvin"

    def test_m_e(self):
        assert m_e.value == 9.1093837015E-31
        assert m_e.unit == "kilogram"

    def test_m_p(self):
        assert m_p.value == 1.67262192369E-27
        assert m_p.unit == "kilogram"

    def test_m_u(self):
        assert m_u.value == 1.6605390666E-27
        assert m_u.unit == "kilogram"

    def test_mu_0(self):
        assert mu_0.value == 1.25663706212E-6
        assert mu_0.unit == "henry / meter"

    def test_N_A(self):
        assert N_A.value == 6.02214076E23
        assert N_A.unit == "1 / mole"

    def test_R(self):
        assert R.value == 8.314462618
        assert R.unit == "joule / kelvin / mole"
