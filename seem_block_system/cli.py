"""Console entry: seem-block-system — Claim-0 isolation demo."""

from __future__ import annotations

import argparse
import json
import sys

import numpy as np

from .dynamics import BlockSystem, Tolerances
from .monitors import evaluate_surfaces


def _run_demo(steps: int, dim: int, seed: int, noise: float) -> dict:
    tol = Tolerances()

    isolated = BlockSystem(dim=dim, c=0.0, seed=seed)
    isolated.run(steps=steps, noise_scale=noise)
    iso_surf = evaluate_surfaces(isolated, tol)

    contaminated = BlockSystem(dim=dim, c=0.15, seed=seed)
    contaminated.run(steps=steps, noise_scale=noise)
    cont_surf = evaluate_surfaces(contaminated, tol)

    return {
        "claim": 0,
        "lifecycle": "SUPERSEDED",
        "successor": "sovereign-clean-room",
        "disclaimer": (
            "Claim-0 sketch only: NumPy monitors of C=0 isolation and I1–I4. "
            "Not a theorem proof, not AGI, not a mind."
        ),
        "steps": steps,
        "dim": dim,
        "noise_scale": noise,
        "tolerances": {
            "eps_ref": tol.eps_ref,
            "theta_max": tol.theta_max,
            "tau_cross": tol.tau_cross,
            "r_max": tol.r_max,
        },
        "C_equals_0": {
            "e_r_norm": float(np.linalg.norm(isolated.e_r)),
            "surfaces": iso_surf.as_dict(),
        },
        "C_nonzero_contrast": {
            "c": contaminated.c,
            "e_r_norm": float(np.linalg.norm(contaminated.e_r)),
            "surfaces": cont_surf.as_dict(),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="seem-block-system",
        description=(
            "Claim-0 Block-System isolation demo (C=0 vs C≠0 contrast). "
            "SUPERSEDED archive — successor: sovereign-clean-room."
        ),
    )
    parser.add_argument("--steps", type=int, default=50, help="simulation steps")
    parser.add_argument("--dim", type=int, default=64, help="embedding dimension")
    parser.add_argument("--seed", type=int, default=0, help="RNG seed")
    parser.add_argument("--noise", type=float, default=0.05, help="operational noise scale")
    parser.add_argument("--json", action="store_true", help="emit JSON report only")
    args = parser.parse_args(argv)

    report = _run_demo(args.steps, args.dim, args.seed, args.noise)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("SEEM Block-System Isolation — Claim-0 sketch")
    print("Lifecycle: SUPERSEDED → sovereign-clean-room")
    print("Not a theorem proof. Not AGI. Explicit ε-tolerances only.\n")
    iso = report["C_equals_0"]
    cont = report["C_nonzero_contrast"]
    print(f"C=0 isolation after {report['steps']} steps:")
    print(f"  ||e^r|| = {iso['e_r_norm']:.3e}")
    print(
        f"  I1 ref integrity: {iso['surfaces']['I1_reference_integrity']} "
        f"(d_S={iso['surfaces']['d_ref']:.3e})"
    )
    print(
        f"  I2 state angular: {iso['surfaces']['I2_state_angular_integrity']} "
        f"(θ={iso['surfaces']['theta']:.4f})"
    )
    print(
        f"  I3 independence:  {iso['surfaces']['I3_representational_independence']} "
        f"(cross={iso['surfaces']['cross']:.4f})"
    )
    print(
        f"  I4 cleanup:       {iso['surfaces']['I4_reconstruction_cleanup']} "
        f"(d={iso['surfaces']['d_cleanup']:.4f})"
    )
    print(f"  all_pass={iso['surfaces']['all_pass']}")
    print()
    print(f"C={cont['c']} contamination contrast:")
    print(f"  ||e^r|| = {cont['e_r_norm']:.3e}")
    print(
        f"  I1 ref integrity: {cont['surfaces']['I1_reference_integrity']} "
        f"(d_S={cont['surfaces']['d_ref']:.3e})"
    )
    print("  (expect I1 FAIL / nonzero e^r when C≠0)")
    ok = iso["surfaces"]["all_pass"] and iso["e_r_norm"] < 1e-12
    print()
    print("OK" if ok else "CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
