# Model should have AdaptiveAvgPool2d layer and then Linear Layer
# We will remove the Linear Layer and create a new Linear Layer with num_classes
# Port from pytorch_cnn_trainer https://github.com/oke-aditya/pytorch_cnn_trainer

import torchvision
from quickvision.models import components
import torch.nn as nn

__all__ = ["vision_cnn", "create_vision_cnn"]


class vision_cnn(nn.Module):
    def __init__(self, model_name: str, num_classes: int, pretrained: str = None):
        super().__init__()
        self.num_classes = num_classes
        self.bottom, self.out_channels = components.create_torchvision_backbone(model_name, pretrained)
        self.top = nn.Linear(self.out_channels, self.num_classes)

    def forward(self, x):
        x = self.bottom(x)
        x = self.top(x.view(-1, self.out_channels))
        return x


def create_vision_cnn(model_name: str, num_classes: int,
                      pretrained: str = None,):

    # We do not pass in_channels here since torchvision models is not supported with it.

    """
    Creates CNN model from Torchvision. It replaces the top classification layer with num_classes you need.
    Args:
        model_name (str) : Name of the model. E.g. resnet18
        num_classes (int) : Number of classes for classification.
        pretrained (str) : Pretrained weights dataset "imagenet", etc
    """
    model = vision_cnn(model_name, num_classes, pretrained)
    return model
