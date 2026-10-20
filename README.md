# ReLift: Dense 3D Tracking as Trajectory Repair

ReLift turns a dense 2-D point tracker and a video geometry model into 3-D trajectories of every pixel: the tracked
pixels are lifted along their camera rays at the predicted depth, and a small transformer, the corrector, repairs
and completes the lifted trajectories. One released checkpoint serves every tracker / geometry combination.

## Setup

```
git clone --recurse-submodules https://github.com/MarounKhriesh/ReLift.git
cd ReLift
bash scripts/setup.sh                  # conda environment "relift" + the five front ends (submodules)
conda activate relift
python scripts/download_weights.py     # all weights into checkpoints/, md5-checked
```

Requires Linux, conda and a CUDA GPU (24 GB; CoWTracker needs 48 GB). VGGT-Omega's weights are **gated** on
Hugging Face: request access on https://huggingface.co/facebook/VGGT-Omega, then `huggingface-cli login` (or set
`HF_TOKEN`) and rerun the download. VGGT-Omega, CoWTracker and 4RC are released under non-commercial licences.

## Demo

```
python scripts/demo_video.py assets/demo/kangaroo.mp4        # any video file or directory of frames
```

Runs Depth Anything 3 and AllTracker on the first 84 frames, lifts every pixel of frame 0 and corrects it. Writes
`outputs/demo/kangaroo/tracks.npz` (`xyz` (T,H,W,3): the 3-D trajectory of every pixel in the frame-0 camera's
coordinates, plus the raw lift, the observation mask and the cameras) and `tracks.mp4` (raw lift left, ReLift
right). `--geometry vggto` uses VGGT-Omega instead of Depth Anything 3.

## Training

Data: the annotation files of the official PointOdyssey training split
(`train.tar.gz`, from which only `<scene>/anno.npz` is needed), extracted to `data/pointodyssey/train/<scene>/anno.npz`.

```
python scripts/prepare_pointodyssey.py --stream 0 &     # training windows -> cache/pointodyssey_windows
python scripts/prepare_pointodyssey.py --stream 1 &     # (CPU; the three streams run in parallel)
python scripts/prepare_pointodyssey.py --stream 2 &
python scripts/train.py --run my_run                    # the released recipe -> outputs/runs/my_run/
python scripts/export_checkpoint.py outputs/runs/my_run/final.pt checkpoints/my_run.pt
```

## Evaluation

Data: the 200 WorldTrack clips (ADT, Panoptic Studio, PointOdyssey, Dynamic Replica; 50 each), downloaded and
md5-checked by the first command. Then the front ends, the corrector and the scorer; the last command prints the
results table (APD3D, the layout of Table 1 of the paper).

```
python scripts/download_worldtrack.py                                                 # -> data/worldtrack/
python scripts/prepare_worldtrack.py --geometry da3 vggto rc4 --tracker alltracker
python scripts/prepare_worldtrack.py --geometry --tracker cowtracker                  # own invocation (needs 48 GB)
python scripts/run_corrector.py [--checkpoint checkpoints/my_run.pt]                  # the six tracker / geometry rows
python scripts/score.py --variants alltracker_da3 alltracker_vggto alltracker_rc4 cowtracker_da3 cowtracker_vggto cowtracker_rc4
python scripts/make_table1.py
```

Every GPU script takes `--shard i --nshards n` and skips finished clips.

## Licence and citation

Our code is MIT (`LICENSE`); the front ends under `third_party/` keep their own licences.

Citation: TBD (the arXiv entry will be added when the paper is online). Authors: Assaf Singer, Maroun Khriesh,
Noam Rotstein, Yoni Kasten, Or Litany.
