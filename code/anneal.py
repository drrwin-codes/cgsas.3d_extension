import time


def anneal(system, t_start=4.0, t_end=1.0, cooling_factor=0.85, sweeps_per_stage=400,
            production_sweeps=2000, enhanced=True, verbose=True):
    """Geometric cooling schedule combined with the enhanced chain-relocation
    move. Temperature alone lets local moves accept more unfavorable steps,
    but can't help a whole chain escape a crowded region -- that needs the
    relocation move. Combining both: explore at high T (weak effective
    interactions + free chain relocation), gradually cool to T=1 (the
    validated physical energy scale), then run production sweeps at T=1."""
    t0 = time.time()
    T = t_start
    stage = 0
    while T > t_end:
        system.temperature = T
        system.run(sweeps_per_stage, enhanced=enhanced)
        stage += 1
        if verbose:
            print(f'  stage {stage}: T={T:.2f}  E={system.total_energy():.0f}  '
                  f't={time.time()-t0:.0f}s')
        T *= cooling_factor
    system.temperature = t_end
    system.run(production_sweeps, enhanced=enhanced)
    if verbose:
        print(f'  production ({production_sweeps} sweeps @ T={t_end}): '
              f'E={system.total_energy():.0f}  total_t={time.time()-t0:.0f}s')
    return system
