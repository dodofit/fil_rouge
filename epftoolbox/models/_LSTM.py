import torch 
import pandas as pd 
<<<<<<< HEAD
import numpy as np
=======
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers, dropout):
        super(LSTM, self).__init__()
        
        self.lstm_1 = nn.LSTM(input_size = input_dim, hidden_size = hidden_dim, num_layers = num_layers, dropout=dropout)
        self.lstm_2 = nn.LSTM(input_size = hidden_dim, hidden_size = hidden_dim, num_layers = num_layers, dropout=dropout)
        self.linear = nn.Linear(input_dim = hidden_dim, output_dim = 1)

    def forward(sel, x):
        pass



>>>>>>> lstm
