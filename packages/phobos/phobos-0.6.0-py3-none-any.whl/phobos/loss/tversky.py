import torch
import torch.nn as nn
import torch.nn.functional as F


class TverskyLoss(nn.Module):
    """Computes the Tversky loss [1].
    Args:
        target: a tensor of shape [B, H, W] or [B, 1, H, W].
        predicted: a tensor of shape [B, C, H, W]. Corresponds to
            the raw output or predicted of the model.
        alpha: controls the penalty for false positives.
        beta: controls the penalty for false negatives.
        eps: added to the denominator for numerical stability.
    Returns:
        tversky_loss: the Tversky loss.
    Notes:
        alpha = beta = 0.5 => dice coeff
        alpha = beta = 1 => tanimoto coeff
        alpha + beta = 1 => F beta coeff
    References:
        [1]: https://arxiv.org/abs/1706.05721
    """
    def __init__(self, args):
        super(TverskyLoss, self).__init__()
        self.alpha = args.alpha
        self.beta = args.beta
        self.gpu = args.gpu

        if hasattr(args, 'eps'):
            self.eps = args.eps
        else:
            self.eps = 1e-7

        if hasattr(args, 'size_average'):
            self.size_average = args.size_average
        else:
            self.size_average = True

    def forward(self, predicted, target):
        predicted = predicted.float()
        target = target.float()
        target = target.unsqueeze(1)

        neg_predicted = 1 - predicted
        neg_target = 1 - target

        dims = tuple(range(2, len(predicted.shape)))

        tps = torch.sum(predicted * target, dims)
        fps = self.alpha * torch.sum(predicted * neg_target, dims)
        fns = self.beta * torch.sum(neg_predicted * target, dims)

        numerator = tps + self.eps
        denominator = tps + fps + fns + self.eps

        tversky_loss = 1 - (numerator / denominator)

        return tversky_loss.mean()
