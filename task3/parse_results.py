#!/usr/bin/env python3
"""Task 3: parse ChampSim logs in <results>/<config>/<trace>.txt into tables.

Configs (directory names):
  baseline       no prefetcher, LRU L2C                  (speedup / coverage reference)
  dyn_irrip      no prefetcher, Dynamic I-RRIP L2C (Task 2B)
  spp_lru        SPP at L1D, LRU L2C                     (standalone SPP, Task 1B)
  spp_dyn_irrip  SPP at L1D, Dynamic I-RRIP L2C without prefetch awareness
  spp_pf_dyn     SPP at L1D, prefetch-aware Dynamic I-RRIP L2C (Task 3)

Speedup  = IPC / IPC of baseline on the same trace.
Accuracy = ChampSim's L1D "USEFUL LOAD PREFETCHES / PREFETCH ISSUED TO LOWER LEVEL".
Coverage = (L1D load misses of baseline - L1D load misses) / L1D load misses of baseline.

Sensitivity runs of the final design live in <results>/sensitivity/<name>/ (pf_ins<r>: prefetch
insertion RRPV, t<T>: leader-set threshold) and get their own tables.

Writes <results>/task3_results.csv and <results>/task3_tables.md.
Usage: python3 task3/parse_results.py [results_dir]   (default results/task3)
"""
import csv, math, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ['baseline', 'dyn_irrip', 'spp_lru', 'spp_dyn_irrip', 'spp_pf_dyn']

PATTERNS = {
    'ipc':            r'Finished CPU 0 instructions: \d+ cycles: \d+ cumulative IPC: ([\d.eE+-]+)',
    'l1d_load_miss':  r'^L1D LOAD\s+ACCESS:\s+\d+\s+HIT:\s+\d+\s+MISS:\s+(\d+)',
    'l1d_mpki':       r'^L1D LOAD\s+ACCESS:.*MPKI: ([\d.eE+-]+)',
    'accuracy':       r'^L1D USEFUL LOAD PREFETCHES:.*ACCURACY: ([\d.eE+-]+)',
    'pf_issued':      r'^L1D USEFUL LOAD PREFETCHES:.*PREFETCH ISSUED TO LOWER LEVEL:\s+(\d+)',
    'l2c_mpki':       r'^L2C LOAD\s+ACCESS:.*MPKI: ([\d.eE+-]+)',
    'l2c_data_mpki':  r'^L2C DATA LOAD MPKI: ([\d.eE+-]+)',
    'l2c_instr_mpki': r'^L2C INSTRUCTION LOAD MPKI: ([\d.eE+-]+)',
    'l2c_miss_lat':   r'^L2C AVERAGE MISS LATENCY: ([\d.eE+-]+)',
    'llc_load_miss':  r'^LLC LOAD\s+ACCESS:\s+\d+\s+HIT:\s+\d+\s+MISS:\s+(\d+)',
    'irrip_fraction': r'^DYN_IRRIP .*irrip_fraction ([\d.eE+-]+)',
    'l2_pf_fills':    r'^L2C_PF .* fills (\d+)',
    'l2_pf_used':     r'^L2C_PF .*demand_used (\d+)',
    'l2_pf_unused':   r'^L2C_PF .*evicted_unused (\d+)',
    'l2_pf_hits':     r'^L2C_PF .*prefetch_hits (\d+)',
}

COLS = ['ipc', 'speedup', 'accuracy', 'coverage', 'l1d_mpki', 'l2c_mpki', 'l2c_instr_mpki', 'l2c_data_mpki',
        'l1d_load_miss', 'pf_issued', 'l2c_miss_lat', 'llc_load_miss', 'irrip_fraction',
        'l2_pf_fills', 'l2_pf_used', 'l2_pf_unused', 'l2_pf_hits']

def parse(path):
    text = open(path, errors='replace').read()
    row = {}
    for k, p in PATTERNS.items():
        m = re.search(p, text, re.M)
        try:
            row[k] = float(m.group(1)) if m else None
        except ValueError:          # "-nan" accuracy when nothing was prefetched
            row[k] = None
    return row

def geomean(xs):
    xs = [x for x in xs if x and x > 0]
    return math.exp(sum(map(math.log, xs)) / len(xs)) if xs else None

def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None

def fmt(x, d=4):
    return '-' if x is None else f'{x:.{d}f}'

def main():
    res = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'results', 'task3')
    if not os.path.isdir(res):
        sys.exit(f'no results in {res}; run task3/run_task3.sh first')
    skip = ('plots', 'sensitivity', 'design_exploration')
    found = [c for c in os.listdir(res) if c not in skip and os.path.isdir(os.path.join(res, c))]
    configs = [c for c in ORDER if c in found] + sorted(c for c in found if c not in ORDER)
    sdir = os.path.join(res, 'sensitivity')
    sens = sorted('sensitivity/' + c for c in os.listdir(sdir)) if os.path.isdir(sdir) else []
    data = {}
    for c in configs + sens:
        for f in sorted(os.listdir(os.path.join(res, c))):
            if f.endswith('.txt'):
                r = parse(os.path.join(res, c, f))
                if r['ipc'] is None:
                    print(f'warning: {c}/{f} has no final IPC (unfinished run?)', file=sys.stderr)
                    continue
                data[(f[:-4], c)] = r
    traces = sorted({t for t, _ in data})
    for (t, c), r in data.items():
        base = data.get((t, 'baseline'))
        r['speedup'] = r['ipc'] / base['ipc'] if base else None
        # coverage is only meaningful for configurations that prefetch
        if base and r['pf_issued']:
            r['coverage'] = 100.0 * (base['l1d_load_miss'] - r['l1d_load_miss']) / base['l1d_load_miss']
        else:
            r['coverage'] = None
        if not r['pf_issued']:
            r['accuracy'] = None

    with open(os.path.join(res, 'task3_results.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['trace', 'config'] + COLS)
        for t in traces:
            for c in configs + sens:
                if (t, c) in data:
                    w.writerow([t, c] + [data[(t, c)].get(k) for k in COLS])

    metrics = [('ipc', 'IPC', 4), ('speedup', 'Speedup over baseline (no prefetcher, LRU)', 4),
               ('accuracy', 'L1D prefetch accuracy (%)', 2), ('coverage', 'L1D prefetch coverage (%)', 2),
               ('l1d_mpki', 'L1D Load MPKI', 3), ('l2c_mpki', 'L2C Load MPKI', 3),
               ('l2c_instr_mpki', 'L2 Instruction Load MPKI', 3), ('l2c_data_mpki', 'L2 Data Load MPKI', 3),
               ('l2c_miss_lat', 'L2C average miss latency (cycles)', 1)]
    out = ['# Task 3 results', '',
           'Average row: geometric mean for IPC/speedup, arithmetic mean otherwise.', '']
    for key, title, d in metrics:
        out += [f'## {title}', '', '| Trace | ' + ' | '.join(configs) + ' |', '|---|' + '---|' * len(configs)]
        for t in traces:
            out.append(f'| {t} | ' + ' | '.join(fmt(data.get((t, c), {}).get(key), d) for c in configs) + ' |')
        agg = geomean if key in ('ipc', 'speedup') else mean
        out.append('| **Average** | ' + ' | '.join(
            fmt(agg([data[(t, c)][key] for t in traces if (t, c) in data]), d) for c in configs) + ' |')
        out.append('')

    if sens:
        # the final design (spp_pf_dyn) is pf_ins1 and t0.05; list it next to its variations
        groups = [('Prefetch insertion RRPV', 'pf_ins', '1'), ('Leader-set threshold', 't', '0.05')]
        for title, pfx, final in groups:
            rows = [(final + ' (final)', 'spp_pf_dyn')] + [
                (c.split('/')[1][len(pfx):], c) for c in sens if c.split('/')[1].startswith(pfx)
                and re.match(r'[\d.]+$', c.split('/')[1][len(pfx):])]
            rows.sort(key=lambda r: float(r[0].split()[0]))
            out += [f'## Sensitivity: {title} (SPP + prefetch-aware Dynamic I-RRIP)', '',
                    '| Value | ' + ' | '.join(f'Speedup {t}' for t in traces) +
                    ' | Geomean speedup | L2C MPKI | L2 Instr MPKI | L2 Data MPKI |',
                    '|---|' + '---|' * (len(traces) + 4)]
            for lab, c in rows:
                sp = [data.get((t, c), {}).get('speedup') for t in traces]
                out.append(f'| {lab} | ' + ' | '.join(fmt(x) for x in sp) + f' | {fmt(geomean(sp))} | ' +
                           ' | '.join(fmt(mean([data.get((t, c), {}).get(k) for t in traces]), 3)
                                      for k in ('l2c_mpki', 'l2c_instr_mpki', 'l2c_data_mpki')) + ' |')
            out.append('')

    md = os.path.join(res, 'task3_tables.md')
    open(md, 'w').write('\n'.join(out))
    print('\n'.join(out))
    print(f'\nwrote {md} and task3_results.csv')

if __name__ == '__main__':
    main()
