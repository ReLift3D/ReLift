"""The one place that puts third-party code (git submodules under ``third_party/``) on the import path."""
import sys
from pathlib import Path

THIRD_PARTY = Path(__file__).resolve().parents[1] / "third_party"


def _require(path: Path, what: str):
    if not path.exists():
        raise ImportError(f"{what} not found at {path}; run `git submodule update --init --recursive`")


def front_ends():
    """The five front-end code bases on the import path, in the order the research runs used: AllTracker's own
    ``utils`` package must come first.  ``moviepy``, which DA3's export module imports and inference never uses,
    is stubbed when it is not installed."""
    import types
    for sub in ("4RC", "cowtracker", "vggt-omega", "Depth-Anything-3/src", "alltracker"):
        p = THIRD_PARTY / sub
        _require(p, f"the {sub.split('/')[0]} submodule")
        if str(p) in sys.path:
            sys.path.remove(str(p))
        sys.path.insert(0, str(p))
    if "moviepy" not in sys.modules:
        try:
            import moviepy  # noqa: F401
        except ImportError:
            stub, editor = types.ModuleType("moviepy"), types.ModuleType("moviepy.editor")
            stub.editor = editor
            sys.modules["moviepy"], sys.modules["moviepy.editor"] = stub, editor


def rc4_eval():
    """4RC's evaluation modules (alignment, metric, clip loader), imported from the pinned submodule.
    Returns (tapvid3d_utils, track_eval_util) with the RANSAC progress bar silenced."""
    root = THIRD_PARTY / "4RC"
    _require(root / "eval" / "track" / "track_eval_util.py", "the 4RC submodule")
    for p in (str(root), str(root / "eval" / "track")):
        if p not in sys.path:
            sys.path.insert(0, p)
    import tapvid3d_utils as TE  # noqa: E402
    import track_eval_util as U  # noqa: E402
    U.tqdm = lambda x, *a, **k: x
    return TE, U
