"""Isolated block-diagonal dynamics with optional contamination contrast.

Composite error z_t = [e^x; e^r]. Strict isolation is C = 0, so

    J_B = [[J_x, 0],
           [0,   0]]

Operational noise may move the operational state; the reference register
is algebraically annihilated between intentional refreshes when C = 0.
A nonzero C injects operational residual into the reference for contrast.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .geometry import normalize, project_tangent


@dataclass(frozen=True)
class Tolerances:
    """Explicit finite-precision epsilons for I1–I4 (Claim-0 defaults)."""

    eps_ref: float = 1e-9
    theta_max: float = 0.50  # radians ~29 deg operational budget
    tau_cross: float = 0.25
    r_max: float = 0.40


@dataclass
class BlockSystem:
    """Minimal C=0 (or C≠0 contrast) block-system on unit hyperspheres."""

    dim: int = 64
    j_x: float = 0.85  # scalar contraction on operational residual
    c: float = 0.0  # operational→reference coupling; 0 = isolation
    seed: int | None = 0

    def __post_init__(self) -> None:
        if self.dim < 4:
            raise ValueError("dim must be >= 4")
        rng = np.random.default_rng(self.seed)
        self.rng = rng
        self.r0 = normalize(rng.normal(size=self.dim))
        self.r = self.r0.copy()
        # Operational target / cleanup attractor (independent of reference)
        self.x_star = normalize(rng.normal(size=self.dim))
        self.x = self.x_star.copy()
        # Second codebook vector for I3; Gram-Schmidt vs r0 so default cross ≈ 0
        v = rng.normal(size=self.dim)
        v = v - np.dot(self.r0, v) * self.r0
        self.v_code = normalize(v)
        self.e_x = np.zeros(self.dim)
        self.e_r = np.zeros(self.dim)
        self.t = 0

    @property
    def isolated(self) -> bool:
        return abs(self.c) < 1e-15

    def refresh_reference(self) -> None:
        """Intentional refresh: reset reference to r0 and clear e_r."""
        self.r = self.r0.copy()
        self.e_r = np.zeros(self.dim)

    def step(self, noise_scale: float = 0.05) -> dict:
        """One discrete step of composite error dynamics.

        When C=0:
            e^r_{t+1} = 0  (annihilated)
            e^x_{t+1} = J_x e^x_t + η_t
        When C≠0:
            e^r gets a C-scaled tangent push from the operational residual.
        """
        # Isotropic noise with ||η|| ≈ noise_scale (not noise_scale·√D)
        raw = self.rng.normal(size=self.dim)
        eta = raw * (noise_scale / (np.linalg.norm(raw) + 1e-15))
        # Operational residual update
        self.e_x = self.j_x * self.e_x + eta
        # Apply residual in the tangent space at x_star, then renormalize
        self.x = normalize(self.x_star + project_tangent(self.x_star, self.e_x))

        if self.isolated:
            self.e_r = np.zeros(self.dim)
            self.r = self.r0.copy()
        else:
            # Contamination: leak operational residual into reference frame
            leak = self.c * project_tangent(self.r, self.e_x)
            self.e_r = self.e_r + leak
            self.r = normalize(self.r0 + project_tangent(self.r0, self.e_r))

        self.t += 1
        return {
            "t": self.t,
            "c": float(self.c),
            "e_x_norm": float(np.linalg.norm(self.e_x)),
            "e_r_norm": float(np.linalg.norm(self.e_r)),
        }

    def run(self, steps: int = 50, noise_scale: float = 0.05) -> list[dict]:
        return [self.step(noise_scale=noise_scale) for _ in range(steps)]

    def cleanup(self, x: np.ndarray | None = None) -> np.ndarray:
        """Toy cleanup: project toward x_star (identity attractor)."""
        x = self.x if x is None else np.asarray(x, dtype=float)
        # Soft pull: average with attractor then normalize
        return normalize(0.5 * (normalize(x) + self.x_star))
