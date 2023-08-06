import torch
import torch.nn as nn


class DiceLoss(nn.Module):
    """Computes the Dice loss.

    Note that PyTorch optimizers minimize a loss. In this
    case, we would like to maximize the dice loss so we
    return the negated dice loss.
    Args:
        target: a tensor of shape [B, 1, H, W].
        predicted: a tensor of shape [B, C, H, W]. Corresponds to
            the raw output or predicted of the model.
        eps: added to the denominator for numerical stability.
    Returns:
        dice_loss: the Dice loss.
    """

    def __init__(self, args):
        super(DiceLoss, self).__init__()
        self.gpu = args.gpu

        if hasattr(args, 'eps'):
            self.eps = args.eps
        else:
            self.eps = 1e-7

    def forward(self, predicted, target):
        """Compute loss between :attr:`predicted` and :attr:`target`.

        Parameters
        ----------
        predicted : torch.Tensor
            Predicted output tensor from a model.
        target : torch.Tensor
            Ground truth tensor.

        Returns
        -------
        torch.Tensor
            Dice loss computed between :attr:`predicted` and :attr:`target`.

        """
        predicted = predicted.float()
        target = target.long()
        target = target.unsqueeze(1)

        dims = tuple(range(2, len(predicted.shape)))
        intersection = torch.sum(target * predicted, dim=dims)

        target_o = torch.sum(target, dim=dims)
        predicted_o = torch.sum(predicted, dim=dims)

        denominator = target_o + predicted_o

        dice_loss = 1.0 - (2.0 * intersection + self.eps) /\
                          (denominator + self.eps)

        return dice_loss.mean()
