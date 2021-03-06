import sys, os
sys.path.append(os.getcwd())
import torch as t
from data.MultiviewCdataset import MultiviewC_dataset
from skimage import transform as sktsf
from torchvision import transforms as tvtsf
from data import util
import numpy as np
from utils.config import opt


def inverse_normalize(img):
    # approximate un-normalize for visualize
    return (img * 0.225 + 0.45).clip(min=0, max=1) * 255


def pytorch_normalze(img):
    """
    https://github.com/pytorch/vision/issues/223
    return appr -1~1 RGB
    """
    normalize = tvtsf.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
    img = normalize(t.from_numpy(img))
    return img.numpy()



def preprocess(img, min_size=600, max_size=1000):
    """Preprocess an image for feature extraction.

    The length of the shorter edge is scaled to :obj:`self.min_size`.
    After the scaling, if the length of the longer edge is longer than
    :param min_size:
    :obj:`self.max_size`, the image is scaled to fit the longer edge
    to :obj:`self.max_size`.

    After resizing the image, the image is subtracted by a mean image value
    :obj:`self.mean`.

    Args:
        img (~numpy.ndarray): An image. This is in CHW and RGB format.
            The range of its value is :math:`[0, 255]`.

    Returns:
        ~numpy.ndarray: A preprocessed image.

    """
    C, H, W = img.shape
    scale1 = min_size / min(H, W)
    scale2 = max_size / max(H, W)
    scale = min(scale1, scale2)
    img = img / 255.
    img = sktsf.resize(img, (C, H * scale, W * scale), mode='reflect',anti_aliasing=False)
    # both the longer and shorter should be less than
    # max_size and min_size
    normalize = pytorch_normalze
    return normalize(img)


class Transform(object):

    def __init__(self, min_size=600, max_size=1000):
        self.min_size = min_size
        self.max_size = max_size

    def __call__(self, in_data):
        img, labels = in_data
        _, H, W = img.shape
        img = preprocess(img, self.min_size, self.max_size)
        _, o_H, o_W = img.shape
        scale = o_H / H
        for i in range(len(labels)):
            bbox_2d = labels[i]['Box_2d'].reshape((1,4))
            labels[i]['Box_2d'] = util.resize_bbox(bbox_2d, (H, W), (o_H, o_W)).reshape((2,2))
        
        return img, labels, scale



class Dataset:
    def __init__(self, opt):
        self.opt = opt
        self.db = MultiviewC_dataset(mode='train')
        self.tsf = Transform(opt.min_size, opt.max_size)

    def __getitem__(self, idx):
        labels, ori_img = self.db.get_example_batch(idx)
        ori_img = np.transpose(ori_img, axes=(2, 0, 1))
        img, labels, scale = self.tsf((ori_img, labels))

        return img.copy(), labels.copy(), scale

    def __len__(self):
        return len(self.db)

