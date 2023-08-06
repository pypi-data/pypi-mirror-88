import torch.utils.data
from torch import nn
from torch.nn import functional as F
from CCA_methods.cca_loss import *

class DCCAE(nn.Module):
    def __init__(self, input_size_1, input_size_2, outdim_size=2, use_all_singular_values=True, lam=0):
        super(DCCAE, self).__init__()
        self.input_size_1 = input_size_1
        self.input_size_2 = input_size_2
        self.outdim_size = outdim_size
        # First encoding layer
        self.encode_l1_1 = nn.Linear(input_size_1, 256)
        # First encoding layer
        self.encode_l2_1 = nn.Linear(256, 256)
        # Encode to mean
        self.encode_l3_1 = nn.Linear(256, outdim_size)
        # First encoding layer
        self.encode_l1_2 = nn.Linear(input_size_1, 256)
        # Encode to mean
        self.encode_l2_2 = nn.Linear(256, 256)
        # Encode to mean
        self.encode_l3_2 = nn.Linear(256, outdim_size)
        # Deocde to x1
        self.decode_l1_1 = nn.Linear(outdim_size, 400)
        self.decode_l2_1 = nn.Linear(400, input_size_1)
        # Deocde to x2
        self.decode_l1_2 = nn.Linear(outdim_size, 400)
        self.decode_l2_2 = nn.Linear(400, input_size_2)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.use_all_singular_values = use_all_singular_values
        self.cca_objective = cca_loss(self.outdim_size, self.use_all_singular_values, self.device)
        self.lam = lam

    def encode_1(self, x):
        # This takes x and outputs mu (d) and sigma (dxd assumed diagonal to give d)
        h1 = F.relu(self.encode_l1_1(x))
        h1 = F.relu(self.encode_l2_1(h1))
        return self.encode_l3_1(h1)

    def encode_2(self, y):
        # This takes x and outputs mu (d) and sigma (dxd assumed diagonal to give d)
        h1 = F.relu(self.encode_l1_2(y))
        h1 = F.relu(self.encode_l2_2(h1))
        return self.encode_l3_2(h1)

    def decode_1(self, z):
        h3_1 = F.relu(self.decode_l1_1(z))
        return torch.sigmoid(self.decode_l2_1(h3_1))

    def decode_2(self, z):
        h3_2 = F.relu(self.decode_l1_2(z))
        return torch.sigmoid(self.decode_l2_2(h3_2))

    def forward(self, x, y):
        z_x = self.encode_1(x)
        z_y = self.encode_2(y)
        x_recon = self.decode_1(z_x)
        y_recon = self.decode_2(z_y)
        return z_x, z_y, x_recon, y_recon

    def loss(self, x, y, z_x, z_y, recon_x, recon_y):
        recon_1 = F.binary_cross_entropy(recon_x, x, reduction='sum')
        recon_2 = F.binary_cross_entropy(recon_y, y, reduction='sum')

        return self.lam * recon_1 + self.lam * recon_2 + self.cca_objective.loss(z_x, z_y)