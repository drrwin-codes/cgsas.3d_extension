# Coarse Grained Self Assembly Simulation (3D-Extension)

This is the 3D generalization of the validated 2D coarse-grained amphiphile self-assembly
simulator (separate repo). Same research question, same energy model.. extended to a cubic lattice.

---

<img width="3255" height="1942" alt="image" src="https://github.com/user-attachments/assets/3a66064e-d2e8-487f-b945-7a0960e6ade7" />


---
## what's in this repo

| file | purpose |
|---|---|
| `lattice_mc_3d.py` | Core engine: cubic lattice, chains, moves (end/kink/rigid translation), enhanced chain-relocation move |
| `cluster_analysis_3d.py` | Aggregate detection, gyration-tensor shape descriptors (asphericity, acylindricity, κ²), vesicle/pocket detection |
| `dispersed_3d.py` | Buffered-placement variant used only for metastability testing (not the standard model) |
| `validation_checks_3d.py` | Reproducible equilibration and metastability checks; run these (recomended) |
| `validation_3d_writeup.md` | Full account of the validation phase, including the central finding below |

---

## the one thing to know before touching this code

**Local-move-only "equilibration" is actively misleading in 3D.** A system can look perfectly
stable for thousands of sweeps and still be sitting in a badly trapped local minimum, tens of
thousands of energy units away from where enhanced sampling reveals it should be. Always run
with `enhanced=True` (the chain-relocation move) for anything resembling a real equilibrium
claim 

> --> see `validation_3d_writeup.md` for the full evidence.

Even with enhanced sampling on, we confirmed genuine persistent multistability at the densest,
most tail-heavy point tested `(φ=0.30, g=0.875`): two different starting conditions settle into
stable, non-converging internal energy states 1210 units apart, even after 5,000 enhanced sweeps
on top of 20,000 regular ones. Resolving it fully would need a different technique `(replica exchange
/ parallel tempering.`

## Reproducing the validation

```python
from validation_checks_3d import equilibration_check, metastability_check

# energy vs. sweep number
equilibration_check(nh=2, nt=6, n_chains=100, n_sweeps=8000)

# clustered vs. dispersed start -- chunk/checkpoint for n_sweeps > ~2000,
# enhanced sampling costs ~150-170ms/sweep at higher density
metastability_check(nh=1, nt=7, n_chains=300, enhanced=True, n_sweeps=1000)
```

## Not yet done

A real geometry x concentration campaign (the 3D analog of the validated 2D 28-point phase
sweep).
> every point needs the equilibration + enhanced-sampling protocol established above,
which is a substantial undertaking in its own right.
>
 Recommended to run in a fresh session
building on this validated foundation rather than guessing at shortcuts.
