"""Front ends: geometry providers (depth, intrinsics, camera-from-world poses on the working grid) and dense 2-D
trackers.  Each writes one file into a clip's window directory:

    <geometry>_depth_data.npz   depth (T,H,W) f16, poses (T,4,4) f32 camera-from-world, intrinsics (T,3,3) f32
    <tracker>_tracks.npz        tracks_2d (T,H,W,2) f16, visibility (T,H,W) f16, confidence (T,H,W) f16

Depth Anything 3 defines the working grid (H, W) and the frames AllTracker runs on; the other providers are
resampled to that grid, so ``da3`` runs first.
"""
GEOMETRY = ("da3", "vggto", "rc4")
TRACKERS = ("alltracker", "cowtracker")


def depth_file(geometry):
    return f"{geometry}_depth_data.npz"


def tracks_file(tracker):
    return f"{tracker}_tracks.npz"
