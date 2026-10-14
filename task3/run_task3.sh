#!/bin/bash
# Task 3: SPP (L1D) + prefetch-aware Dynamic I-RRIP (L2C). 25M warmup + 25M simulation.
#
# Build the binaries first (with gcc 7), from the repo root:
#   ./build_champsim.sh no  lru       baseline
#   ./build_champsim.sh no  dyn_irrip dyn_irrip
#   ./build_champsim.sh spp lru       spp
#   ./build_champsim.sh spp dyn_irrip spp_dyn_irrip
#
# Configurations (one directory each under results/task3/):
#   baseline       no prefetcher, LRU
#   dyn_irrip      no prefetcher, Dynamic I-RRIP (Task 2B; no prefetches reach the L2, so the
#                  prefetch-aware code paths are never taken)
#   spp_lru        standalone SPP, LRU
#   spp_dyn_irrip  SPP + Dynamic I-RRIP with prefetch awareness switched off (DYN_IRRIP_PF_AWARE=0)
#   spp_pf_dyn     SPP + prefetch-aware Dynamic I-RRIP (Task 3, final design)
# Sensitivity study of the final design (results/task3/sensitivity/):
#   pf_ins<r>      prefetch fills inserted at RRPV r instead of 1 (r = 0, 2, 3)
#   t<T>           leader-set threshold T instead of 0.05
#
# Usage: task3/run_task3.sh <trace_dir> [parallel_jobs]
# Logs:  results/task3/<config>/<trace>.txt

set -u
TRACE_DIR=${1:?usage: $0 <trace_dir> [parallel_jobs]}
JOBS=${2:-5}
WARMUP=${WARMUP:-25000000}
SIM=${SIM:-25000000}
THRESHOLDS="0.10 0.20 0.35 0.50"      # 0.05 is the final design (spp_pf_dyn)

ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT=$ROOT/results/task3
NOPF=$ROOT/bin/hashed_perceptron-no-no-no-no-no-no-no-lru-lru-lru
SPP=$ROOT/bin/hashed_perceptron-no-spp-no-no-no-no-no-lru-lru-lru

# one line per run: <config> <extra env or -> <binary>
configs() {
    echo "baseline - $NOPF-lru-lru-lru-lru-lru-1core-baseline"
    echo "dyn_irrip - $NOPF-dyn_irrip-lru-lru-lru-lru-1core-dyn_irrip"
    echo "spp_lru - $SPP-lru-lru-lru-lru-lru-1core-spp"
    echo "spp_dyn_irrip DYN_IRRIP_PF_AWARE=0 $SPP-dyn_irrip-lru-lru-lru-lru-1core-spp_dyn_irrip"
    echo "spp_pf_dyn - $SPP-dyn_irrip-lru-lru-lru-lru-1core-spp_dyn_irrip"
    for r in 0 2 3; do
        echo "sensitivity/pf_ins$r DYN_IRRIP_PF_INS=$r $SPP-dyn_irrip-lru-lru-lru-lru-1core-spp_dyn_irrip"
    done
    for t in $THRESHOLDS; do
        echo "sensitivity/t$t DYN_IRRIP_THRESHOLD=$t $SPP-dyn_irrip-lru-lru-lru-lru-1core-spp_dyn_irrip"
    done
}

configs | while read -r _ _ bin; do
    [ -x "$bin" ] || { echo "missing binary: $bin"; exit 1; }
done || exit 1

run_one() {  # config env binary trace
    local cfg=$1 extra=$2 bin=$3 trace=$4
    local name log
    name=$(basename "$trace"); name=${name%%.champsim*}; name=${name%.xz}; name=${name%.gz}
    mkdir -p "$OUT/$cfg"
    log=$OUT/$cfg/$name.txt
    if grep -q "Finished CPU" "$log" 2>/dev/null; then echo "skip $cfg/$name (done)"; return; fi
    echo "run  $cfg/$name"
    [ "$extra" = "-" ] && extra=""
    env $extra "$bin" -warmup_instructions $WARMUP -simulation_instructions $SIM -traces "$trace" > "$log" 2>&1
}
export -f run_one
export OUT WARMUP SIM

shopt -s nullglob
TRACES=("$TRACE_DIR"/*.xz "$TRACE_DIR"/*.gz)
[ ${#TRACES[@]} -gt 0 ] || { echo "no .xz/.gz traces in $TRACE_DIR"; exit 1; }

for tr in "${TRACES[@]}"; do
    configs | while read -r cfg extra bin; do echo "$cfg $extra $bin $tr"; done
done | xargs -P "$JOBS" -L 1 bash -c 'run_one "$@"' _

echo "done. now run: python3 task3/parse_results.py && python3 task3/plot_results.py"
