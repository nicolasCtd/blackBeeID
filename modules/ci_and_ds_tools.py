from images import *
import numpy as np
import matplotlib.pyplot as plt
import logging

def get_zoom_center(file):
    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    if "zoom" not in file:
        print("Erreur : cette image n'est pas un zoom")
    else:
        a = file.find("xmin")
        b = file.find("xmax")
        c = file.find("ymin")
        d = file.find("ymax")
        e = file.find("end")

        xmin=int(file[a+4:b])
        xmax=int(file[b+4:c])
        ymin=int(file[c+4:d])
        ymax=int(file[d+4:e])
    return xmin, xmax, ymin, ymax

def sort_ci_points(nodes):
    nodes_ordered = list()
    if len(nodes) != 3:
        print("Erreur : le nombre de points CI devrait être égal à 3")
    else:
        # sort the 3 points from left to right 
        order = np.array(np.argsort(np.array([nodes[0].j, nodes[1].j, nodes[2].j])), dtype=int)
        for i in range(3):
            nodes_ordered.append(nodes[order[i]])
    return nodes_ordered

def sort_ds_points(nodes):
    nodes_ordered = list()
    if len(nodes) != 4:
        print("Erreur : le nombre de points DS devrait être égal à 4")
    else:
        idx = np.argmax([nodes[0].i, nodes[1].i, nodes[2].i, nodes[3].i])
        DS = nodes[idx]
        nodes.remove(nodes[idx])
        # sort the 3 points from left to right 
        order = np.array(np.argsort(np.array([nodes[0].j, nodes[1].j, nodes[2].j])), dtype=int)
        for i in range(3):
            nodes_ordered.append(nodes[order[i]])
        nodes_ordered.append(DS)
    return nodes_ordered

def compute_cubital_index(ci_points):
    n0 = ci_points[0]
    n1 = ci_points[1]
    n2 = ci_points[2]
    a = DROITE(n0, n1).distance
    b = DROITE(n1, n2).distance
    cubital_index = a/b
    return cubital_index

def compute_discoidal_shift(perp_02_point1, perp_02_point2, ds_points):
    U = DROITE(perp_02_point1, perp_02_point2)
    V = DROITE(ds_points[1], ds_points[3])
    dot = U.nX * V.nX + U.nY * V.nY
    delta = ds_points[3].j - U.get_x(ds_points[3].i)
    discoidal_shift = np.sign(delta) *  np.arccos(dot/(U.distance * V.distance)) * 180/np.pi
    return discoidal_shift

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
        # self.data = np.copy((plt.imread(file)*255).astype(np.uint8))
        #self.data = (self.data * 255).astype(np.uint8)
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
    
    def draw_ci_lines(self, clr):
        # draw lines between cubital index points
        DROITE(self.ci_points[0], self.ci_points[1]).draw(self, 2, 2, color=clr)
        DROITE(self.ci_points[1], self.ci_points[2]).draw(self, 2, 2, color=clr)
        return 0
    
    def draw_ds_line_02(self, clr):
        DROITE(self.ds_points[0], self.ds_points[2]).draw(self, 2, 2, color=clr)
        return 0
    
    def draw_ds_line_02_perpendicular(self, clr):
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
            logging.info(txt)
            # print(txt, file=self.log)
            print(txt)
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
        DROITE(point1, point2).draw(self, 2, 5, color=clr)
        self.point1 = point1
        self.point2 = point2
        return 0
        
    
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
