# Original implementation by https://github.com/sniklaus/pytorch-hed

from __future__ import annotations

from pathlib import Path

import PIL.Image
import torch
import torch.cuda
import numpy as np
from .network import Network


def load_tensor(path: str) -> torch.Tensor:
    img = PIL.Image.open(path)
    array = np.array(img)
    array = array[:, :, ::-1].transpose(2, 0, 1)
    array = array.astype(np.float32) * (1.0 / 255.0)
    array = np.ascontiguousarray(array)
    tensor = torch.FloatTensor(array)
    name = Path(path).stem
    return tensor


def save_tensor(tensor: torch.Tensor, path: str) -> None:
    tensor = tensor.clamp(0.0, 1.0)
    array = tensor.numpy()
    array = array.transpose(1, 2, 0)[:, :, 0] * 255.0
    array = array.astype(np.uint8)
    img = PIL.Image.fromarray(array)
    img.save(path)


def estimate(tensor_in: torch.Tensor) -> torch.Tensor:

    # requires at least pytorch version 1.3.0
    assert(int(str('').join(torch.__version__.split('.')[0:2])) >= 13)
    # make sure to not compute gradients for computational performance
    torch.set_grad_enabled(False)
    # make sure to use cudnn for computational performance
    torch.backends.cudnn.enabled = True

    # Load the network
    net = Network()
    if torch.cuda.is_available():
        net.cuda()
    net.eval()

    width_in = tensor_in.shape[2]
    height_in = tensor_in.shape[1]

    # remember that there is no guarantee for correctness, comment out
    # the following two lines if you acknowledge this and want to continue
    assert(width_in == 480)
    assert(height_in == 320)

    tensor_in = tensor_in.cuda()
    tensor_in = tensor_in.view(1, 3, height_in, width_in)
    tensor_out = net(tensor_in)
    tensor_out = tensor_out[0, :, :, :].cpu()

    return tensor_out


def process_img(input_fn: str, output_fn: str) -> None:
    """Given an image, applies to it HED and 
    writes the output in another image

    Args:
        input_fn (str): Input image filename
        output_fn (str): Output image filename
    """
    tensor_in = load_tensor(input_fn)
    tensor_out = estimate(tensor_in)
    save_tensor(tensor_out, output_fn)
