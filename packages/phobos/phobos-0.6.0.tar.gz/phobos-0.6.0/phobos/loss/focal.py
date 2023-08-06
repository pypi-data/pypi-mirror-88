import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class FocalLoss(nn.Module):
    r"""Focal loss from https://arxiv.org/pdf/1708.02002.pdf.

    A factor of :math:`(1-\rho_t)^{\gamma}` is added to the
    standard cross entropy criterion. Setting :math:`\gamma>0`
    reduces the relative loss for well-classified examples
    :math: `(\rho_t > 0.5)`, putting more focus on hard, misclassified
    examples.

    Parameters
    ----------
    args : phobos.grain.grain.Grain
        Arguments passed via the experiment when loss function is called.
        :attr:`args` should contain :attr:`gamma` and :attr:`alpha`.
        :attr:`size_average` is optional.
    Attributes
    ----------
    gamma : float
        Tunable focusing parameter, :math:`\gamma >= 0`.
    alpha : float
        Weighthing factor :math:`\alpha \epsilon [0,1]`.
    size_average : bool
        By default, the losses are averaged over each loss element in the
        batch. Note that for some losses, there are multiple elements per
        sample. If the field :attr:`size_average` is set to ``False``,
        the losses are instead summed for each minibatch. Ignored when reduce
        is ``False``. Default: ``True``

    """

    def __init__(self, args):
        super(FocalLoss, self).__init__()
        self.gamma = args.gamma

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
            Focal loss computed between :attr:`predicted` and :attr:`target`.

        """
        predicted = predicted.float()
        target = target.long()
        target = target.unsqueeze(1)
        p = predicted
        t = target

        if p.dim() > 2:
            p = p.view(p.size(0), p.size(1), -1)
            t = t.view(t.size(0), t.size(1), -1)
        else:
            p = p.unsqueeze(2)
            t = t.unsqueeze(2)

        logpt = F.log_softmax(p, dim=1)

        if target.shape[1] == 1:
            logpt = logpt.gather(1, t.long())
            logpt = torch.squeeze(logpt, dim=1)

        pt = torch.exp(logpt)

        weight = torch.pow(-pt + 1.0, self.gamma)

        if target.shape[1] == 1:
            loss = torch.mean(-weight * logpt, dim=1)
        else:
            loss = torch.mean(-weight * t * logpt, dim=-1)

        return loss.mean()
