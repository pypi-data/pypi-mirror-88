import torch.nn as nn

from .dice import DiceLoss
from .dice_spline import DiceSplineLoss
from .focal import FocalLoss
from .jaccard import JaccardLoss
from .binary_jaccard import BinaryJaccardLoss
from .spline import SplineLoss
from .tversky import TverskyLoss

__all__ = ['DiceLoss', 'DiceSplineLoss', 'FocalLoss',
           'JaccardLoss', 'SplineLoss', 'TverskyLoss',
           'BinaryLoss']


def get_loss(args):
    """Get loss function based on passed args.

    Parameters
    ----------
    args : args
        Parsed arguments.

    Returns
    -------
    phobos.loss
        Selected loss class object.

    """
    if args.loss == 'dice':
        return DiceLoss(args)

    if args.loss == 'focal':
        return FocalLoss(args)

    if args.loss == 'jaccard':
        return JaccardLoss(args)

    if args.loss == 'tversky':
        return TverskyLoss(args)

    if args.loss == 'spline':
        return SplineLoss(args)

    if args.loss == 'dice_spline':
        return DiceSplineLoss(args)

    if args.loss == 'ce':
        return nn.CrossEntropyLoss()

    if args.loss == 'binary_jaccard':
        return BinaryJaccardLoss(args)
