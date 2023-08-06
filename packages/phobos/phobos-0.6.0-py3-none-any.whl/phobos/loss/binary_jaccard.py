import torch
import torch.nn as nn


class BinaryJaccardLoss(nn.Module):
    def __init__(self, args):
        super(BinaryJaccardLoss, self).__init__()
        self.gpu = args.gpu

        if hasattr(args, 'eps'):
            self.eps = args.eps
        else:
            self.eps = 1e-15

        self.nll_loss = nn.BCELoss()
        self.jaccard_weight = args.jaccard_weight
        self._stash_bce_loss = 0
        self._stash_jaccard = 0

    def forward(self, predicted, target):
        predicted = predicted.float()
        target = target.float()

        self._stash_bce_loss = self.nll_loss(predicted, target)
        loss = (1 - self.jaccard_weight) * self._stash_bce_loss

        jaccard_target = (target == 1).float()
        jaccard_output = torch.sigmoid(predicted)

        intersection = (jaccard_output * jaccard_target).sum()
        union = jaccard_output.sum() + jaccard_target.sum()

        jaccard_score = (
            (intersection + self.eps) / (union - intersection + self.eps))
        self._stash_jaccard = jaccard_score
        loss += self.jaccard_weight * (1. - jaccard_score)

        return loss
