# Copyright (c) Gorilla-Lab. All rights reserved.
import os.path as osp
from PIL import Image

import torch
import torchvision.transforms as transforms

from gorilla2d import datasets
from gorilla2d.datasets import ResizeImage

def default_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        img_PIL = img.convert('RGB')

    return img_PIL


def _select_image_process(DATA_TRANSFORM_TYPE="simple"):
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225
                                          ])  # the mean and std of ImageNet

    if DATA_TRANSFORM_TYPE == "old":
        transform_train = transforms.Compose([
            transforms.Resize(256),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
        ])
    elif DATA_TRANSFORM_TYPE == "simple":
        transform_train = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize,
        ])
    elif DATA_TRANSFORM_TYPE == "long":
        transform_train = transforms.Compose([
            ResizeImage(256),
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            normalize
        ])
    else:
        raise NotImplementedError("DATA_TRANSFORM_TYPE: {}".format(DATA_TRANSFORM_TYPE))

    transform_test = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        normalize,
    ])

    return transform_train, transform_test


def build_dataloaders(cfg):
    r"""Build dataloaders of source and target domain for training and testing."""
    Dataset = datasets.__dict__[cfg.dataset]
    transform_train, transform_test = _select_image_process(cfg.transform_type)

    train_dataset_source = Dataset(root=osp.join(cfg.data_root, cfg.dataset),
                                   task=cfg.source,
                                   download=False,
                                   transform=transform_train)
    # at torch version above 1.0.0, it will cause many warnings like:
    # OMP: Warning #190: Forking a process while a parallel region is active is potentially unsafe.
    # when pin_memory=True, so it is turned to False
    train_loader_source = torch.utils.data.DataLoader(
        train_dataset_source,
        batch_size=cfg.samples_per_gpu,
        shuffle=True,
        num_workers=cfg.workers_per_gpu,
        pin_memory=False,
        sampler=None,
        drop_last=True)

    train_dataset_target = Dataset(root=osp.join(cfg.data_root, cfg.dataset),
                                   task=cfg.target,
                                   download=False,
                                   transform=transform_train)
    train_loader_target = torch.utils.data.DataLoader(
        train_dataset_target,
        batch_size=cfg.samples_per_gpu,
        shuffle=True,
        num_workers=cfg.workers_per_gpu,
        pin_memory=False,
        sampler=None,
        drop_last=True)

    test_dataset_target = Dataset(root=osp.join(cfg.data_root, cfg.dataset),
                                   task=cfg.target,
                                   download=False,
                                   transform=transform_test)
    test_loader_target = torch.utils.data.DataLoader(
        test_dataset_target,
        batch_size=cfg.samples_per_gpu,
        shuffle=False,
        num_workers=cfg.workers_per_gpu,
        pin_memory=False,
        sampler=None)

    return {
        "train_src": train_loader_source,
        "train_tgt": train_loader_target,
        "test_tgt": test_loader_target,
    }
