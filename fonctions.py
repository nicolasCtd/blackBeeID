import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import csv
from matplotlib.ticker import MultipleLocator
from scipy.stats import pearsonr


def gauss(x, mu, sigma):
    return 1/(np.sqrt(2*np.pi) * sigma) * np.exp(-(x - mu)**2/(2*sigma**2))

def denoise_images(path):
    ech_denoise = list()
    ech_input = list()

    for file in os.listdir(path):
        if '.jpg' in file:
            ech_input.append(int(file.split('.')[0]))

    for file in os.listdir(path + os.sep + "denoise"):
        ech_denoise.append(int(file.split("_")[0]))

    done = np.intersect1d(ech_input, ech_denoise)

    for file in os.listdir(path):
        if '.jpg' in file:
            if int(file.split('.')[0]) not in done:
                print(f"denoising of image {file}...")
                denoise(file, "denoise" + file, save=True)
                print('done')
            

def denoise(path_in, path_out, save=False):
    image = cv2.imread(path_in)
    dst = cv2.fastNlMeansDenoisingColored(image, None, 11, 6, 7, 21)
    verbose = ""
    if save:
        verbose += f"save image {path_out}"
        cv2.imwrite(path_out, dst)
    return dst, verbose


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

            f = plt.figure()
            plt.plot(Xnorm, Ynorm, "-*", label="mesures")
            plt.plot(Xnorm, normal, "-*", label="fit gauss")
            plt.title(f"{espece}. Coeff correlation: {int(coeff*100)/100}")
            # plt.savefig(f"{self.path}debug_coeff_correlation_{espece}.png")
            plt.close()
        
        MELLIFERA = int(coeffs['mellifera'] / somme * 100)
        CAUCASICA = int(coeffs['caucasica'] / somme * 100)
        LIGUSTICA = int(coeffs['ligustica'] / somme * 100)
        CARNICA = int(coeffs['carnica'] / somme * 100)

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

        for espece, m in zip(self.limits.keys(), range(4)):

            plt.figure(m)

            fig = plt.gcf()
            ax = plt.gca()
            fig.set_size_inches((16*0.9, 9*0.9))

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
        
            plt.title(f"Histogramme de l'indice cubital (classification {self.visu})", fontweight='bold', fontsize='xx-large')
            plt.xlabel("Indice", fontsize='x-large', fontweight='light')
            plt.ylabel("Nombre d'abeilles", fontsize='x-large', fontweight='light')
            plt.legend(loc='upper left', fontsize=14)
            plt.grid()
            if save:
                plt.savefig(f"{self.path}{3-m}_histogramme_{self.visu}_{espece}.png")
            if show:
                plt.show()

    
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

def scatter_plot(path, indices=list(), shifts=list(), name_fig="", title="", legends=["BEE ID"]):
    fig, ax = plt.subplots()
    fig.set_size_inches((16*0.5, 9*0.7))

    colors = ["blue", "red", "black"]

    for INDICES, SHIFTS, COL, LEG in zip(indices, shifts, colors, legends):
        plt.plot(INDICES, SHIFTS, "*", color=COL, label=LEG, markersize=10)
        
    plt.ylim([-np.max(np.abs(SHIFTS)), +np.max(np.abs(SHIFTS))])

    # mean = np.mean(indices)
    # std = np.std(indices)
    plt.xlim([1, 3])
    plt.axhline(0, color="darkgrey", linewidth=5, zorder=0)
    plt.axvline(2, color="darkgrey", linewidth=5, zorder=0)
    plt.grid()
    plt.ylabel("Transgression discoïdale (°)", fontweight='bold', fontsize=14)
    plt.xlabel("Indice cubital (-)", fontweight='bold', fontsize=14)
    plt.title(title)
    plt.legend()
    if name_fig != "":
        name_fig = "_" + name_fig
    plt.savefig(f"{path}scatter_plot{name_fig}.png")
    plt.show()

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

def files(directory):
    F = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            F.append(file)
    return F

def check_new_files(Rref, R):
    """Check files that are present in directory 'Rref' but not present in directory 'R' """
    
    files_in_Rref = files(Rref)

    for i in range(len(files_in_Rref)):
        files_in_Rref[i] = int(files_in_Rref[i].replace(".", "_").split("_")[0])

    files_in_R = files(R)

    for i in range(len(files_in_R)):
        files_in_R[i] = int(files_in_R[i].replace(".", "_").split("_")[0])

    UU = [True] * len(files_in_Rref)
    for index, in_Rref in enumerate(files_in_Rref):
        for file in files_in_R:
            if file == in_Rref:
                UU[index] = False

    unique = list()
    present_in_both = list()
    for idx, value in enumerate(UU):
        if value == True:
            unique.append(files_in_Rref[idx])
        else:
            present_in_both.append(files_in_Rref[idx])

    return unique, present_in_both

def read_measures(path_to_results):
    ID = list()
    a = list()
    b = list()
    DS = list()
    indices = list()
    rejected = list()
    fail = list()
    with open(f'{path_to_results}', mode ='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            if line[1] == 'a':
                continue
            elif line[1] == 'FAIL':
                fail.append(int(line[0]))
            elif line[1] == 'REJECTED':
                rejected.append(int(line[0]))
            else:
                ID.append(int(line[0]))
                a.append(float(line[1]))
                b.append(float(line[2]))
                indices.append(float(line[3]))
                DS.append(float(line[5]))
    return ID, a, b, indices, DS, fail, rejected