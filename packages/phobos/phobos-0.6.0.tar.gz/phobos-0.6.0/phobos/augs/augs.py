import numpy as np
from scipy import ndimage as ndi

from albumentations.augmentations import functional as F
from albumentations.core.transforms_interface import DualTransform, \
    to_tuple


__all__ = ['Rotate']


class Rotate(DualTransform):
    """Array rotation using scipy.ndimage's implementation."""

    def __init__(self, limit=90, border_mode='reflect', cval=0.0,
                 always_apply=False, p=0.5):
        super(Rotate, self).__init__(always_apply, p)

        self.limit = to_tuple(limit)
        self.border_mode = border_mode
        self.cval = cval

    def apply(self, im_arr, angle=0, border_mode='reflect', cval=0, **params):
        return ndi.interpolation.rotate(im_arr, angle=angle,
                                        mode=self.border_mode, cval=self.cval)

    def get_params(self):
        return {'angle': np.random.randint(self.limit[0], self.limit[1])}

    def apply_to_bbox(self, bbox, angle=0, **params):
        return F.bbox_rotate(bbox, angle, **params)

    def apply_to_keypoint(self):
        raise NotImplementedError
