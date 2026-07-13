# addendum: why are there no vesicles?

Following the campaign, I investigated why 24 runs never produced a closed-shell
vesicle (trapped interior volume), despite validated detection code and abundant "bilayer/vesicle"
(box-spanning) classifications.

## the hypothesis

Vesicle formation literature (e.g. arXiv:2002.05930, a closely analogous coarse-grained
self-assembly study) establishes that a growing bilayer patch eliminates its energetically
costly exposed edge one of two ways: curling into a closed vesicle, or extending into an
edge-free periodic sheet. A periodic simulation box offers the sheet route "for free" -- once a
patch wraps around the box, it has zero edges without ever needing to bend. Our working
hypothesis: L=20 was small enough that patches reached the box-spanning shortcut before they
were ever large/curved enough to consider closing into a sphere.

## what i tested

Reran the annealing+enhanced protocol at L=30 (50% larger, ~3.4x the volume) with a matched
chain count, first at g=0.375 (nh=5, nt=3 -- more heads than tails), then corrected to a
genuinely tail-majority composition, g=0.875 (nh=1, nt=7), which is the physically appropriate
regime for bilayer formation.

## what i found

> - **The g=0.375 test was the wrong regime entirely** -- visual inspection showed a compact,
  roughly spherical blob, not a flat patch. With more heads than tails, that's the physically
  correct outcome (a small tail core with a head shell, i.e. a large micelle), not a bilayer
  candidate. Caught by actually looking at the 3D structure, not just reading aggregation numbers
  -- the "bilayer/vesicle" label it received was a topological artifact (box-spanning in one
  dimension) rather than evidence of real membrane morphology.

> - **The corrected g=0.875 test confirmed the right physics**: a genuine flat, sheet-like
  structure formed (visible directly in `largest_aggregate_shape_g0875.png` as flat slab
  fragments, an artifact of periodic wraparound splitting one continuous sheet into
  apparently-separate pieces).

> - **The sheet still took the box-spanning shortcut at L=30**, ruling out "just needs more room"
  as a complete explanation. Small (size-1) water pockets appeared but nothing resembling a real enclosed interior.

## conclusion

The periodic-shortcut hypothesis is real but incomplete. The more likely full picture: our move
set (single-bead kinks, end-moves, whole-chain relocation) can grow and merge sheets efficiently
but has no move specifically suited to `*collective bending*`. Curling an extended sheet into a
sphere requires many coordinated local rearrangements happening together, which isn't what any of
our current moves target. This is a testable follow-up (a purpose-built curvature-inducing move,
or a much larger box to see if the shortcut eventually loses its advantage).

## materials

`largest_aggregate_shape.png` (head-majority blob, g=0.375), `largest_aggregate_shape_g0875.png`
(tail-majority sheet, g=0.875); both from L=30 room tests, checkpoints in `ckpt_room_L30*.pkl`.
