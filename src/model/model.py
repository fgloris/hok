import cv2
import numpy as np
import torch, torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

ACTIONS_MOVE = ['left', 'right']
GREEDY = 0.9
LR = 0.1
GAMMA = 0.9
MAX_EPISODES = 13
TIME_STEP = 0.3

device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)



class DQN(nn.Module):

    def __init__(self, w, h, n_actions):
        super(DQN, self).__init__()
        self.w,self.h = w,h
        self.f1 = nn.Linear(128, 128)
        self.f2 = nn.Linear(128, 128)
        self.f3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.f1(x))
        x = F.relu(self.f2(x))
        return self.layer3(x)

