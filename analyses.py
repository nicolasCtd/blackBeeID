# coding: utf-8

import numpy as np
import os
from utile import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings
from datetime import datetime
import yaml

warnings.filterwarnings('ignore') 

mpl.use('TkAgg')

dpi = 160
HEIGHT = 1060
WIDTH = 750

class HISTOGRAM():
    def __init__(self, indices, path, visu="RUTTNER"):
        self.path=path
        self.visu = visu
        self.indices = indices
        self.classes = self.get_classes(indices)
        self.limits = {'carnica':[2.3, 3.2],
                       'ligustica':[2, 2.8],
                       'caucasica': [1.7, 2.3],
                       'mellifera':[1.4, 2.1]}
        self.mclc = {'carnica':0,
                       'ligustica':0,
                       'caucasica': 0,
                       'mellifera':0}
        self.save_abacus()

    
    def save_abacus(self):
        classes, indices = self.compute_abacus()
        with open(os.sep.join([self.path, "abacus.txt"]), "w") as f:
            for classe, indice in zip(classes, indices):
                f.write(str(indice) + " " + str(classe) + "\n")
        return 0
        
    def histogram(self):
        y = list()
        x = list()
        for i in range(1, 25):
            y.append(self.classes.count(i))
            x.append(i)
        self.x = x
        self.y = y
        return x, y

    def compute_abacus(self):
        if self.visu == "DREHER":
            delta = 100 / 50
        elif self.visu == "RUTTNER":
            delta = 100 / 60

        CLASSES = list()
        INDICES = list()
        for i in range(-5, 18):
            a = 50 + i * delta 
            b = 50 - i * delta 
            CLASSES.append(6 + i)
            INDICES.append(int(a/b*1000)/1000)

        return CLASSES, INDICES

    def get_classes(self, indices):
        CLASSES, INDICES = self.compute_abacus()
        CL = CLASSES[:-1]
        CI_min = INDICES[:-1]
        CI_max = INDICES[1:]

        classes = list()
        for indice in indices:
            for i in range(len(CL)):
                if (indice >= CI_min[i]) and (indice < CI_max[i]):
                    classes.append(CL[i])
                    break
        return classes

    def MCLC(self):
        X = np.array(self.x)
        Y = np.array(self.y)
        
        E = Y.sum()

        coeffs = dict()
        somme = 0

        for espece in self.limits.keys():

            classes = self.get_classes(self.limits[espece])
            cmin, cmax = classes[0], classes[1]
            select = (X >= cmin) & (X <=cmax)

            Xnorm = X[select]
            Ynorm = Y[select] / Y[select].sum()
            Ynorm[0] = 0
            Ynorm[-1] = 0
            sigma = (cmax - cmin )/6
            mu = (cmax + cmin)/2

            normal = gauss(Xnorm, mu, sigma)
            coeff, _ = pearsonr(normal, Ynorm)
            coeff = coeff * Y[select].sum() / E

            if coeff < 0:
                coeff = 0
            coeffs[espece] = coeff
            somme += coeff

            try:
                COEF = int(coeff*100)/100
            except:
                COEF="NaN"

            f = plt.figure()
            plt.plot(Xnorm, Ynorm, "-*", label="mesures")
            plt.plot(Xnorm, normal, "-*", label="fit gauss")
            plt.title(f"{espece}. Coeff correlation: {COEF}")
            # plt.savefig(f"{self.path}debug_coeff_correlation_{espece}.png")
            plt.close()
        
        try:
            C1 = int(coeffs['mellifera'] / somme * 100)
            C2 = int(coeffs['caucasica'] / somme * 100)
            C3 = int(coeffs['ligustica'] / somme * 100)
            C4 = int(coeffs['carnica'] / somme * 100)
        except:
            C1 = 0
            C2 = 0
            C3 = 0
            C4 = 0

        MELLIFERA = C1
        CAUCASICA = C2
        LIGUSTICA = C3
        CARNICA = C4

        if MELLIFERA>0:
            MELLIFERA+=1
        else:
            if CAUCASICA>0:
                CAUCASICA += 1

        if LIGUSTICA>0:
            LIGUSTICA+=1
        else:
            if CARNICA>0:
                CARNICA += 1

        self.mclc = {'mellifera':min(100, MELLIFERA), 'caucasica':min(100, CAUCASICA), 'ligustica':min(100, LIGUSTICA), 'carnica':min(100, CARNICA)}
        print(self.mclc)

        return 0

    def reset_ticks(self, ax):
        tck_label = list()
        position = list()
        for tick in ax.get_yticklabels():
            
            if "−" in tick.get_text():
                tck_label.append("")
                position.append(tick.get_position()[1])
            else:
                if tick.get_position()[1] == int(tick.get_position()[1]):
                    tck_label.append(tick.get_text())
                    position.append(int(tick.get_position()[1]))

        ax.set_yticks(position, tck_label)
        cl, idx = self.compute_abacus()
        xticks = []
        for i in range(len(idx)):
            xticks.append(str(int(idx[i]*100)/100))
        
        ax.set_xticks(np.arange(1, 24), xticks, fontsize=8)

        ax.xaxis.set_major_locator(MultipleLocator(1))
        # ax.xaxis.set_minor_locator(MultipleLocator(0.5))

        return tck_label, position


    def plot_histogram(self, show=True, save=True):

        x, y = self.histogram()

        self.MCLC()

        mean_of_classes = np.sum((np.array(x)+0.5) * np.array(y)) / np.sum(np.array(y))

        print(f"indice cubital moyen : {int(np.mean(self.indices) * 100)/100}")
        print(f"moyenne des classes : {int(mean_of_classes * 100)/100}")
        print("\n")

        alpha = 0.5
        colors = ['aquamarine', 'khaki', 'silver', 'thistle']

        figures_out = list()

        for espece, m in zip(self.limits.keys(), range(4)):

            plt.figure(m, figsize=(HEIGHT/dpi, WIDTH/dpi), dpi=dpi)

            fig = plt.gcf()
            ax = plt.gca()
            # fig.set_size_inches((16*0.9, 9*0.9))

            plt.plot(np.array(x)+0.5, y, label=f"Mesures {len(self.indices)} abeilles", linewidth=3.5, zorder=5)

            tck_label, positions = self.reset_ticks(ax)
            plt.ylim(0, max(positions))

            for i in range(0, 24):
                ax.axvline(i, color='black', linewidth=0.5, zorder=0)
            
            for classe in np.arange(1, 24):
                plt.text(classe+0.4, 0.15, str(classe), color='black', fontsize=7, fontweight='bold', zorder=30)

            plt.vlines(mean_of_classes+0.5, 0, max(positions), color='black', linewidth=1.5, linestyle="--", zorder=6)

            cmin = int(self.get_classes([self.limits[espece][0]])[0])
            cmax = int(self.get_classes([self.limits[espece][1]])[0])
            xx = range(cmin, cmax +1)
            yy1 = np.zeros(cmax - cmin + 1)
            yy2 = float(plt.gca().get_yticks()[-1])

            plt.fill_between(xx, yy1, yy2, color=colors[m], alpha=alpha, zorder=2)
            plt.text(cmin + (cmax - cmin)/3, max(positions)-1.5, espece + f"\n     {self.mclc[espece]}%", fontsize=12, style='italic', zorder=10)
            plt.text(mean_of_classes+0., 0.8, f'Moyenne indices : {int(np.mean(self.indices) * 100)/100}', 
                     fontstyle='italic', fontweight='bold', fontsize=8, zorder=20)
        
            # plt.title(f"Histogramme de l'indice cubital (classification {self.visu})", fontweight='bold', fontsize='xx-large')
            plt.xlabel("Indice", fontsize='x-large', fontweight='light')
            plt.ylabel("Nombre d'abeilles", fontsize='x-large', fontweight='light')
            plt.legend(loc='upper left', fontsize=14)
            plt.tight_layout()
            plt.grid()
            PATH = f"{self.path}{os.sep}{3-m}_histogramme_{self.visu}_{espece}.png"
            figures_out.append(PATH)
            if save:
                plt.savefig(PATH, dpi=dpi)
            if show:
                plt.show()
            plt.close()
        return figures_out

    
    def add_plot(self, x, y, indices, mclc, show=True, save=True):

        mean_of_classes = np.sum((np.array(x)+0.5) * np.array(y)) / np.sum(np.array(y)) 

        print(f"indice cubital moyen : {int(np.mean(indices) * 100)/100}")
        print(f"moyenne des classes : {int(mean_of_classes * 100)/100}")

        for espece, m in zip(self.limits.keys(), range(4)):
        
            plt.figure(m)

            fig = plt.gcf()
            ax = plt.gca()

            ax.plot(np.array(x)+0.5, y, label=f"Deepwings {len(self.indices)} abeilles", color='red', linewidth=3.5, zorder=3)

            tck_label, positions = self.reset_ticks(ax)
            plt.ylim(0, max(max(positions), max(y)))

            plt.vlines(mean_of_classes+0.5, 0, max(positions), color='red', linewidth=1.5, linestyle="--", zorder=5.5)

            cmin = int(self.get_classes([self.limits[espece][0]])[0])
            cmax = int(self.get_classes([self.limits[espece][1]])[0])

            plt.text(cmin + (cmax - cmin)/3, max(positions)-2, f"\n     {mclc[espece]}%", fontsize=12, style='italic', color='red', zorder=10)
            plt.text(mean_of_classes-0.5, 1.2, f'Moyenne indices : {int(np.mean(indices) * 100)/100}', 
                        fontstyle='italic', fontweight='bold', fontsize=8, color='red', zorder=20)
            plt.legend(loc='upper left', fontsize=14)
        
            if save:
                fig.savefig(f"{self.path}{3-m}_histogramme_{self.visu}_{espece}.png")
            if show:
                fig.show()

def scatter_plot(path, indices=list(), shifts=list(), name_fig="", title=""):
    
    fig, ax = plt.subplots(figsize=(HEIGHT/dpi, WIDTH/dpi), dpi=dpi)
    # fig.set_size_inches((16*0.5, 9*0.7))
#
    # colors = ["blue", "red", "black"]

    # for INDICES, SHIFTS, COL, LEG in zip(indices, shifts, colors, legends):
    #     plt.plot(INDICES, SHIFTS, "*", color=COL, label=LEG, markersize=10)

    indices = np.array(indices)
    shifts = np.array(shifts)

    abeilles_noires = (indices < 2.05) & (shifts < 0)
    autres_abeilles = ~(abeilles_noires)

    plt.plot(indices[abeilles_noires], shifts[abeilles_noires], "*", color="red", markersize=10)
    plt.plot(indices[autres_abeilles], shifts[autres_abeilles], "*", color="blue", markersize=10)

    plt.ylim([-np.max(np.abs(shifts)), +np.max(np.abs(shifts))])

    # mean = np.mean(indices)
    # std = np.std(indices)
    plt.xlim([1, 3])
    plt.axhline(0, color="darkgrey", linewidth=5, zorder=0)
    plt.axvline(2, color="darkgrey", linewidth=5, zorder=0)
    plt.grid()
    plt.ylabel("Transgression discoïdale (°)", fontweight='bold', fontsize=14)
    plt.xlabel("Indice cubital (-)", fontweight='bold', fontsize=14)
    plt.tight_layout()
    # plt.title(title)
    # plt.legend()
    if name_fig != "":
        name_fig = "_" + name_fig
    ds_image = f"{path}{os.sep}scatter_plot{name_fig}.png"
    plt.savefig(ds_image, dpi=dpi)
    # plt.show()
    return ds_image

def write_results(path, a, b, indices, classes, discoidal_shift, ID, fail, reject):
    
    order = np.argsort(np.array(ID))
    ID = np.array(ID)[order]
    indices = np.array(indices)[order]
    discoidal_shift = np.array(discoidal_shift)[order]
    classes = np.array(classes)[order]
    a = np.array(a)[order]
    b = np.array(b)[order]

    with open(f"{path}results.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["num", "a", "b", "indice_cubital", "classe", "discoidal_shift"])
        
        min_ID = np.min(np.concatenate([ID, fail, reject]))
        max_ID = np.max(np.concatenate([ID, fail, reject]))
        
        for num in np.arange(min_ID, max_ID+1):
            if num in ID:
                idx = int(np.where(num == ID)[0])
                line = [ID[idx], int(a[idx]*100)/100, int(b[idx]*100)/100, int(indices[idx]*100)/100, classes[idx], int(discoidal_shift[idx]*100)/100]
            elif num in fail:
                idx = int(np.where(num == fail)[0])
                line = [fail[idx], "FAIL", "FAIL", "FAIL", "FAIL", "FAIL"]
            elif num in reject:
                idx = int(np.where(num == reject)[0])
                line = [reject[idx], "REJECTED", "REJECTED", "REJECTED", "REJECTED", "REJECTED"]
            else:
                continue
            writer.writerow(line)
        f.close()
        return 0


def analyse(indices, shifts, visu="RUTTNER", path_out=""):

    H = HISTOGRAM(indices=indices, visu=visu, path=path_out)

    list_of_ci_images = H.plot_histogram(show=False, save=True)

    ds_image = scatter_plot(path=path_out, indices=[indices], shifts=[shifts])

    # write_results(path=path_out, a=a, b=b, indices=indices, classes=H.classes, discoidal_shift=discoidal_shift, ID=ID, fail=fail, reject=reject)

    return list_of_ci_images, ds_image

if __name__ == '__main__':
    with open('config.yml', 'r') as file:
        data = yaml.safe_load(file)
    