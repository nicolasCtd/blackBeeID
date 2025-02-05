# coding: utf-8

import numpy as np
import os
from fonctions import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings
from datetime import datetime
import yaml

warnings.filterwarnings('ignore') 


class IMAGE():
    def __init__(self):
        self.name = ''
        self.data = np.array([])
        self.nb_lignes = 0
        self.nb_col = 0
        self.c1 = np.array([])  # composante 1 (R)
        self.c2 = np.array([])  # composante 2 (G)
        self.c3 = np.array([])  # composante 3 (B)
        self.ci_points = list()
        self.ds_points = list()
        self.DS_i = 0
        self.DS_j = 0
        self.discoidal_shift = 90
    
    def load(self, file):
        self.name = file
        self.data = np.copy(plt.imread(file))
        self.data_copy = np.copy(self.data)
        self.nb_lignes = self.data.shape[0]
        self.nb_col = self.data.shape[1]
        self.c1 = self.data[:, :, 0]
        self.c2 = self.data[:, :, 1]
        self.c3 = self.data[:, :, 2]

    def highlight(self, node, color, rayon=5):
        y, x = np.meshgrid(np.arange(self.nb_col), np.arange(self.nb_lignes))
        for i in range(3):
            dot_ci = (np.sqrt(np.abs(node.i - x)**2 + np.abs(node.j-y)**2) <= rayon) * 1
            idx_ci_i, idx_ci_j = np.where(dot_ci == 1)
            # Color in blue point that has been identified
            for i, j in zip(idx_ci_i, idx_ci_j):
                self.data[i, j][0] = color[0]
                self.data[i, j][1] = color[1]
                self.data[i, j][2] = color[2]
                # "discard" these pixels
                self.data_copy[i, j][0] = 0
                self.data_copy[i, j][1] = 0
                self.data_copy[i, j][2] = 0
        return 0
    
class POINT():
    def __init__(self):
        self.i = 0
        self.j = 0
        self.color = (0, 0, 255)
    
    def __str__(self) -> str:
        print(f"i : {self.i}")
        print(f"j : {self.j}")