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
        super(Extractor, self).__init__()
        self.model = resnet(args)

    def forward(self, x):
        output = self.model(x)

        return output


class Class_classifier(nn.Module):

    def __init__(self, in_feature, num_classes=31):
        super(Class_classifier, self).__init__()
        self.model = nn.Sequential(
                nn.Linear(in_feature, num_classes)
            )
    def forward(self, x):
        output = self.model(x)

        return output


class Domain_classifier(nn.Module):

    def __init__(self, in_feature, hidden_size=128, mode='standard'):
        super(Domain_classifier, self).__init__()
        if mode == 'standard':
            self.model = nn.Sequential(
                    nn.Dropout(0.5),
                    nn.Linear(in_feature, hidden_size),
                    nn.ReLU(),
                    nn.Dropout(0.5),
                    nn.Linear(hidden_size, hidden_size),
                    nn.ReLU(),
                    nn.Dropout(0.5),            
                    nn.Linear(hidden_size, 2)
                )

    def forward(self, input, constant):
        input = GradReverse.grad_reverse(input, constant)
        output = self.model(input)

        return output
