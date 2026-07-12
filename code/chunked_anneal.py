import sys, pickle, random, time
from lattice_mc_3d import System3D
from cluster_analysis_3d import classify_system

T_START, T_END, COOLING, SWEEPS_PER_STAGE, PRODUCTION_SWEEPS = 4.0, 1.0, 0.85, 200, 1000

# precompute the full stage temperature schedule
_schedule = []
T = T_START
while T > T_END:
    _schedule.append(T)
    T *= COOLING
N_STAGES = len(_schedule)

action = sys.argv[1]
ckpt = sys.argv[2]

if action == 'init':
    n_chains, nh, nt, seed = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
    s = System3D(L=20, n_chains=n_chains, n_head=nh, n_tail=nt, rng=random.Random(seed))
    with open(ckpt, 'wb') as f:
        pickle.dump((s, 0), f)  # (system, next_stage_index)
    print(f'init: {n_chains} chains, {N_STAGES} stages planned, E={s.total_energy():.0f}')

elif action == 'stages':
    stage_from, stage_to = int(sys.argv[3]), int(sys.argv[4])  # e.g. 0,3 = run stages 0,1,2
    t0 = time.time()
    with open(ckpt, 'rb') as f:
        s, _ = pickle.load(f)
    for i in range(stage_from, stage_to):
        s.temperature = _schedule[i]
        s.run(SWEEPS_PER_STAGE, enhanced=True)
    with open(ckpt, 'wb') as f:
        pickle.dump((s, stage_to), f)
    print(f'stages {stage_from}-{stage_to-1} done in {time.time()-t0:.0f}s, '
          f'T={_schedule[stage_to-1]:.2f}, E={s.total_energy():.0f}')

elif action == 'production':
    t0 = time.time()
    with open(ckpt, 'rb') as f:
        s, stage_idx = pickle.load(f)
    assert stage_idx >= N_STAGES, f'only completed {stage_idx}/{N_STAGES} stages'
    s.temperature = T_END
    s.run(PRODUCTION_SWEEPS, enhanced=True)
    with open(ckpt, 'wb') as f:
        pickle.dump((s, stage_idx), f)
    print(f'production done in {time.time()-t0:.0f}s, E={s.total_energy():.0f}')

elif action == 'finalize':
    phi_label, g_label, seed_label = sys.argv[3], sys.argv[4], sys.argv[5]
    with open(ckpt, 'rb') as f:
        s, _ = pickle.load(f)
    results, vesicle_info = classify_system(s)
    total_chains = sum(r['agg_number'] for r in results)
    mean_agg = sum(r['agg_number'] ** 2 for r in results) / total_chains
    max_agg = max(r['agg_number'] for r in results)
    chains_by_label = {}
    for r in results:
        chains_by_label[r['label']] = chains_by_label.get(r['label'], 0) + r['agg_number']
    dominant = max(chains_by_label, key=chains_by_label.get)
    energy = s.total_energy()
    print(f'FINAL phi={phi_label} g={g_label} seed={seed_label} -> mean#={mean_agg:.1f} '
          f'max#={max_agg} label={dominant} n_vesicles={len(vesicle_info)} E={energy:.0f}')
    import csv, os
    write_header = not os.path.exists('sweep_3d_results.csv')
    with open('sweep_3d_results.csv', 'a', newline='') as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(['phi', 'g', 'nh', 'nt', 'seed', 'mean_agg', 'max_agg',
                         'dominant_label', 'n_vesicles', 'energy'])
        nh = s.type_seq.count('H')
        nt = s.type_seq.count('T')
        w.writerow([phi_label, g_label, nh, nt, seed_label, mean_agg, max_agg,
                     dominant, len(vesicle_info), energy])
