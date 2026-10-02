"""Claim-0 Block-System isolation monitors (not a proof, not AGI)."""

from .geometry import geodesic_distance, normalize, tangent_projection_norm
from .dynamics import BlockSystem, Tolerances
from .monitors import FailureSurfaces, evaluate_surfaces

__all__ = [
    "BlockSystem",
    "Tolerances",
    "FailureSurfaces",
    "evaluate_surfaces",
    "geodesic_distance",
    "normalize",
    "tangent_projection_norm",
]

__version__ = "0.1.0"
