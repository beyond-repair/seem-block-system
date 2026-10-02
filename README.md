<div align="center">

[![Lifecycle](https://img.shields.io/badge/●_SUPERSEDED-f59e0b?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)
[![Claim](https://img.shields.io/badge/Claim_0-22c55e?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)
[![Governance](https://img.shields.io/badge/ADL--Governance-7c3aed?style=for-the-badge&labelColor=0f0f23)](https://github.com/beyond-repair/ADL-Governance)

```
LIFECYCLE   SUPERSEDED
CLAIM       0
SUCCESSOR   sovereign-clean-room
```

</div>

> **SUPERSEDED.** Canonical successor: [sovereign-clean-room](https://github.com/beyond-repair/sovereign-clean-room). No new feature work.

---

> **⚠️ SUPERSEDED / ABSORBED:** This repository is a historical archive plus a Claim-0 NumPy monitor. The Block-System theorem for ongoing Clean-Room work lives in **[sovereign-clean-room](https://github.com/beyond-repair/sovereign-clean-room)** at [`docs/BLOCK_SYSTEM.md`](https://github.com/beyond-repair/sovereign-clean-room/blob/main/docs/BLOCK_SYSTEM.md).
>
> A self-contained archive copy of the v1.3 theorem is restored here at [`docs/BLOCK_SYSTEM.md`](./docs/BLOCK_SYSTEM.md).

---

# SEEM Block-System Isolation Theorem (LEGACY + Claim-0 sketch)

**Purpose:** Eliminate runaway phase drift and reference-frame contamination under continuous high-throughput operational loads by isolating the reference registry from operational feedback (`C = 0` block-diagonal dynamics).

This tree ships:

1. The restored Block-System-v1.3 mathematical specification ([`docs/BLOCK_SYSTEM.md`](./docs/BLOCK_SYSTEM.md)).
2. A minimal Python + NumPy reference that enforces `C = 0`, monitors failure surfaces I₁–I₄ with geodesic / spherical distances, and contrasts contamination when `C ≠ 0`.

**Not a mind. Not AGI. Not a theorem proof.** Explicit ε-tolerances only. See [CLAIM_STATUS.md](./CLAIM_STATUS.md).

Aligned conceptually with Clean-Room v1.3: single-pass unbind, hyperspherical geometry, invertibility gate, sandbox boundary — implemented in the successor, not here.

---

## Prefer the final form

```bash
git clone https://github.com/beyond-repair/sovereign-clean-room.git
cd sovereign-clean-room
# see that repo's README for install / run
```

## Historical Claim-0 quickstart (offline runnable sketch)

```bash
git clone https://github.com/beyond-repair/seem-block-system.git
cd seem-block-system
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
seem-block-system
seem-block-system --json
```

### What the demo shows

- **`C = 0`:** `||e^r|| ≈ 0`, reference integrity I₁ holds (`d_S(r_t, r_0) ≤ ε_ref`), I₂–I₄ monitored under operational noise.
- **`C ≠ 0` contrast:** reference drifts; I₁ fails — operational noise contaminates the registry.

### Tolerances (defaults)

| Symbol | Meaning | Default |
|--------|---------|---------|
| `ε_ref` | I₁ reference geodesic budget | `1e-9` |
| `θ_max` | I₂ operational angular budget | `0.50` rad |
| `τ_cross` | I₃ codebook cross-talk | `0.25` |
| `R_max` | I₄ cleanup geodesic budget | `0.40` |

---

## What this line contributed

- Canonical Block-System Isolation Theorem (v1.3): `C = 0`, block-diagonal `J_B`, spectral annihilation of the reference mode
- Calibrated failure surfaces I₁–I₄ (Reference / State Angular / Representational / Reconstruction integrity)
- Tangent projection diagnostic `||P_a(b)||_2 = √(1 − (a·b)²)`
- Claim-0 NumPy isolation monitors (this sketch)

## License

See [LICENSE](./LICENSE).

---

<div align="center">

**REWRITE · BUILD · TRANSCEND**

Governing source: [ADL-Governance](https://github.com/beyond-repair/ADL-Governance) · [Claim levels 0–5](https://github.com/beyond-repair/ADL-Governance/blob/main/docs/CLAIM_VALIDATION.md)

</div>
