# Task 3 results

Average row: geometric mean for IPC/speedup, arithmetic mean otherwise.

## IPC

| Trace | baseline | dyn_irrip | spp_lru | spp_dyn_irrip | spp_pf_dyn |
|---|---|---|---|---|---|
| trace1 | 0.2322 | 0.2346 | 0.2343 | 0.2374 | 0.2375 |
| trace2 | 0.2513 | 0.2601 | 0.2529 | 0.2621 | 0.2625 |
| trace3 | 0.3819 | 0.3840 | 0.3880 | 0.3906 | 0.3907 |
| **Average** | 0.2814 | 0.2861 | 0.2843 | 0.2897 | 0.2899 |

## Speedup over baseline (no prefetcher, LRU)

| Trace | baseline | dyn_irrip | spp_lru | spp_dyn_irrip | spp_pf_dyn |
|---|---|---|---|---|---|
| trace1 | 1.0000 | 1.0101 | 1.0087 | 1.0222 | 1.0226 |
| trace2 | 1.0000 | 1.0349 | 1.0065 | 1.0430 | 1.0445 |
| trace3 | 1.0000 | 1.0057 | 1.0160 | 1.0229 | 1.0232 |
| **Average** | 1.0000 | 1.0168 | 1.0104 | 1.0293 | 1.0301 |

## L1D prefetch accuracy (%)

| Trace | baseline | dyn_irrip | spp_lru | spp_dyn_irrip | spp_pf_dyn |
|---|---|---|---|---|---|
| trace1 | - | - | 53.09 | 52.93 | 52.86 |
| trace2 | - | - | 44.98 | 44.40 | 44.50 |
| trace3 | - | - | 37.94 | 37.85 | 37.97 |
| **Average** | - | - | 45.34 | 45.06 | 45.11 |

## L1D prefetch coverage (%)

| Trace | baseline | dyn_irrip | spp_lru | spp_dyn_irrip | spp_pf_dyn |
|---|---|---|---|---|---|
| trace1 | - | - | 9.63 | 9.53 | 9.53 |
| trace2 | - | - | 2.67 | 2.58 | 2.57 |
| trace3 | - | - | 13.85 | 13.76 | 13.78 |
| **Average** | - | - | 8.72 | 8.62 | 8.63 |

## L1D Load MPKI

| Trace | baseline | dyn_irrip | spp_lru | spp_dyn_irrip | spp_pf_dyn |
|---|---|---|---|---|---|
| trace1 | 10.679 | 10.680 | 9.650 | 9.661 | 9.662 |
| trace2 | 13.536 | 13.545 | 13.175 | 13.188 | 13.189 |
| trace3 | 3.403 | 3.404 | 2.932 | 2.935 | 2.934 |
| **Average** | 9.206 | 9.210 | 8.586 | 8.595 | 8.595 |

## L2C Load MPKI

| Trace | baseline | dyn_irrip | spp_lru | spp_dyn_irrip | spp_pf_dyn |
|---|---|---|---|---|---|
| trace1 | 17.703 | 19.042 | 16.825 | 17.873 | 17.878 |
| trace2 | 27.560 | 21.379 | 27.486 | 21.041 | 20.844 |
| trace3 | 3.960 | 3.994 | 3.313 | 3.308 | 3.307 |
| **Average** | 16.408 | 14.805 | 15.875 | 14.074 | 14.010 |

## L2 Instruction Load MPKI

| Trace | baseline | dyn_irrip | spp_lru | spp_dyn_irrip | spp_pf_dyn |
|---|---|---|---|---|---|
| trace1 | 10.368 | 9.072 | 10.392 | 9.043 | 9.044 |
| trace2 | 18.892 | 9.264 | 19.132 | 9.298 | 9.096 |
| trace3 | 1.124 | 0.727 | 1.144 | 0.725 | 0.723 |
| **Average** | 10.128 | 6.354 | 10.222 | 6.356 | 6.288 |

## L2 Data Load MPKI

| Trace | baseline | dyn_irrip | spp_lru | spp_dyn_irrip | spp_pf_dyn |
|---|---|---|---|---|---|
| trace1 | 7.334 | 9.970 | 6.434 | 8.830 | 8.834 |
| trace2 | 8.668 | 12.115 | 8.354 | 11.742 | 11.748 |
| trace3 | 2.837 | 3.267 | 2.169 | 2.583 | 2.585 |
| **Average** | 6.280 | 8.451 | 5.652 | 7.718 | 7.722 |

## L2C average miss latency (cycles)

| Trace | baseline | dyn_irrip | spp_lru | spp_dyn_irrip | spp_pf_dyn |
|---|---|---|---|---|---|
| trace1 | 140.5 | 107.1 | 141.9 | 108.2 | 108.2 |
| trace2 | 88.9 | 82.8 | 89.4 | 83.4 | 83.7 |
| trace3 | 156.9 | 109.3 | 158.3 | 113.1 | 113.1 |
| **Average** | 128.8 | 99.7 | 129.8 | 101.6 | 101.7 |

## Sensitivity: Prefetch insertion RRPV (SPP + prefetch-aware Dynamic I-RRIP)

| Value | Speedup trace1 | Speedup trace2 | Speedup trace3 | Geomean speedup | L2C MPKI | L2 Instr MPKI | L2 Data MPKI |
|---|---|---|---|---|---|---|---|
| 0 | 1.0226 | 1.0442 | 1.0231 | 1.0299 | 14.014 | 6.295 | 7.718 |
| 1 (final) | 1.0226 | 1.0445 | 1.0232 | 1.0301 | 14.010 | 6.288 | 7.722 |
| 2 | 1.0222 | 1.0430 | 1.0229 | 1.0293 | 14.074 | 6.356 | 7.718 |
| 3 | 1.0198 | 1.0430 | 1.0226 | 1.0284 | 14.078 | 6.361 | 7.717 |

## Sensitivity: Leader-set threshold (SPP + prefetch-aware Dynamic I-RRIP)

| Value | Speedup trace1 | Speedup trace2 | Speedup trace3 | Geomean speedup | L2C MPKI | L2 Instr MPKI | L2 Data MPKI |
|---|---|---|---|---|---|---|---|
| 0.05 (final) | 1.0226 | 1.0445 | 1.0232 | 1.0301 | 14.010 | 6.288 | 7.722 |
| 0.10 | 1.0226 | 1.0441 | 1.0227 | 1.0297 | 14.012 | 6.291 | 7.721 |
| 0.20 | 1.0220 | 1.0395 | 1.0211 | 1.0275 | 14.032 | 6.418 | 7.613 |
| 0.35 | 1.0217 | 1.0383 | 1.0169 | 1.0256 | 14.132 | 6.558 | 7.574 |
| 0.50 | 1.0090 | 1.0366 | 1.0146 | 1.0200 | 13.843 | 7.124 | 6.719 |
