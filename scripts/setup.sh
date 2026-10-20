#!/usr/bin/env bash
# One-shot setup: third-party submodules, the conda environment (environment.yml), an editable install of relift.
#
#     bash scripts/setup.sh [ENV]      ENV: a conda environment name (default: relift) or a directory path
#     conda activate ENV
#
# Rerunning updates an existing environment.  Weights and data are separate steps (README.md).  conda's package
# cache and pip's cache follow CONDA_PKGS_DIRS / PIP_CACHE_DIR if you need them off the home directory.
set -euo pipefail
cd "$(dirname "$0")/.."
# Build and check the environment without the per-user site-packages (~/.local): pip must neither take a dependency
# from there nor touch anything there.  The same variable is stored in the environment itself below.
export PYTHONNOUSERSITE=1
ENV="${1:-relift}"
if [[ "$ENV" == */* ]]; then FLAG=(-p "$ENV"); else FLAG=(-n "$ENV"); fi

echo "== submodules"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git submodule update --init --recursive
fi
for d in Depth-Anything-3 alltracker vggt-omega 4RC cowtracker; do
    [ -e "third_party/$d/README.md" ] || { echo "third_party/$d is empty: clone with --recurse-submodules"; exit 1; }
done

echo "== conda environment $ENV"
if conda run "${FLAG[@]}" python -c "" >/dev/null 2>&1; then
    conda env update "${FLAG[@]}" -f environment.yml --prune
else
    conda env create "${FLAG[@]}" -f environment.yml
fi
conda run "${FLAG[@]}" --no-capture-output pip install -e . --no-deps
conda env config vars set "${FLAG[@]}" PYTHONNOUSERSITE=1

echo "== check"
conda run "${FLAG[@]}" --no-capture-output python -c "import relift, torch; print('relift ok, torch', torch.__version__, 'cuda', torch.cuda.is_available())"
echo "done. Next: conda activate $ENV && python scripts/download_weights.py"
