import numpy as np

from os import listdir
from PIL import Image
from torch.utils.data import Dataset
from PIL import Image, ImageOps

from boxes_classifier.core.sync_image import resize_with_padding


class BoxesDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, cfg, transform=None):
        """
        Args:
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.cfg = cfg
        self.list_train = list(map(lambda file: f'{self.cfg.ROOT_DIR}/{file}', listdir(self.cfg.ROOT_DIR)))
        self.transform = transform

    def __len__(self):
        return len(listdir(self.cfg.ROOT_DIR))

    def __getitem__(self, idx):
        path = self.list_train[idx]
        name = path.split("/")[-1].split('.')[0]
        sample = Image.open(path).convert("RGB")
        sample = resize_with_padding(sample, self.cfg.SIZE)
        if self.transform:
            sample = self.transform(sample)

        return {"name": name, "id":idx, "sample": sample}
