import torch
import torch.utils.data
from torch import nn
from torch.nn import functional as F


class DVCCA(nn.Module):
    # https: // github.com / pytorch / examples / blob / master / vae / main.py
    def __init__(self, input_size_1, input_size_2, outdim_size=2, mu=0.5, both_encoders=True):
        super(DVCCA, self).__init__()
        self.input_size_1 = input_size_1
        self.input_size_2 = input_size_2
        self.outdim_size = outdim_size
        # First encoding layer
        self.encode_1_1 = nn.Linear(input_size_1, 400)
        # Encode to mean
        self.encode_2_mean_1 = nn.Linear(400, outdim_size)
        # Encode to standard deviation
        self.encode_2_std_1 = nn.Linear(400, outdim_size)
        # First encoding layer
        self.encode_1_2 = nn.Linear(input_size_1, 400)
        # Encode to mean
        self.encode_2_mean_2 = nn.Linear(400, outdim_size)
        # Encode to standard deviation
        self.encode_2_std_2 = nn.Linear(400, outdim_size)
        # Deocde to x1
        self.decode_1_1 = nn.Linear(outdim_size, 400)
        self.decode_2_1 = nn.Linear(400, input_size_1)
        # Deocde to x2
        self.decode_1_2 = nn.Linear(outdim_size, 400)
        self.decode_2_2 = nn.Linear(400, input_size_2)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.both_encoders = both_encoders
        self.mu = mu

    def encode_1(self, x):
        # This takes x and outputs mu (d) and sigma (dxd assumed diagonal to give d)
        h1 = F.relu(self.encode_1_1(x))
        return self.encode_2_mean_1(h1), self.encode_2_std_1(h1)

    def encode_2(self, y):
        # This takes x and outputs mu (d) and sigma (dxd assumed diagonal to give d)
        h1 = F.relu(self.encode_1_2(y))
        return self.encode_2_mean_2(h1), self.encode_2_std_2(h1)

    def reparameterize(self, mu, logvar):
        # Use the standard deviation from the encoder
        std = torch.exp(0.5 * logvar)
        # Mutliply with additive noise (assumed gaussian observation model)
        eps = torch.randn_like(std)
        # Generate random sample
        return mu + eps * std

    def decode_1(self, z):
        h3_1 = F.relu(self.decode_1_1(z))
        return torch.sigmoid(self.decode_2_1(h3_1))

    def decode_2(self, z):
        h3_2 = F.relu(self.decode_1_2(z))
        return torch.sigmoid(self.decode_2_2(h3_2))

    def forward(self, x, y=None):
        mu_x, logvar_x = self.encode_1(x)
        z_x = self.reparameterize(mu_x, logvar_x)
        if self.both_encoders:
            mu_y, logvar_y = self.encode_2(y)
            z_y = self.reparameterize(mu_y, logvar_y)
            return self.decode_1(z_x), self.decode_2(z_y), mu_x, logvar_x, mu_y, logvar_y
        return self.decode_1(z_x), self.decode_2(z_x), mu_x, logvar_x

    def loss(self, x, y, recon_x, recon_y, mu_x, logvar_x, mu_y=None, logvar_y=None):
        # KL bit - we have assumed logvar diagonal
        KL_x = -0.5 * torch.sum(1 + logvar_x - logvar_x.exp() - mu_x.pow(2))

        BCE_1 = F.binary_cross_entropy(recon_x, x, reduction='sum')

        BCE_2 = F.binary_cross_entropy(recon_y, y, reduction='sum')

        if self.both_encoders:
            KL_y = -0.5 * torch.sum(1 + logvar_y - logvar_y.exp() - mu_y.pow(2))
            return self.mu * KL_x + (1 - self.mu) * KL_y + BCE_1 + BCE_2

        return KL_x + BCE_1 + BCE_2


class DVCCA_p(nn.Module):
    # https: // github.com / pytorch / examples / blob / master / vae / main.py
    def __init__(self, input_size_1, input_size_2, outdim_size=2, mu=0.5, both_encoders=True):
        super(DVCCA_p, self).__init__()
        self.input_size_1 = input_size_1
        self.input_size_2 = input_size_2
        self.outdim_size = outdim_size
        # First encoding layer
        self.encode_1_1 = nn.Linear(input_size_1, 400)
        # Encode to mean
        self.encode_2_mean_1 = nn.Linear(400, outdim_size)
        # Encode to standard deviation
        self.encode_2_std_1 = nn.Linear(400, outdim_size)
        # First encoding layer
        self.encode_1_2 = nn.Linear(input_size_1, 400)
        # Encode to mean
        self.encode_2_mean_2 = nn.Linear(400, outdim_size)
        # Encode to standard deviation
        self.encode_2_std_2 = nn.Linear(400, outdim_size)
        # First encoding layer
        self.encode_1_p1 = nn.Linear(input_size_1, 400)
        # Encode to mean
        self.encode_2_mean_p1 = nn.Linear(400, outdim_size)
        # Encode to standard deviation
        self.encode_2_std_p1 = nn.Linear(400, outdim_size)
        # First encoding layer
        self.encode_1_p2 = nn.Linear(input_size_1, 400)
        # Encode to mean
        self.encode_2_mean_p2 = nn.Linear(400, outdim_size)
        # Encode to standard deviation
        self.encode_2_std_p2 = nn.Linear(400, outdim_size)
        # Deocde to x1
        self.decode_1_1 = nn.Linear(outdim_size * 3, 400)
        self.decode_2_1 = nn.Linear(400, input_size_1)
        # Deocde to x2
        self.decode_1_2 = nn.Linear(outdim_size * 3, 400)
        self.decode_2_2 = nn.Linear(400, input_size_2)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.both_encoders = both_encoders
        self.mu = mu

    def encode_1(self, x):
        # This takes x and outputs mu (d) and sigma (dxd assumed diagonal to give d)
        h1 = F.relu(self.encode_1_1(x))
        return self.encode_2_mean_1(h1), self.encode_2_std_1(h1)

    def encode_p1(self, x):
        # This takes x and outputs mu (d) and sigma (dxd assumed diagonal to give d)
        h1 = F.relu(self.encode_1_p1(x))
        return self.encode_2_mean_p1(h1), self.encode_2_std_p1(h1)

    def encode_2(self, y):
        # This takes x and outputs mu (d) and sigma (dxd assumed diagonal to give d)
        h1 = F.relu(self.encode_1_2(y))
        return self.encode_2_mean_2(h1), self.encode_2_std_2(h1)

    def encode_p2(self, y):
        # This takes x and outputs mu (d) and sigma (dxd assumed diagonal to give d)
        h1 = F.relu(self.encode_1_p2(y))
        return self.encode_2_mean_p2(h1), self.encode_2_std_p2(h1)

    def reparameterize(self, mu, logvar):
        # Use the standard deviation from the encoder
        std = torch.exp(0.5 * logvar)
        # Mutliply with additive noise (assumed gaussian observation model)
        eps = torch.randn_like(std)
        # Generate random sample
        return mu + eps * std

    def decode_1(self, z):
        h3_1 = F.relu(self.decode_1_1(z))
        return torch.sigmoid(self.decode_2_1(h3_1))

    def decode_2(self, z):
        h3_2 = F.relu(self.decode_1_2(z))
        return torch.sigmoid(self.decode_2_2(h3_2))

    def forward(self, x, y=None):
        mu_x, logvar_x = self.encode_1(x)
        z_x = self.reparameterize(mu_x, logvar_x)
        mu_px, logvar_px = self.encode_p1(x)
        z_px = self.reparameterize(mu_px, logvar_px)
        mu_py, logvar_py = self.encode_p2(y)
        z_py = self.reparameterize(mu_py, logvar_py)
        z_decode = torch.cat([z_x, z_px, z_py], dim=-1)
        if self.both_encoders:
            mu_y, logvar_y = self.encode_2(y)
            z_y = self.reparameterize(mu_y, logvar_y)
            z_x_decode = torch.cat([z_x, z_px, z_py], dim=-1)
            z_y_decode = torch.cat([z_y, z_px, z_py], dim=-1)
            return self.decode_1(z_y_decode), self.decode_2(
                z_x_decode), mu_x, logvar_x, mu_y, logvar_y, mu_px, logvar_px, mu_py, logvar_py
        return self.decode_1(z_decode), self.decode_2(z_decode), mu_x, logvar_x, mu_px, logvar_px, mu_py, logvar_py

    def loss(self, x, y, recon_x, recon_y, mu_x, logvar_x, mu_px, logvar_px, mu_y=None, logvar_y=None, mu_py=None,
             logvar_py=None):
        # KL bit - we have assumed logvar diagonal
        KL_x = -0.5 * torch.sum(1 + logvar_x - logvar_x.exp() - mu_x.pow(2))

        KL_px = -0.5 * torch.sum(1 + logvar_px - logvar_px.exp() - mu_px.pow(2))

        BCE_1 = F.binary_cross_entropy(recon_x, x, reduction='sum')

        BCE_2 = F.binary_cross_entropy(recon_y, y, reduction='sum')

        if self.both_encoders:
            KL_y = -0.5 * torch.sum(1 + logvar_y - logvar_y.exp() - mu_y.pow(2))
            KL_py = -0.5 * torch.sum(1 + logvar_py - logvar_py.exp() - mu_py.pow(2))
            return self.mu * KL_x + (1 - self.mu) * KL_y + BCE_1 + BCE_2 + KL_px + KL_py

        return KL_x + BCE_1 + BCE_2 + KL_px
