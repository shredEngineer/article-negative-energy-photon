import sympy as sp

# Symbols
E, c, eps0 = sp.symbols('E c ε₀')

# Metric with signature (- + + +)
eta = sp.diag(-1, 1, 1, 1)

# Mixed-rank Faraday tensor F^μ_ν
F_mixed = sp.Matrix([
    [ 0,   E/c,   0,    0 ],
    [E/c,   0,    0,  -E/c],
    [ 0,    0,    0,    0 ],
    [ 0,   E/c,   0,    0 ]
])

# Raise the second index: F^{μ α} = η^{αν} F^μ_ν
F_upup = sp.Matrix(4, 4, lambda mu, alpha: sum(
    eta[alpha, nu] * F_mixed[mu, nu] for nu in range(4)
))

# Lower the first index: F_{ν α} = η_{ν μ} F^μ_α
F_down = sp.Matrix(4, 4, lambda nu, alpha: sum(
    eta[nu, mu] * F_mixed[mu, alpha] for mu in range(4)
))

# Contract: T^μ_ν = ε₀ ⋅ F^{μ α} ⋅ F_{ν α}
T_mixed = sp.Matrix(4, 4, lambda mu, nu: eps0 * sum(
    F_upup[mu, alpha] * F_down[nu, alpha] for alpha in range(4)
))

# Output
sp.pretty_print(T_mixed)
print(r"T^\mu_{\ \nu} = \varepsilon_0 \cdot " + sp.latex(T_mixed / eps0))
