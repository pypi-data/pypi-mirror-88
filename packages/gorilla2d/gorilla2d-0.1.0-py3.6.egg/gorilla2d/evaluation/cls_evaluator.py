# Copyright (c) Gorilla-Lab. All rights reserved.
import os.path as osp

import torch
import numpy as np

from gorilla.evaluation import DatasetEvaluator
from .metric import (accuracy, accuracy_for_each_class)


class ClsEvaluator(DatasetEvaluator):
    """
    Evaluator of classification task, support instance accuary and class-wise accuracy.
    """

    def __init__(self,
                 logger=None,
                 class_wise=False,
                 num_classes=None):
        r"""
        Args:
            dataset_root (str): Root directory of dataset
            logger
            class_wise (bool): If True, return class-wise accuracy additionally
        """
        self.logger = logger
        if class_wise:
            assert num_classes is not None, "num_classes should be given if class_wise=True"
        self.class_wise = class_wise
        self.num_classes = num_classes
        self.reset()

    def reset(self):
        self._output = None
        self._gt = None

    def process(self, output, gt):
        r"""
        Process a batch of model output
        Args:
            output (torch.Tensor): The output of classifier with shape of [batch_size, num_classes]
            gt (torch.Tensor): The ground truth of images with shape of [batch_size, 1]
        """
        if self._output is None:
            self._output = output.detach().cpu()
            self._gt = gt.cpu()
        else:
            self._output = torch.cat(self._output, output.detach().cpu(), dim=0)
            self._gt = torch.cat(self._gt, gt.cpu(), dim=0)

    def evaluate(self):
        """
        Evaluates standard semantic segmentation metrics (http://cocodataset.org/#stuff-eval):
        * Mean intersection-over-union averaged across classes (mIoU)
        * Frequency Weighted IoU (fwIoU)
        * Mean pixel accuracy averaged across classes (mACC)
        * Pixel Accuracy (pACC)
        """
        acc = accuracy(self._output, self._gt)
        if self.class_wise:
            class_wise_acc = accuracy_for_each_class(self._output, self._gt, self.num_classes)
            return acc, class_wise_acc
        return acc
