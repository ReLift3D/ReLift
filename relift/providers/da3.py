"""Depth Anything 3 (DA3NESTED-GIANT-LARGE-1.1): depth, intrinsics and camera-from-world poses of all frames jointly."""
import numpy as np

from ..vendor import front_ends


class DepthAnything3Provider:
    def __init__(self, weights, device="cuda", process_res=504, process_res_method="upper_bound_resize",
                 ref_view_strategy="saddle_balanced"):
        front_ends()
        from depth_anything_3.api import DepthAnything3
        self.model = DepthAnything3.from_pretrained(weights).to(device)
        self.kw = dict(process_res=process_res, process_res_method=process_res_method, ref_view_strategy=ref_view_strategy)

    def run(self, frames):
        """frames (T,H,W,3) uint8 RGB -> dict(depth (T,h,w) f32, poses (T,4,4) f32, intrinsics (T,3,3) f32,
        images (T,h,w,3) uint8: the frames as DA3 processed them, which the tracker runs on)."""
        pred = self.model.inference(image=[f for f in frames], **self.kw)
        ext = pred.extrinsics.astype(np.float32)
        if ext.shape[1:] == (3, 4):
            ext = np.concatenate([ext, np.tile(np.array([[[0, 0, 0, 1]]], np.float32), (len(ext), 1, 1))], 1)
        return dict(depth=pred.depth.astype(np.float32), poses=ext, intrinsics=pred.intrinsics.astype(np.float32),
                    images=pred.processed_images)
