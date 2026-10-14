#!/usr/bin/env python3
"""Task 3 plots, from results/task3/task3_results.csv (run parse_results.py first).

Writes one PNG per metric into results/task3/plots/ (ipc, speedup, accuracy, coverage,
l1d_mpki, l2c_mpki, l2c_instr_mpki, l2c_data_mpki): per-trace grouped bars for
every configuration, plus an Average group (geomean for IPC/speedup, mean otherwise),
and sensitivity.png: geomean speedup of the final design against the prefetch
insertion RRPV and against the leader-set threshold, with the other configurations
as reference lines.
Usage: python3 task3/plot_results.py. Needs matplotlib.
"""
import csv, math, os, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, 'results', 'task3')
OUT = os.path.join(RES, 'plots')

SERIES = [('baseline', 'Baseline (no pf, LRU)', '#9a9893'),
          ('dyn_irrip', 'Dynamic I-RRIP (no pf)', '#6250d6'),
          ('spp_lru', 'SPP + LRU', '#eb6834'),
          ('spp_dyn_irrip', 'SPP + Dyn I-RRIP (unaware)', '#e8a33a'),
          ('spp_pf_dyn', 'SPP + PF-aware Dyn I-RRIP', '#1baf7a')]
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e4e3df'

METRICS = [('ipc', 'IPC'), ('speedup', 'Speedup over baseline'),
           ('accuracy', 'L1D prefetch accuracy (%)'), ('coverage', 'L1D prefetch coverage (%)'),
           ('l1d_mpki', 'L1D Load MPKI'), ('l2c_mpki', 'L2C Load MPKI'),
           ('l2c_instr_mpki', 'L2 Instruction Load MPKI'), ('l2c_data_mpki', 'L2 Data Load MPKI')]

def load():
    data = {}
    with open(os.path.join(RES, 'task3_results.csv')) as fh:
        for r in csv.DictReader(fh):
            data[(r['trace'], r['config'])] = {k: (float(v) if v not in ('', 'None') else None)
                                               for k, v in r.items() if k not in ('trace', 'config')}
    return data

def geomean(xs):
    xs = [x for x in xs if x]
    return math.exp(sum(map(math.log, xs)) / len(xs)) if xs else float('nan')

def style(ax, ylabel):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_ylabel(ylabel, color=INK)

def plot(data, traces, key, ylabel):
    # accuracy / coverage only exist for the configurations that prefetch
    series = [s for s in SERIES if any((data.get((t, s[0])) or {}).get(key) is not None for t in traces)]
    labels = traces + ['Average']
    n = len(series)
    width = 0.8 / n
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    allv = []
    for i, (cfg, lab, col) in enumerate(series):
        vals = [(data.get((t, cfg)) or {}).get(key) for t in traces]
        clean = [v for v in vals if v is not None]
        avg = geomean(clean) if key in ('ipc', 'speedup') else (sum(clean) / len(clean) if clean else float('nan'))
        ys = [v if v is not None else float('nan') for v in vals] + [avg]
        allv += [y for y in ys if y == y]
        xs = [j + (i - (n - 1) / 2) * width for j in range(len(labels))]
        ax.bar(xs, ys, width * 0.92, color=col, label=lab, edgecolor='white', linewidth=0.8)
    if key == 'speedup':
        # zoom in around 1.0, otherwise differences of a few percent are invisible
        ax.axhline(1.0, color=INK2, linewidth=1, linestyle='--')
        lo, hi = min(allv + [1]), max(allv + [1])
        pad = max(0.005, (hi - lo) * 0.15)
        ax.set_ylim(lo - pad, hi + pad)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    style(ax, ylabel)
    ax.set_title(f'{ylabel}: SPP + L2C replacement policies', color=INK, fontsize=11, loc='left')
    ax.legend(frameon=False, fontsize=8.5, ncol=3, loc='upper left', bbox_to_anchor=(0, -0.08))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, f'{key}.png'), dpi=200)
    plt.close(fig)

def sensitivity(data, traces):
    gm = lambda c: geomean([(data.get((t, c)) or {}).get('speedup') for t in traces])
    configs = {c for _, c in data}
    panels = [('pf_ins', '1', 'Prefetch fill insertion RRPV'), ('t', '0.05', 'Leader-set threshold')]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, (pfx, final, xlabel) in zip(axes, panels):
        pts = {float(final): gm('spp_pf_dyn')}
        for c in configs:
            m = re.match(rf'sensitivity/{pfx}([\d.]+)$', c)
            if m:
                pts[float(m.group(1))] = gm(c)
        xs = sorted(pts)
        ax.plot(xs, [pts[x] for x in xs], color='#1baf7a', linewidth=2, marker='o', markersize=7,
                markeredgecolor='white', markeredgewidth=1.5, label='SPP + PF-aware Dyn I-RRIP')
        ax.plot([float(final)], [pts[float(final)]], marker='*', markersize=14, color='#1baf7a', linestyle='none')
        for cfg, lab, col in SERIES[1:4]:
            if cfg in configs:
                ax.axhline(gm(cfg), color=col, linewidth=1.3, linestyle='--', label=lab)
        ax.set_xlabel(xlabel, color=INK)
        if pfx == 'pf_ins':
            ax.set_xticks(xs)
        style(ax, 'Geomean speedup over baseline' if ax is axes[0] else '')
    axes[0].set_title('Sensitivity of the final design (star = chosen value)', color=INK, fontsize=11, loc='left')
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=8.5, ncol=4, loc='lower center')
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(os.path.join(OUT, 'sensitivity.png'), dpi=200)
    plt.close(fig)

def main():
    data = load()
    os.makedirs(OUT, exist_ok=True)
    traces = sorted({t for t, _ in data})
    main_data = {k: v for k, v in data.items() if not k[1].startswith('sensitivity/')}
    for key, ylabel in METRICS:
        plot(main_data, traces, key, ylabel)
    if any(c.startswith('sensitivity/') for _, c in data):
        sensitivity(data, traces)
    print(f'plots written to {OUT}')

if __name__ == '__main__':
    main()
