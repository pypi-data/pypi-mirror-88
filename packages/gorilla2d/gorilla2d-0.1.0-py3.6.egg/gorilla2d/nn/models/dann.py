# Copyright (c) Gorilla-Lab. All rights reserved.
import numpy as np

import torch
import torch.nn as nn
from torch.autograd import Function
from gorilla.nn import resnet

from  ..modules.dann import Extractor, Class_classifier, Domain_classifier

class DANN(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        if cfg.arch == "resnet18" or cfg.arch == "resnet34":
            feature_dim = 512
        elif cfg.arch == "resnet50":
            feature_dim = 2048
        else:
            raise NotImplementedError(cfg.arch)

        self.G_f = Extractor(cfg)
        self.G_y = Class_classifier(feature_dim, num_classes=cfg.num_classes) # 512 for ResNet18 and 32, 2048 for ResNet50
        self.G_d = Domain_classifier(feature_dim, hidden_size=128)
        self.gamma = cfg.gamma
        self.epochs = cfg.epochs

    def forward(self, source_data, target_data, constant, epoch):
        # compute the output of source domain and target domain
        feature_source = self.G_f(source_data)
        feature_target = self.G_f(target_data)

        # compute the class loss of feature_source
        cate_output_source = self.G_y(feature_source)
        cate_output_target = self.G_y(feature_target)

        # compute the domain loss of feature_source and target_feature
        p = float(epoch) / self.epochs
        constant = 2. / (1. + np.exp(-self.gamma * p)) - 1
        print('constant:', constant)
        domain_output_source = self.G_d(feature_source, constant)
        domain_output_target = self.G_d(feature_target, constant)

        return dict(cate_output_source = cate_output_source,
                    cate_output_target = cate_output_target,
                    domain_output_source = domain_output_source,
                    domain_output_target = domain_output_target)
