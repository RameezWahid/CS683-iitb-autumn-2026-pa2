# Task 2B results

Speedup = IPC / IPC of LRU baseline (no prefetching). Average row: geometric mean for IPC/speedup, arithmetic mean for MPKI.

## IPC

| Trace | baseline | rrip | irrip | dyn_irrip_t0.05 | dyn_irrip_t0.10 | dyn_irrip_t0.20 | dyn_irrip_t0.35 | dyn_irrip_t0.50 |
|---|---|---|---|---|---|---|---|---|
| trace1 | 0.2322 | 0.2322 | 0.2321 | 0.2346 | 0.2346 | 0.2346 | 0.2338 | 0.2322 |
| trace2 | 0.2513 | 0.2518 | 0.2571 | 0.2601 | 0.2593 | 0.2588 | 0.2584 | 0.2580 |
| trace3 | 0.3819 | 0.3816 | 0.3818 | 0.3840 | 0.3840 | 0.3821 | 0.3821 | 0.3813 |
| **Average** | 0.2814 | 0.2815 | 0.2835 | 0.2861 | 0.2859 | 0.2852 | 0.2848 | 0.2838 |

## Speedup over LRU baseline

| Trace | baseline | rrip | irrip | dyn_irrip_t0.05 | dyn_irrip_t0.10 | dyn_irrip_t0.20 | dyn_irrip_t0.35 | dyn_irrip_t0.50 |
|---|---|---|---|---|---|---|---|---|
| trace1 | 1.0000 | 0.9999 | 0.9994 | 1.0101 | 1.0101 | 1.0099 | 1.0068 | 0.9999 |
| trace2 | 1.0000 | 1.0022 | 1.0231 | 1.0349 | 1.0319 | 1.0297 | 1.0283 | 1.0267 |
| trace3 | 1.0000 | 0.9993 | 0.9999 | 1.0057 | 1.0056 | 1.0006 | 1.0007 | 0.9986 |
| **Average** | 1.0000 | 1.0004 | 1.0074 | 1.0168 | 1.0158 | 1.0133 | 1.0119 | 1.0083 |

## L2C Load MPKI

| Trace | baseline | rrip | irrip | dyn_irrip_t0.05 | dyn_irrip_t0.10 | dyn_irrip_t0.20 | dyn_irrip_t0.35 | dyn_irrip_t0.50 |
|---|---|---|---|---|---|---|---|---|
| trace1 | 17.703 | 17.619 | 17.781 | 19.042 | 19.042 | 19.039 | 19.036 | 17.619 |
| trace2 | 27.560 | 26.012 | 22.292 | 21.379 | 21.428 | 21.510 | 21.698 | 21.966 |
| trace3 | 3.960 | 4.037 | 3.891 | 3.994 | 3.999 | 4.061 | 4.038 | 4.053 |
| **Average** | 16.408 | 15.889 | 14.655 | 14.805 | 14.823 | 14.870 | 14.924 | 14.546 |

## L2 Instruction Load MPKI

| Trace | baseline | rrip | irrip | dyn_irrip_t0.05 | dyn_irrip_t0.10 | dyn_irrip_t0.20 | dyn_irrip_t0.35 | dyn_irrip_t0.50 |
|---|---|---|---|---|---|---|---|---|
| trace1 | 10.368 | 10.563 | 9.871 | 9.072 | 9.072 | 9.072 | 9.175 | 10.563 |
| trace2 | 18.892 | 17.980 | 12.834 | 9.264 | 9.531 | 9.690 | 9.957 | 10.263 |
| trace3 | 1.124 | 1.190 | 0.998 | 0.727 | 0.731 | 0.937 | 0.985 | 1.051 |
| **Average** | 10.128 | 9.911 | 7.901 | 6.354 | 6.445 | 6.566 | 6.705 | 7.292 |

## L2 Data Load MPKI

| Trace | baseline | rrip | irrip | dyn_irrip_t0.05 | dyn_irrip_t0.10 | dyn_irrip_t0.20 | dyn_irrip_t0.35 | dyn_irrip_t0.50 |
|---|---|---|---|---|---|---|---|---|
| trace1 | 7.334 | 7.056 | 7.910 | 9.970 | 9.970 | 9.966 | 9.861 | 7.056 |
| trace2 | 8.668 | 8.032 | 9.458 | 12.115 | 11.896 | 11.820 | 11.741 | 11.703 |
| trace3 | 2.837 | 2.846 | 2.893 | 3.267 | 3.268 | 3.124 | 3.053 | 3.002 |
| **Average** | 6.280 | 5.978 | 6.753 | 8.451 | 8.378 | 8.304 | 8.218 | 7.254 |

## Dynamic I-RRIP mode selection (fraction of epochs in I-RRIP mode / mode switches)

| Trace | dyn_irrip_t0.05 | dyn_irrip_t0.10 | dyn_irrip_t0.20 | dyn_irrip_t0.35 | dyn_irrip_t0.50 |
|---|---|---|---|---|---|
| trace1 | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 | 0.96 / 2 | 0.00 / 0 |
| trace2 | 1.00 / 0 | 0.98 / 2 | 0.96 / 2 | 0.91 / 2 | 0.89 / 2 |
| trace3 | 1.00 / 0 | 1.00 / 0 | 0.50 / 1 | 0.33 / 1 | 0.33 / 1 |
