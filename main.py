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

mpl.use('TkAgg')

class IMAGE():
    def __init__(self, log):
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
        self.log = log
    
    def load(self, file):
        self.name = file
        self.data = np.copy(plt.imread(file))
        self.data_copy = np.copy(self.data)
        self.nb_lignes = self.data.shape[0]
        self.nb_col = self.data.shape[1]
        self.c1 = self.data[:, :, 0]
        self.c2 = self.data[:, :, 1]
        self.c3 = self.data[:, :, 2]

    def show(self):
        plt.imshow(image.data)
        plt.show()

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


    def highlight_ci_points(self):
        """Find the 3 cubital index points (in orange) and paint them in blue on final image"""
        nodes = list()
        for i in range(3):
            t1 = self.data_copy[:,:,0]
            t2 = self.data_copy[:,:,1]
            t3 = self.data_copy[:,:,2]
            node = POINT()
            coloured_pixels = np.where((t1 > 250) & (t2 > 100) & (t3 < 10))    # orange pixels (t1 is strong)
            idx_max = int(np.argmax(t1[coloured_pixels]))
            node.i = coloured_pixels[0][idx_max]
            node.j = coloured_pixels[1][idx_max]
            self.highlight(node, color=(0, 0, 255))
            nodes.append(node)
        # sort the 3 points from left to right 
        order = np.array(np.argsort(np.array([nodes[0].j, nodes[1].j, nodes[2].j])), dtype=int)
        for i in range(3):
            self.ci_points.append(nodes[order[i]])
        return 0
    
    def draw_ci_lines(self):
        # draw lines between cubital index points
        DROITE(self.ci_points[0], self.ci_points[1]).draw(self, 2, 2, color=(0, 0, 255))
        DROITE(self.ci_points[1], self.ci_points[2]).draw(self, 2, 2, color=(0, 0, 255))
        return 0

    def highlight_ds_points(self):
        """Find the 4 discoidal shift points (in green) and paint them in yellow on final image"""
        nodes = list()
        pos_y = list()
        for i in range(4):
            t1 = self.data_copy[:,:,0]
            t2 = self.data_copy[:,:,1]
            t3 = self.data_copy[:,:,2]
            node = POINT()
            coloured_pixels = np.where((t1 < 100) & (t2 > 250) & (t3 < 50))    # green pixels (t2 is strong)
            idx_max = int(np.argmax(t1[coloured_pixels]))
            node.i = coloured_pixels[0][idx_max]
            node.j = coloured_pixels[1][idx_max]
            pos_y.append(node.i)
            node.color = (255, 255, 0)
            self.highlight(node, color=(255, 255, 0))
            nodes.append(node)
        idx = np.argmax(pos_y)
        self.DS = nodes[idx]
        nodes.remove(nodes[idx])
        # sort the 3 points from left to right 
        order = np.array(np.argsort(np.array([nodes[0].j, nodes[1].j, nodes[2].j])), dtype=int)
        for i in range(3):
            self.ds_points.append(nodes[order[i]])
        return 0

    def draw_ds_line_02(self):
        DROITE(self.ds_points[0], self.ds_points[2]).draw(self, 2, 2, color=(0, 0, 0))
        return 0

    def draw_ds_line_02_perpendicular(self):
        point1 = POINT()
        point2 = POINT()
        x, y = DROITE(self.ds_points[0], self.ds_points[2]).xy
        dot_product = np.ones(x.size)
        for pixel in range(x.size):
            u = (self.ds_points[2].j - self.ds_points[0].j, self.ds_points[2].i - self.ds_points[0].i)
            v = (x[pixel] - self.ds_points[1].j, y[pixel] - self.ds_points[1].i)
            dot_product[pixel] = u[0] * v[0] + u[1] * v[1]
        idx = int(np.argmin(np.abs(dot_product)))
        Pyy, Pxx = y[idx], x[idx]

        # look for another pixel (point1) in this area that minimizes the dot product
        square = 20
        dot_product = np.ones((self.nb_lignes, self.nb_col)) * 1000
        for dY in np.arange(0, int(1.5*square)):
            for dX in np.arange(-square, +square+1):
                Py_test, Px_test = Pyy - dY, Pxx - dX
                u = (self.ds_points[2].j - self.ds_points[0].j, self.ds_points[2].i - self.ds_points[0].i)
                v = (Px_test - self.ds_points[1].j, Py_test - self.ds_points[1].i)
                dot_product[Py_test, Px_test] = u[0] * v[0] + u[1] * v[1]
        Py, Px = np.where(np.abs(dot_product) == np.min(np.abs(dot_product)))


        if len(Py)>1:
            txt = "draw_ds_line_02_perpendicular(): la recherche + précise d'un autre pixel "
            txt += "appartenant à la droite perpendiculaire à la première n'a pas marché"
            print(txt, file=self.log)
            Py, Px = Pyy, Pxx

        point1.i = Py
        point1.j = Px
        point1.color = self.ds_points[0].color
        # Now find another point far from the second DS point but in the same alignment
        distance_ref = 0.8 * DROITE(self.ds_points[0], self.ds_points[2]).distance
        small_line = DROITE(point1, self.ds_points[1])
        x = np.arange(self.nb_col)
        y = small_line.get_y(x)
        x = x[y>0]
        y = y[y>0]
        distance = np.sqrt((x - point1.j) **2 + (y - point1.i) ** 2)
        delta = np.abs(distance - distance_ref)
        idx = int(np.where(delta == np.min(delta))[0][0])
        point2.i = int(y[idx])
        point2.j = int(x[idx])
        DROITE(point1, point2).draw(self, 2, 5, color=(0, 0, 0))
        self.point1 = point1
        self.point2 = point2
        return 0
    
    def draw_ds_line_02_angle(self):
        P = POINT()
        X1, Y1 = DROITE(self.point1, self.point2).xy
        X2, Y2 = DROITE(self.ds_points[0], self.ds_points[2]).xy
        x = list()
        y = list()
        d = list()
        for x1, y1 in zip(X1, Y1):
            for x2, y2 in zip(X2, Y2):
                d.append((x1 - x2) ** 2 + (y1 - y2)**2)
                x.append(x1)
                y.append(y1)
        P.j, P.i = x[np.argmin(d)], y[np.argmin(d)]
        P.color = self.DS.color
        # Find a point with more distance
        D = DROITE(P, self.DS)
        y = D.get_x(self.point2.i - 10)
        Q = POINT()
        Q.i = self.point2.i - 10
        Q.j = y
        DROITE(P, Q).draw(self, 2, 4, color=(0, 0, 0))
        return 0

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

    def compute_cubital_index(self):
        n0 = self.ci_points[0]
        n1 = self.ci_points[1]
        n2 = self.ci_points[2]
        a = DROITE(n0, n1).distance
        b = DROITE(n1, n2).distance
        self.cubital_index = a/b
        self.a = a
        self.b = b
        return a/b
    
    def compute_discoidal_shift(self):
        U = DROITE(self.point1, self.point2)
        V = DROITE(self.ds_points[1], self.DS)
        dot = U.nX * V.nX + U.nY * V.nY
        delta = self.DS.j - U.get_x(self.DS.i)
        self.discoidal_shift = np.sign(delta) *  np.arccos(dot/(U.distance * V.distance)) * 180/np.pi

    def fill_image(self):
        try:
            self.highlight_ci_points()
            self.draw_ci_lines()
        except:
            print("Pas réussi à trouver les points Ci", file=self.log)
        # self.show()
        try:
            self.highlight_ds_points()
        except:
            print("Pas réussi à trouver les points Ds", file=self.log)
        
        try:
            self.draw_ds_line_02()
            self.draw_ds_line_02_perpendicular()
            # self.draw_ds_line_02_angle()
        except:
            print("Pas réussi à tracer les droites Ds", file=self.log)

class POINT():
    def __init__(self):
        self.i = 0
        self.j = 0
        self.color = (0, 0, 255)
    
    def __str__(self) -> str:
        print(f"i : {self.i}")
        print(f"j : {self.j}")

class DROITE(IMAGE):
    def __init__(self, P1, P2):
        self.coefficients(P1, P2)
        self.coords_xy(P1, P2)
        self.color = P1.color
        self.distance(P1, P2)
        self.vect(P1, P2)
    
    def __str__(self) -> str:
        print(f"a : {self.slope}")
        print(f"b : {self.offset}")
        return super().__str__()

    def coefficients(self, P1, P2):
        if np.abs(P2.j - P1.j)>0:
            slope = (P2.i - P1.i) / (P2.j - P1.j)
        else:
            slope = (P2.i - P1.i) / (P2.j+1 - P1.j)
        offset = P1.i - slope * P1.j
        self.slope = slope 
        self.offset = offset
        self.coeffs = (slope, offset)
        return slope, offset

    def coords_xy(self, P1, P2):
        if np.abs(P1.j - P2.j) > np.abs(P1.i - P2.i):
            x = np.arange(P1.j, P2.j+1, step=np.sign(P2.j - P1.j))
            y = self.get_y(x)
        else:
            y = np.arange(P1.i, P2.i+1)
            x = self.get_x(y)
        self.x = x 
        self.y = y
        self.xy = x, y
        return x, y

    def draw(self, image, dx, dy, color):
        for i in range(self.x.size):
            for g in range(-dy//2, +dy//2+1):
                for h in range(-dx//2, +dx//2+1):
                    image.data[self.y[i]+g, self.x[i]+h][0] = color[0]
                    image.data[self.y[i]+g, self.x[i]+h][1] = color[1]
                    image.data[self.y[i]+g, self.x[i]+h][2] = color[2]


    def distance(self, P1, P2):
        distance = np.sqrt(np.abs(P2.i - P1.i) ** 2 + np.abs(P2.j - P1.j) ** 2)
        self.distance = distance
        return distance

    def get_y(self, x):
        return np.int32(self.slope * x + self.offset)
    
    def get_x(self, y):
        return np.int32((y - self.offset) / self.slope)
    
    def vect(self, P1, P2):
        self.nX = P2.j - P1.j
        self.nY = P2.i - P1.i
        return 0

###########################################################################################################################
###########################################################################################################################
###########################################################################################################################

path = os.path.dirname(__file__)

with open(f"{path}{os.sep}config.yml", 'r') as f:
    conf = yaml.load(f, Loader=yaml.SafeLoader)

path_in_raw = os.sep.join([conf["in"], "raw"]) + os.sep
path_in = os.sep.join([conf["in"], "denoise"]) + os.sep
path_out = conf["out"] + os.sep
path_out_images = path_out + "images" + os.sep

log = open(os.sep.join([path_out, "log.txt"]), "w")

# read parameters
visu = conf["visu"]
RESTART = conf["RESTART"]

dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print(f"{dt_string}", file=log)
print(f"Visualisation : {visu}")
print(f"Running program...", file=log)

# 1) check fort new photo in ./INPUT/raw that have to be denoised
print("------------------------------------------------", file=log)
print(f"Start preprocessing (denoising).", file=log)
print(f"Exploration of {path_in_raw} and {path_in}", file=log)
to_be_denoised, already_denoised = check_new_files(path_in_raw, path_in)
print(f"Following images have already been denoised: {already_denoised}", file=log)
if len(to_be_denoised)>0:
    print(f"New images have been found: {to_be_denoised}", log)
    print(f"Start denoising the new images: {to_be_denoised}", file=log)
    for file in to_be_denoised:
        file2 = '{:0>2}'.format(file)
        photo_in = os.sep.join([path_in_raw, str(file)]) + ".jpg"
        photo_out = os.sep.join([path_in, file2]) + "_denoise.jpg"
        _, txt = denoise(photo_in, photo_out, save=True)
        print(txt, file=log)
    print("Orange and Green markers have to be put on the new images.", file=log)
    print("END OF PROCESSING", file=log)
    exit()
else:
    print(f"All images have already been denoised.", file=log)

print("------------------------------------------------", file=log)
# 2) get results that have already been computed
ID_read = []
a_read = []
b_read = []
indices_read = []
DS_read = []
to_be_processed = np.arange(1, len(files(path_in))+1)
already_processed = []
fail_read = []
reject_read = []
if RESTART:
    print(f"RESTART=1  => All images in {path_in} will be analysed.", file=log)
else:
    print(f"RESTART=0  => Only new images that will be detected will be analysed.", file=log)
    print(f"Exploration of {path_in} and {path_out_images}", file=log)
    to_be_processed, already_processed = check_new_files(path_in, path_out_images)
    if len(to_be_processed)>0:
        print(f"New images have been found in {path_in}: {to_be_processed}.", file=log)
    else:
        print("No new images have been found.", file=log)
    try:
        ID_read, a_read, b_read, indices_read, DS_read, fail_read, reject_read = read_measures(f"{path_out}results.csv")
        print("Get data from results.csv: OK", file=log)
    except:
        print(f"Error loading file: results.csv", file=log)
        print(f"Processing has to start from scratch.", file=log)
        print(f"All images in {path_in} will be processed.", file=log)

reject = conf["reject"]

subset = os.listdir(path_in)

print(f"Images that are manually rejected from processing: {reject}", file=log)

discoidal_shift = list()
indices = list()
a = list()
b = list()
ID = list()
fail = list()

for file in subset:
    num = int(file.split("_")[0])
    if num in reject:
        print(f"Image number {num}: REJECTED", file=log)
    else:
        if num in to_be_processed:
            print(f"Processing of image {file}", file=log)
            print(file)
            image = IMAGE(log)
            image.load(path_in + file)
            image.fill_image()
            image.customize(save=True, show=False, out=path_out_images)
            if (image.a != 0) and (image.discoidal_shift != 90):
                a.append(image.a)
                b.append(image.b)
                discoidal_shift.append(float(image.discoidal_shift))
                ID.append(num)
                indices.append(image.cubital_index)
            else:
                print(f"Processing for image {file}: FAILED")
                fail.append(num)
                continue
        else:
            print(f"Image {file} has already been processed.", file=log)

# gather all results (results already computed + newly computed)
ID = ID + ID_read
a = a + a_read
b = b + b_read
indices = indices + indices_read
discoidal_shift = discoidal_shift + DS_read
rejected = reject + reject_read
fail = fail + fail_read

H = HISTOGRAM(indices=indices, visu=visu, path=path_out)
H.plot_histogram(show=False)

scatter_plot(path=path_out, indices=[indices], shifts=[discoidal_shift])

write_results(path=path_out, a=a, b=b, indices=indices, classes=H.classes, discoidal_shift=discoidal_shift, ID=ID, fail=fail, reject=reject)