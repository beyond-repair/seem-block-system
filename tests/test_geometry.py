import numpy as np
import pytest

from seem_block_system.geometry import (
    geodesic_distance,
    normalize,
    tangent_projection_norm,
)


def test_normalize_unit():
    v = normalize(np.array([3.0, 4.0]))
    assert abs(np.linalg.norm(v) - 1.0) < 1e-12


def test_geodesic_identical_zero():
    a = normalize(np.ones(8))
    assert geodesic_distance(a, a) < 1e-12


def test_geodesic_orthogonal_is_pi_over_2():
    a = np.array([1.0, 0.0, 0.0])
    b = np.array([0.0, 1.0, 0.0])
    assert geodesic_distance(a, b) == pytest.approx(np.pi / 2)


def test_tangent_projection_norm_identity():
    a = normalize(np.random.default_rng(1).normal(size=16))
    assert tangent_projection_norm(a, a) < 1e-12
    # Orthogonal: |a·b|=0 → ||P|| = 1
    b = normalize(np.random.default_rng(2).normal(size=16))
    b = b - np.dot(a, b) * a
    b = normalize(b)
    assert abs(np.dot(a, b)) < 1e-12
    assert tangent_projection_norm(a, b) == pytest.approx(1.0)
