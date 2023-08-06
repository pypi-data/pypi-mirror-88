from scipy.constants import physical_constants

from ueca.data import PhysicsData


# 真空中の光速度
c = PhysicsData(*physical_constants["speed of light in vacuum"][:2], symbol="c")

# 素電荷
e = PhysicsData(*physical_constants["atomic unit of charge"][:2], symbol="e")

# 電気定数
epsilon_0 = PhysicsData(*physical_constants["vacuum electric permittivity"][:2], symbol="epsilon_0")

# 重力加速度(標準値)
g = PhysicsData(*physical_constants["standard acceleration of gravity"][:2], symbol="g")

# 万有引力定数
G = PhysicsData(*physical_constants["Newtonian constant of gravitation"][:2],
                symbol="G").unit_to("N*m^2/kg^2")

# プランク定数
h = PhysicsData(*physical_constants["Planck constant"][:2], symbol="h").unit_to("J*s")

# ボルツマン定数
k = PhysicsData(*physical_constants["Boltzmann constant"][:2], symbol="k")

# 電子の質量
m_e = PhysicsData(*physical_constants["electron mass"][:2], symbol="m_e")

# 陽子の質量
m_p = PhysicsData(*physical_constants["proton mass"][:2], symbol="m_p")

# 原子質量単位
m_u = PhysicsData(*physical_constants["atomic mass constant"][:2], symbol="m_u")

# 磁気定数
mu_0 = PhysicsData(*physical_constants["vacuum mag. permeability"][:2],
                   symbol="mu_0").unit_to("H/m")

# アボガドロ定数
N_A = PhysicsData(*physical_constants["Avogadro constant"][:2], symbol="N_A")

# 気体定数
R = gas_constant = PhysicsData(*physical_constants["molar gas constant"][:2], symbol="R")
