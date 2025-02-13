"""
proposed model only with the correlation branch.

author: David-Alexandre Beaupre
date: 2020-04-27

Modified by: Philippe Duplessis-Guindon
date: 2022-07-26
"""

import torch
import torch.nn as nn

from models.hrnet.seg_hrnet import get_seg_model
from models.classifier import Classifier


class CorrNet(nn.Module):
    def __init__(self, config):
        """
        represents the architecture of the proposed model with only the correlation branch.
        :param num_channels: number of channels of the input image.
        """
        super(CorrNet, self).__init__()
        self.rgb_features = get_seg_model(config)
        self.lwir_features = get_seg_model(config)
        self.correlation_cls = Classifier(num_channels=331776)

    def forward(self, rgb: torch.Tensor, lwir: torch.Tensor) -> torch.Tensor:
        """
        forward pass implementation of the correlation branch.
        :param rgb: rgb patch tensor.
        :param lwir: lwir patch tensor.
        :return: 2 elements probability tensor (rgb and lwir being the same or not).
        """
        rgb = self.rgb_features(rgb)
        lwir = self.lwir_features(lwir)

        correlation = torch.matmul(rgb, lwir)
        correlation = correlation.view(correlation.size(0), -1)
        correlation = self.correlation_cls(correlation)

        return correlation
