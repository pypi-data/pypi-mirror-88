import torch.nn.functional as F

from torch import nn


class Embedding(nn.Module):
    def __init__(self):
        super(Embedding, self).__init__()
        # an affine operation: y = Wx + b
        self.fc = nn.Linear(7 * 7 * 1280, 1280, bias=False)  # 7 * 7 from image dimension

    def forward(self, x):
        x = F.avg_pool2d(x, kernel_size=3, stride=1, padding=1)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc(x), inplace=True)

        return x

    @staticmethod
    def num_flat_features(x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features