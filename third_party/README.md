# Front-end licences

ReLift vendors no third-party code: each front end is a git submodule, pinned to the revision the published
numbers were produced with (`.gitmodules`, `configs/weights.yaml`). Each keeps its own licence, and the code
licence and the weight licence are not always the same one.

| Front end | Role | Code | Weights |
|---|---|---|---|
| [AllTracker](https://github.com/aharley/alltracker) | 2-D tracker | MIT | MIT |
| [Depth Anything 3](https://github.com/ByteDance-Seed/Depth-Anything-3) | geometry | Apache-2.0 | **CC BY-NC-4.0** — the `DA3NESTED-GIANT-LARGE-1.1` checkpoint we pin (DA3's small/base/metric models are Apache-2.0) |
| [4RC](https://github.com/Luo-Yihang/4RC) | geometry | S-Lab License 1.0 — **non-commercial** | S-Lab License 1.0 |
| [CoWTracker](https://github.com/facebookresearch/cowtracker) | 2-D tracker | FAIR Noncommercial Research License | CC BY-NC-4.0 |
| [VGGT-Omega](https://github.com/facebookresearch/vggt-omega) | geometry | FAIR Noncommercial Research License | FAIR Noncommercial Research License — **gated** |

AllTracker is the only front end that is permissive end to end: every geometry model we use ships non-commercial
weights, so the default demo path (Depth Anything 3 + AllTracker) is non-commercial too. Commercial use needs to
be cleared with the respective authors.

Code licences are each repository's `LICENSE`; weight licences are the Hugging Face model cards of the exact
checkpoints `configs/weights.yaml` pins. Checked 2026-10-26.
