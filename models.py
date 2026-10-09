"""
Ledger — model architecture definitions.
Must match the architecture used in the training notebook exactly, since
we load trained weights into these same class definitions for inference.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class MonotonicMLP(nn.Module):
    """
    Splits input into monotonic and non-monotonic features.

    Monotonic features (income, credit score) are routed through a
    sub-network where every weight, in every layer, is passed through
    softplus() to force it non-negative. Composed with ReLU (itself
    non-decreasing), this guarantees that pathway's contribution to the
    output can only increase as these features increase — end-to-end,
    with no way for a later layer to reverse it.

    Non-monotonic features go through a normal unconstrained MLP. Both
    pathways are summed to form the final logit.
    """

    def __init__(self, in_features, monotonic_mask, hidden1=16, hidden2=8, mono_hidden=8):
        super().__init__()
        self.register_buffer("mask", monotonic_mask.bool())
        n_mono = int(monotonic_mask.sum().item())
        n_other = in_features - n_mono

        self.mono_w1 = nn.Parameter(torch.randn(mono_hidden, n_mono) * 0.1)
        self.mono_b1 = nn.Parameter(torch.zeros(mono_hidden))
        self.mono_w2 = nn.Parameter(torch.randn(1, mono_hidden) * 0.1)
        self.mono_b2 = nn.Parameter(torch.zeros(1))

        self.other_net = nn.Sequential(
            nn.Linear(n_other, hidden1),
            nn.ReLU(),
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Linear(hidden2, 1),
        )

        self.temperature = nn.Parameter(torch.ones(1) * 1.0)

    def forward(self, x, apply_temperature=False):
        x_mono = x[:, self.mask]
        x_other = x[:, ~self.mask]

        h = F.linear(x_mono, F.softplus(self.mono_w1), self.mono_b1)
        h = F.relu(h)
        mono_out = F.linear(h, F.softplus(self.mono_w2), self.mono_b2).squeeze(-1)

        other_out = self.other_net(x_other).squeeze(-1)

        logit = mono_out + other_out
        if apply_temperature:
            logit = logit / self.temperature
        return logit

    def predict_proba(self, x, apply_temperature=True):
        logit = self.forward(x, apply_temperature=apply_temperature)
        return torch.sigmoid(logit)
