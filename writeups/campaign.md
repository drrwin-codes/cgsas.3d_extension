# 3D Campaign Results

Builds on `validation_3d_writeup.md`. Full grid: g ∈ {0.125, 0.375, 0.625, 0.875} ×
φ ∈ {0.15, 0.25, 0.35}, 2 seeds per point, 24 runs total, all using the protocol developed
during validation: simulated annealing (T=4.0 → 1.0, geometric cooling, factor 0.85) combined
with the enhanced chain-relocation move, followed by production sweeps at T=1.

## Why the protocol changed mid-campaign

The original plan used fixed-temperature sweeps, reserving the expensive enhanced-sampling
protocol for a "risk zone." Partway through, evidence showed that risk zone was wrong on two
counts: it wasn't primarily geometry-driven (g=0.375 at φ=0.25 showed large aggregation that a
g-only threshold would have missed) and even the "safe" low-concentration tier showed
unequilibrated, strongly positive energies at high g. Rather than keep patching thresholds,
we researched and adopted simulated annealing combined with the enhanced move as the standard
protocol for every point — which turned out to be both more reliable *and* roughly 5x faster
per run than the brute-force fixed-temperature approach it replaced.

## What we found

- **Aggregation grows sharply with g and plateaus at complete merger.** At φ=0.25-0.35, every
  point with g≥0.375 shows the maximum aggregate containing all or nearly all chains in the
  system (e.g. 250/250 at φ=0.25, g=0.625; 350/350 at φ=0.35, g≥0.625). This isn't a numerical
  artifact — it reproduced consistently across both seeds with tightly matching energies.
- **This differs qualitatively from the 2D result.** 2D showed a progression through discrete
  micelle → cylinder → vesicle regimes at intermediate sizes. 3D, once conditions favor
  aggregation at all, tends toward complete macroscopic phase separation rather than stabilizing
  at an intermediate aggregate size. This is a believable real phenomenon -- sufficiently
  hydrophobic amphiphiles (too little head group to stabilize discrete structures) are known to
  behave more like separating oil than forming stable micelles/vesicles -- but it means our grid,
  as scoped, mostly samples "does it phase-separate" rather than resolving fine structure once it
  does.
- **We never observed a genuine closed-shell vesicle (trapped interior volume) anywhere in the
  grid.** Every "bilayer/vesicle" classification here is the box-spanning periodic sheet variety,
  not a real closed shell. Three honest possibilities, not distinguished by this campaign: our
  detection thresholds (min pocket size 8, min aggregation number 20) may be too strict; a closed
  shell may need conditions outside this grid (finer geometry resolution around where sheets first
  form, rather than this coarse 4-point sweep); or L=20 may simply be too small for a closed shell
  to be favorable over a periodic sheet.
- **Only g=0.125 stays in genuinely discrete-aggregate territory** across the whole concentration
  range tested (max aggregate 17 to 31 chains, never full merger) -- this is the one region of the
  grid behaving like classic micellar self-assembly rather than phase separation.

## Honest limitations of this campaign specifically

- Coarse grid (4x3) relative to the validated 2D campaign (7x4) -- a real trade against compute
  cost, not a claim of matching resolution.
- 2 seeds per point, not 4 -- real uncertainty here is less tightly bounded than in 2D.
- No finite-size check yet at this L=20 scale for the campaign grid specifically (the validation
  phase's finite-size-adjacent findings don't directly cover this).
- The complete-merger result at high g/phi is itself a plausible candidate for the same kind of
  persistent multistability found during validation -- we did not re-run the full metastability
  check (clustered vs. dispersed start) at every campaign point, only at the validation points.

## Materials

`chunked_anneal.py` (the production driver used for every point in this campaign),
`sweep_3d_results.csv` (raw results), `phase_diagram_3d.png`.
