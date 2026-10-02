import numpy as np
import pytest

from seem_block_system import BlockSystem, Tolerances, evaluate_surfaces
from seem_block_system.geometry import normalize


def test_c_zero_keeps_reference_error_annihilated():
    sys = BlockSystem(dim=64, c=0.0, seed=7)
    sys.run(steps=80, noise_scale=0.08)
    assert np.linalg.norm(sys.e_r) < 1e-15
    assert np.allclose(sys.r, sys.r0)
    surf = evaluate_surfaces(sys)
    assert surf.i1_ref_integrity
    assert surf.d_ref <= Tolerances().eps_ref
    assert surf.p_norm < 1e-12


def test_c_nonzero_contaminates_reference():
    sys = BlockSystem(dim=64, c=0.2, seed=7)
    sys.run(steps=80, noise_scale=0.08)
    assert np.linalg.norm(sys.e_r) > 1e-6
    surf = evaluate_surfaces(sys)
    assert not surf.i1_ref_integrity
    assert surf.d_ref > Tolerances().eps_ref


def test_spectral_block_form_c_zero():
    """J_B = diag(J_x, 0) when C=0: reference eigenvalue annihilated."""
    j_x = 0.85
    J_B = np.array([[j_x, 0.0], [0.0, 0.0]])
    eigs = np.sort(np.linalg.eigvals(J_B).real)
    assert eigs[0] == pytest.approx(0.0)
    assert eigs[1] == pytest.approx(j_x)


def test_i2_i4_pass_under_moderate_noise_when_isolated():
    sys = BlockSystem(dim=64, c=0.0, j_x=0.7, seed=3)
    sys.run(steps=40, noise_scale=0.03)
    surf = evaluate_surfaces(sys)
    assert surf.i2_state_angular
    assert surf.i4_reconstruction
    assert surf.all_pass


def test_i3_representational_independence_default_codebook():
    sys = BlockSystem(dim=128, c=0.0, seed=11)
    surf = evaluate_surfaces(sys)
    assert surf.i3_representational
    assert surf.cross < Tolerances().tau_cross
    assert surf.cross < 1e-12  # Gram-Schmidt vs r0 at init


def test_i3_fails_when_codebook_aligned():
    sys = BlockSystem(dim=32, c=0.0, seed=2)
    sys.v_code = sys.r0.copy()  # force |v_i·v_j| = 1
    surf = evaluate_surfaces(sys)
    assert not surf.i3_representational
    assert surf.cross == pytest.approx(1.0)


def test_refresh_resets_contaminated_reference():
    sys = BlockSystem(dim=32, c=0.3, seed=1)
    sys.run(steps=30, noise_scale=0.1)
    assert not evaluate_surfaces(sys).i1_ref_integrity
    sys.refresh_reference()
    assert evaluate_surfaces(sys).i1_ref_integrity
    assert np.linalg.norm(sys.e_r) < 1e-15


def test_normalize_helper_used_by_dynamics():
    v = normalize(np.array([0.0, 2.0, 0.0]))
    assert v[1] == pytest.approx(1.0)
