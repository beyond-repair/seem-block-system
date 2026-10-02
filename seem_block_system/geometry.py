"""Hyperspherical helpers for I1–I4 monitors."""

from __future__ import annotations

import numpy as np


def normalize(v: np.ndarray) -> np.ndarray:
    """Return a unit vector; raise if the input is near zero."""
    v = np.asarray(v, dtype=float)
    n = float(np.linalg.norm(v))
    if n < 1e-15:
        raise ValueError("cannot normalize near-zero vector")
    return v / n


def geodesic_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Geodesic distance on the unit sphere: arccos(clip(a·b, -1, 1))."""
    a = normalize(a)
    b = normalize(b)
    dot = float(np.clip(np.dot(a, b), -1.0, 1.0))
    return float(np.arccos(dot))


def tangent_projection_norm(a: np.ndarray, b: np.ndarray) -> float:
    """||P_a(b)||_2 = sqrt(1 - (a·b)^2) for unit vectors a, b."""
    a = normalize(a)
    b = normalize(b)
    dot = float(np.clip(np.dot(a, b), -1.0, 1.0))
    return float(np.sqrt(max(0.0, 1.0 - dot * dot)))


def project_tangent(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Orthogonal residual of b onto the tangent space at unit a."""
    a = normalize(a)
    b = np.asarray(b, dtype=float)
    return b - np.dot(a, b) * a
