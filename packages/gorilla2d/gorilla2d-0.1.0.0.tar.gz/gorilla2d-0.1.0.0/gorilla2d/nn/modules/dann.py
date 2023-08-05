# Copyright (c) Gorilla-Lab. All rights reserved.
import numpy as np

import torch
import torch.nn as nn
from torch.autograd import Function
from gorilla.nn import resnet


class GradReverse(torch.autograd.Function):
    """
    Extension of grad reverse layer
    """
    @staticmethod
    def forward(ctx, x, constant):
        ctx.constant = constant
        return x.view_as(x)

    @staticmethod
    def backward(ctx, grad_output):
        grad_output = grad_output.neg() * ctx.constant
        return grad_output, None

    @staticmethod
    def grad_reverse(x, constant):
        return GradReverse.apply(x, constant)


class Extractor(nn.Module):

    def __init__(self, args, **kwargs):
        super().__init__()
        self.model = resnet(args)

    def forward(self, x):
        output = self.model(x)

        return output


class Class_classifier(nn.Module):

    def __init__(self, in_feature, num_classes=31):
        super().__init__()
        self.model = nn.Sequential(
                nn.Linear(in_feature, num_classes)
            )
    def forward(self, x):
        output = self.model(x)

        return output


class Domain_classifier(nn.Module):

    def __init__(self, in_feature, hidden_size=128):
        super().__init__()
        self.model = nn.Sequential(
                nn.Linear(in_feature, hidden_size),
                nn.BatchNorm1d(hidden_size),
                nn.ReLU(),
                nn.Linear(hidden_size, hidden_size),
                nn.BatchNorm1d(hidden_size),
                nn.ReLU(),
                nn.Linear(hidden_size, 1),
                nn.Sigmoid(),
            )

    def forward(self, x, constant):
        x = GradReverse.grad_reverse(x, constant)
        output = self.model(x)

        return output


class Bottleneck(nn.Module):
    def __init__(self, in_feature, bottleneck_dim=256):
        super().__init__()
        self.bottleneck = nn.Sequential(
            nn.Linear(in_feature, bottleneck_dim),
            nn.BatchNorm1d(bottleneck_dim),
            nn.ReLU()
        )

    def forward(self, x):

        return self.bottleneck(x)
