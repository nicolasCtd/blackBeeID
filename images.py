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


    def customize(self, save, show, out=''):
        try:
            self.compute_cubital_index()
        except:
            print("Erreur dans le calcul de l'indice cubital", file=self.log)
        
        try:
            self.compute_discoidal_shift()
        except:
            print("Erreur dans le calcul de l'angle discoidal", file=self.log)

        fig = plt.imshow(self.data[:, self.nb_col//2:])
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        
        if self.a != 0:
            ci = int(self.cubital_index*100)/100
        else:
            ci = "erreur"

        tt = ""
        if self.discoidal_shift != 90:
            ds = int(self.discoidal_shift*100)/100
            if np.sign(ds) == 1:
                tt = "+"
        else:
            ds = "erreur"

        plt.title(f"Abeille #{num}             Indice cubital : {ci}             Angle discoïdal : {tt}{ds}°", color='white', fontweight='bold', fontsize=15)

        if save:
            plt.gcf().set_size_inches(18.5, 10.5)
            plt.gcf().set_facecolor("grey")
            plt.gcf().savefig(f"{out}{os.sep}{num}.png")
            print(f"Image successfully saved: {out}{num}.png", file=self.log)
            
        if show:
            plt.show()

        plt.close()

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