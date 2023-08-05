# Copy from https://github.com/thuml/Transfer-Learning-Library
import os
from typing import Optional

from torchvision.datasets.folder import DatasetFolder, IMG_EXTENSIONS, default_loader
from torchvision.datasets.utils import download_and_extract_archive

from gorilla2d.datasets import download_data, check_exits


class OfficeCaltech(DatasetFolder):
    """Office+Caltech Dataset.

    Parameters:
        - **root** (str): Root directory of dataset
        - **task** (str): The task (domain) to create dataset. Choices include ``'A'``: amazon, \
            ``'D'``: dslr, ``'W'``:webcam and ``'C'``: caltech.
        - **download** (bool, optional): If true, downloads the dataset from the internet and puts it \
            in root directory. If dataset is already downloaded, it is not downloaded again.
        - **transform** (callable, optional): A function/transform that  takes in an PIL image and returns a \
            transformed version. E.g, ``transforms.RandomCrop``.
        - **target_transform** (callable, optional): A function/transform that takes in the target and transforms it.

    .. note:: In `root`, there will exist following files after downloading.
        ::
            amazon/
                images/
                    backpack/
                        *.jpg
                        ...
            dslr/
            webcam/
            caltech/
            image_list/
                amazon.txt
                dslr.txt
                webcam.txt
                caltech.txt
    """
    directories = {
        "A": "amazon",
        "D": "dslr",
        "W": "webcam",
        "C": "caltech"
    }
    CLASSES = ['back_pack', 'bike', 'calculator', 'headphones', 'keyboard',
               'laptop_computer', 'monitor', 'mouse', 'mug', 'projector']

    def __init__(self, root: str, task: str, download: Optional[bool] = False, **kwargs):
        # NOTE: 拷贝过来之后暂未经过测试
        if download:
            for dir in self.directories.values():
                if not os.path.exists(os.path.join(root, dir)):
                    download_and_extract_archive(url="https://cloud.tsinghua.edu.cn/f/bc427c57459c4194baf0/?dl=1",
                                                 download_root=os.path.join(root, 'download'),
                                                 filename="officecaltech.tgz", remove_finished=False, extract_root=root)
                    break
        else:
            list(map(lambda dir, _: check_exits(root, dir), self.directories.values()))

        super().__init__(
            os.path.join(root, self.directories[task]), default_loader, extensions=IMG_EXTENSIONS, **kwargs)
        self.classes = OfficeCaltech.classes
        self.class_to_idx = {cls: idx
                             for idx, clss in enumerate(self.classes)
                             for cls in clss}

    @property
    def num_classes(self):
        """Number of classes"""
        return len(self.classes)
