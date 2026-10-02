"""I1–I4 failure-surface monitors with explicit epsilon gates."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .dynamics import BlockSystem, Tolerances
from .geometry import geodesic_distance, tangent_projection_norm


@dataclass(frozen=True)
class FailureSurfaces:
    i1_ref_integrity: bool
    i2_state_angular: bool
    i3_representational: bool
    i4_reconstruction: bool
    d_ref: float
    theta: float
    cross: float
    d_cleanup: float
    p_norm: float

    @property
    def all_pass(self) -> bool:
        return (
            self.i1_ref_integrity
            and self.i2_state_angular
            and self.i3_representational
            and self.i4_reconstruction
        )

    def as_dict(self) -> dict:
        return {
            "I1_reference_integrity": self.i1_ref_integrity,
            "I2_state_angular_integrity": self.i2_state_angular,
            "I3_representational_independence": self.i3_representational,
            "I4_reconstruction_cleanup": self.i4_reconstruction,
            "d_ref": self.d_ref,
            "theta": self.theta,
            "cross": self.cross,
            "d_cleanup": self.d_cleanup,
            "P_a_norm": self.p_norm,
            "all_pass": self.all_pass,
        }


def evaluate_surfaces(
    system: BlockSystem,
    tolerances: Tolerances | None = None,
) -> FailureSurfaces:
    """Evaluate I1–I4 against explicit tolerances (Claim-0 monitors)."""
    tol = tolerances or Tolerances()

    d_ref = geodesic_distance(system.r, system.r0)
    theta = geodesic_distance(system.x, system.x_star)
    cross = abs(float(np.dot(system.r0, system.v_code)))
    cleaned = system.cleanup()
    d_cleanup = geodesic_distance(cleaned, system.x_star)
    p_norm = tangent_projection_norm(system.r0, system.r)

    return FailureSurfaces(
        i1_ref_integrity=d_ref <= tol.eps_ref,
        i2_state_angular=theta <= tol.theta_max,
        i3_representational=cross < tol.tau_cross,
        i4_reconstruction=d_cleanup < tol.r_max,
        d_ref=d_ref,
        theta=theta,
        cross=cross,
        d_cleanup=d_cleanup,
        p_norm=p_norm,
    )
