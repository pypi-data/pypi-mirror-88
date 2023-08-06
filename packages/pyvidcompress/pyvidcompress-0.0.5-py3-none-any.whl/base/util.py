from base.config import Config
from math import log10, sqrt
from enum import Enum
import numpy as np
import cv2
import os
import sys
import skvideo.io


class Channel(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


def get_channels(tensor, channels):
    if len(channels) == 3:
        return tensor

    red = tensor[:, :, :, 0]
    green = tensor[:, :, :, 1]
    blue = tensor[:, :, :, 2]
    selection = []
    if Channel.RED in channels:
        selection.append(red)

    if Channel.GREEN in channels:
        selection.append(green)

    if Channel.BLUE in channels:
        selection.append(blue)

    return np.stack(selection, axis=3)


def file_to_tensor(file, config: Config):
    channels = config.get(
        "channels", [Channel.RED, Channel.GREEN, Channel.BLUE])
    start_frame = config.get("fstart", 0)
    end_frame = config.get("fend", sys.maxsize)

    vidcap = cv2.VideoCapture(file)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    success, image = vidcap.read()
    count = 0
    frames = []
    while success:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if count >= start_frame and count < end_frame:
            frames.append(image)
        count += 1
        success, image = vidcap.read()

    frames = np.stack(frames, axis=0)
    frames = get_channels(frames, channels).astype(float)
    return frames, fps


def claculate_compression_ratio(original_file, compressed_file):
    original_file_size = float(os.stat(original_file).st_size)
    compressed_file_size = float(os.stat(compressed_file).st_size)
    return original_file_size/compressed_file_size


def calculate_psnr(original_file, compressed_file):
    config = Config()
    original, ofps = file_to_tensor(original_file, config)
    compressed, cfps = file_to_tensor(compressed_file, config)
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 48
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


def write_tensor_to_file(tensr, out_file):
    skvideo.io.vwrite(out_file, tensr.cpu())


def write_numpy_to_file(np_arr, out_file):
    skvideo.io.vwrite(out_file, np_arr)
