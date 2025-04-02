# from images import *
from images2 import *
import matplotlib.pyplot as plt

import sys
import os

from datetime import datetime, date

import shutil

import zipfile

from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal, QEvent
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QGridLayout,
    QSizePolicy,
    QTabWidget,
    QDesktopWidget,
    QDockWidget,
    QMessageBox,
    QLineEdit,
    QFileDialog,
    QInputDialog
)
from PyQt5.QtGui import QPixmap, QCursor, QFont

from PyQt5.QtGui import QPainter, QColor, QCloseEvent
from PyQt5 import QtCore, QtGui, QtWidgets

from functools import partial

from PIL import Image, ImageDraw, ImageFont



def insertnow(file):       
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").replace("/", "_").replace(" ", "___").replace(":", "_")
    tmp = file.split(".")
    return tmp[0] + "___" + dt_string + "." + tmp[-1]

def get_file_name(path):
    path_split = path.replace(os.sep, "/").split("/")
    name = path_split[-1]
    return name.split("_")[0]

def get_path(path2file):
    path_split = path2file.replace(os.sep, "/").split("/")
    return os.sep.join(path_split[:-1]) + os.sep

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
    print(nodes_ordered)
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


class FolderSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.button = QPushButton('Select Folder', self)
        self.button.clicked.connect(self.showFolderDialog)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def showFolderDialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        print('Selected Folder:', folder_path)


class Third(QMainWindow):
    def __init__(self, parent=None):
        super(Third, self).__init__(parent)

    def display(self, path_to_image):
        self.label = QLabel(self)
        pixmap = QPixmap(path_to_image)

        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)

        self.pixmapWidth = pixmap.width()
        self.pixmapHeight = pixmap.height()

        coeff = 0.83
        self.label.setFixedSize(int(self.pixmapWidth*coeff), int(self.pixmapHeight*coeff))

        self.label.setScaledContents(True)

class Second(QMainWindow):
    def __init__(self, Tab, num, parent=None):
        super(Second, self).__init__(parent)
        self.setWindowTitle("Fenêtre d'édition")
        self.num = str(num)
        self.move(50, 100)

        self.w = QWidget()
        self.layout = QVBoxLayout(self.w)

        self.switch_button_zoom_in = True
        self.switch_button_zoom_out = False

        self.count_ci_points = 0
        self.count_ds_points = 0

        self.switch_ci = False
        self.switch_ds = False
        self.switch_back = False
        self.switch_done = False

        self.ZOOM = 0
        self.last_name =  ["", ""]

        self.color_ci = [0, 255, 255]
        self.color_ds = [255, 255, 51]

        self.LAB_RIGHT = Tab.label_right
        self.WIDTH = Tab.width
        self.HEIGHT = Tab.height
        self.NUM = Tab.num

        self.ci_points = [POINT(), POINT(), POINT()]
        self.ds_points = [POINT(), POINT(), POINT(), POINT()]


    def display(self, fileName):

        self.name = get_file_name(fileName).replace(".jpg", "").replace("png", "")
        self.extension = "." + fileName.split(".")[-1]
        self.path = get_path(fileName)

        self.tmp = "tmp" + os.sep + self.num + os.sep
        self.out = "out" + os.sep + self.num + os.sep

        self.last_name[self.ZOOM] = insertnow(self.name + self.extension)

        try:
            os.makedirs(self.tmp)
        except:
            pass

        try:
            os.makedirs(self.out)
        except:
            pass

        try:
            shutil.copyfile(fileName, self.path + self.tmp + self.last_name[self.ZOOM])
            
        except:
            pass


        self.label = QLabel(self)
        pixmap = QPixmap(fileName)

        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)

        self.pixmapWidth = pixmap.width()
        self.pixmapHeight = pixmap.height()

        coeff = 0.83
        self.label.setFixedSize(int(self.pixmapWidth*coeff), int(self.pixmapHeight*coeff))

        self.label.setScaledContents(True)

        self.set_dock()
    
    # def show(self, fileName):
    #     self.label = QLabel(self)
    #     pixmap = QPixmap(fileName)

    #     self.label.setPixmap(pixmap)
    #     self.setCentralWidget(self.label)
    #     return
    
    def set_dock(self):
        self.btn_zoom_1 = QPushButton("  ZOOM IN ")
        self.btn_zoom_1.setIcon(QtGui.QIcon(f"images{os.sep}search.png"))
        self.btn_zoom_1.setFont(QFont('Times', 14))
        self.btn_zoom_1.clicked.connect(partial(self.zoom_in, True))

        self.btn_zoom_2 = QPushButton("  ZOOM OUT")
        self.btn_zoom_2.setIcon(QtGui.QIcon(f"images{os.sep}fusee.webp"))
        self.btn_zoom_2.setFont(QFont('Times', 14))
        self.btn_zoom_2.clicked.connect(self.zoom_out)

        self.btn_zoom_1.setEnabled(self.switch_button_zoom_in)
        self.btn_zoom_2.setEnabled(self.switch_button_zoom_out)

        self.btn_cancel = QPushButton("")
        self.btn_cancel.setIcon(QtGui.QIcon(f"images{os.sep}back.png"))
        self.btn_cancel.clicked.connect(self.cancel)

        self.btn_cancel.setEnabled(self.switch_back)

        self.btn_ci_points = QPushButton("3 CI points")
        self.btn_ci_points.setFont(QFont('Times', 13))
        self.btn_ci_points.clicked.connect(partial(self.set_ci_points, switch=self.switch_ci))

        self.btn_ds_points = QPushButton("4 DS points")
        self.btn_ds_points.setFont(QFont('Times', 13))
        self.btn_ds_points.clicked.connect(partial(self.set_ds_points, switch=self.switch_ds))

        self.btn_done = QPushButton("  Done")
        self.btn_done.setIcon(QtGui.QIcon(f"images{os.sep}done.jpg"))
        self.btn_done.setFont(QFont('Times', 14))
        self.btn_done.setEnabled(self.switch_done)
        self.btn_done.clicked.connect(self.validate_editing)

        self.layout.addWidget(self.btn_zoom_1)
        self.layout.addWidget(self.btn_zoom_2)
        self.layout.addWidget(self.btn_cancel)
        self.layout.addWidget(self.btn_ci_points)
        self.layout.addWidget(self.btn_ds_points)
        self.layout.addWidget(self.btn_done)
        self.dock = QDockWidget(f"{self.name}{self.extension}", self)
        self.dock.setFeatures(QDockWidget.DockWidgetMovable)
        self.dock.setWidget(self.w)

    def validate_editing(self):
        file_wo_zoom, file_w_zoom = self.get_last_file(self.tmp)
        im = IMAGE()
        im.load(f"{self.path}{self.tmp}{file_wo_zoom}")
        im.ci_points = sort_ci_points(self.ci_points)
        im.ds_points = sort_ds_points(self.ds_points)
        im.draw_ci_lines(self.color_ci)
        im.draw_ds_line_02(self.color_ds)
        im.draw_ds_line_02_perpendicular(self.color_ds)
        self.ci_value = compute_cubital_index(self.ci_points)
        self.ds_value = compute_discoidal_shift(im.point1, im.point2, im.ds_points)
        # im.customize()
        # shutil.copyfile(f"{self.path}{self.tmp}{file_wo_zoom}", f"{self.path}{self.out}{file_wo_zoom}")
        plt.imsave(fname=f"{self.path}{self.out}{self.name}_out{self.extension}", arr=im.data)
        self.add_infos()
        self.write_results()
        
        pixmap = QPixmap(f"{self.path}{self.out}{self.name}_out{self.extension}")
        pixmap = pixmap.scaled(self.WIDTH, self.HEIGHT, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.LAB_RIGHT[self.NUM-1].setPixmap(pixmap)

        self.close()
        return 0

    def add_infos(self):
        img = Image.open(f"{self.path}{self.out}{self.name}_out{self.extension}")
        # Create a drawing object
        draw = ImageDraw.Draw(img)

        # Define text attributes
        num = self.num
        ci = int(self.ci_value*100)/100
        ds = int(self.ds_value*100)/100
        tt = ""
        if np.sign(ds) == 1:
            tt = "+"
        text = f"Abeille #{num}             Indice cubital : {ci}             Angle discoïdal : {tt}{ds}°"
        font = ImageFont.truetype(f"{self.path}font{os.sep}Paul-le1V.ttf", size=40)
        text_color = (255, 0, 0)  # Red color

        # Position of the text
        position = (50, 25)

        # Add text to the image
        draw.text(position, text, fill=text_color, font=font)

        # Save or display the image
        img.save(f"{self.path}{self.out}{self.name}_out{self.extension}")

    def write_results(self):
        with open(self.path + os.sep + "out" + os.sep + "results.txt", "a") as f:
            ds_value = float(str(self.ds_value).replace("[", "").replace("]", ""))
            line = f"{self.num} {int(self.ci_value*100)/100} {int(ds_value*100)/100}\n"
            f.write(line)
        f.close()
        return 0

    def set_ci_points(self, switch):
        self.switch_ci = switch
        # Set the cursor to a cross cursor
        self.setCursor(Qt.CrossCursor)
        self.label.mousePressEvent = self.getPos_ci
    
    def set_ds_points(self, switch):
        self.switch_ds = switch
        # Set the cursor to a cross cursor
        self.setCursor(Qt.CrossCursor)
        self.label.mousePressEvent = self.getPos_ds

    def getPos_ci(self, event):
        self.count_ci_points += 1
        if  self.count_ci_points <= 3:
            x, y = self.get_pos_in_widget(event)
            file = self.last_name[self.ZOOM]
            if self.ZOOM:
                xmin, xmax, ymin, ymax = get_zoom_center(file)
                new_name = insertnow(self.name + "_zoom_" + f"xmin{xmin}xmax{xmax}ymin{ymin}ymax{ymax}end" + f"_CI_{self.count_ci_points}" + f"_DS_{self.count_ds_points}" + self.extension)
            else:
                new_name = insertnow(self.name + f"_CI_{self.count_ci_points}" + f"_DS_{self.count_ds_points}" + self.extension)
                xmin, xmax, ymin, ymax = 0, 0, 0, 0
            self.last_name[self.ZOOM] = new_name
            A = IMAGE()
            A.load(self.tmp + file)
            node, node_zoom = POINT(), POINT()
            node_zoom.j, node_zoom.i = x, y
            node.j, node.i = x+xmin, y+ymin
            self.ci_points[self.count_ci_points-1] = node
            if self.ZOOM:
                A.highlight(node_zoom, self.color_ci)
            else:
                A.highlight(node, self.color_ci)
            plt.imsave(fname=f"{self.tmp}{self.last_name[self.ZOOM]}", arr=A.data)
            pixmap = QPixmap(f"{self.tmp}{os.sep}{self.last_name[self.ZOOM]}")
            self.label.setPixmap(pixmap)
            self.setCentralWidget(self.label)
            self.setCursor(Qt.ArrowCursor)
            if self.ZOOM:
                file_wo_zoom, file_w_zoom = self.get_last_file(self.tmp)
                B = IMAGE()
                B.load(self.tmp + file_wo_zoom)
                B.highlight(node, self.color_ci)
                new_name = insertnow(self.name + f"_CI_{self.count_ci_points}" + f"_DS_{self.count_ds_points}" + self.extension)
                plt.imsave(fname=f"{self.tmp}{new_name}", arr=B.data)
        if self.count_ci_points in [1, 2, 3]:
            self.switch_back = True
        else:
            self.switch_back = False
        if self.count_ci_points >= 3:
            self.switch_ci = False
        else:
            self.switch_ci = True
        
        if self.count_ci_points == 3 and self.count_ds_points == 4:
            self.switch_done = True
        
        self.btn_cancel.setEnabled(self.switch_back)
        self.btn_ci_points.setEnabled(self.switch_ci)
        self.btn_done.setEnabled(self.switch_done)
        self.setCursor(Qt.ArrowCursor)

    def getPos_ds(self, event):
        self.count_ds_points += 1
        if  self.count_ds_points <= 4:
            x, y = self.get_pos_in_widget(event)
            file = self.last_name[self.ZOOM]
            if self.ZOOM:
                xmin, xmax, ymin, ymax = get_zoom_center(file)
                new_name = insertnow(self.name + "_zoom_" + f"xmin{xmin}xmax{xmax}ymin{ymin}ymax{ymax}end" + f"_CI_{self.count_ci_points}" + f"_DS_{self.count_ds_points}" + self.extension)
            else:
                new_name = insertnow(self.name + f"_CI_{self.count_ci_points}" + f"_DS_{self.count_ds_points}" + self.extension)
                xmin, xmax, ymin, ymax = 0, 0, 0, 0
            self.last_name[self.ZOOM] = new_name
            A = IMAGE()
            A.load(self.tmp + file)
            node, node_zoom = POINT(), POINT()
            node_zoom.j, node_zoom.i = x, y
            node.j, node.i = x+xmin, y+ymin
            self.ds_points[self.count_ds_points-1] = node
            if self.ZOOM:
                A.highlight(node_zoom, self.color_ds)
            else:
                A.highlight(node, self.color_ds)

            A.highlight(node, self.color_ds)
            plt.imsave(fname=f"{self.tmp}{self.last_name[self.ZOOM]}", arr=A.data)
            pixmap = QPixmap(f"{self.tmp}{os.sep}{self.last_name[self.ZOOM]}")
            self.label.setPixmap(pixmap)
            self.setCentralWidget(self.label)
            self.setCursor(Qt.ArrowCursor)
            if self.ZOOM:
                file_wo_zoom, file_w_zoom = self.get_last_file(self.tmp)
                B = IMAGE()
                B.load(self.tmp + file_wo_zoom)
                B.highlight(node, self.color_ds)
                new_name = insertnow(self.name + f"_CI_{self.count_ci_points}" + f"_DS_{self.count_ds_points}" + self.extension)
                plt.imsave(fname=f"{self.tmp}{new_name}", arr=B.data)
            
        if self.count_ds_points in [1, 2, 3, 4]:
            self.switch_back = True
        else:
            self.switch_back = False
        
        if self.count_ds_points >= 4:
            self.switch_ds = False
        else:
            self.switch_ds = True
        
        if self.count_ci_points == 3 and self.count_ds_points == 4:
            self.switch_done = True
            
        self.btn_cancel.setEnabled(self.switch_back)
        self.btn_ds_points.setEnabled(self.switch_ds)
        self.btn_done.setEnabled(self.switch_done)

        self.setCursor(Qt.ArrowCursor)

    def cancel(self):
        last_file_wo_zoom, last_file_w_zoom = self.get_last_file(path=self.tmp)
        os.remove(self.path + self.tmp + last_file_wo_zoom)
        try:
            os.remove(self.path + self.tmp + last_file_w_zoom)
        except:
            pass
        last_file_wo_zoom, last_file_w_zoom = self.get_last_file(path=self.tmp)
        self.last_name[0] = last_file_wo_zoom
        self.last_name[1] = last_file_w_zoom

        pixmap = QPixmap(f"{self.tmp}{os.sep}{self.last_name[self.ZOOM]}")
        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)

        if ("CI_0" in last_file_wo_zoom) or ("CI" not in last_file_wo_zoom):
            self.count_ci_points = 0
        elif "CI_1" in last_file_wo_zoom:
            self.count_ci_points = 1
            self.ci_points[1] = POINT()
            self.ci_points[2] = POINT()
        elif "CI_2" in last_file_wo_zoom:
            self.count_ci_points = 2
            self.ci_points[2] = POINT()
        elif "CI_3" in last_file_wo_zoom:
            self.count_ci_points = 3

        if ("DS_0" in last_file_wo_zoom) or ("DS" not in last_file_wo_zoom):
            self.count_ds_points = 0
        elif "DS_1" in last_file_wo_zoom:
            self.count_ds_points = 1
        elif "DS_2" in last_file_wo_zoom:
            self.count_ds_points = 2
        elif "DS_3" in last_file_wo_zoom:
            self.count_ds_points = 3
        elif "DS_4" in last_file_wo_zoom:
            self.count_ds_points = 4

        if (self.count_ci_points<1) and (self.count_ds_points<1):
            self.switch_back = False
        else:
            self.switch_back = True

        if self.count_ci_points >= 3:
            self.switch_ci = False 
        else:
            self.switch_ci = True

        if self.count_ds_points >= 4:
            self.switch_ds = False 
        else:
            self.switch_ds = True

        self.btn_cancel.setEnabled(self.switch_back)
        self.btn_ci_points.setEnabled(self.switch_ci)
        self.btn_ds_points.setEnabled(self.switch_ds)
        self.switch_done = False
        self.btn_done.setEnabled(self.switch_done)
        
        return 0


    def zoom_in(self, ZOOM=True):
        file_wo_zoom, file_w_zoom = self.get_last_file(self.path + self.tmp)
        self.ZOOM = ZOOM
        pixmap = QPixmap(f"images{os.sep}search.png")
        pixmap = pixmap.scaled(32, 32)
        cursor = QCursor(pixmap, 32, 32)
        self.setCursor(cursor)
        pixmap = QPixmap(file_wo_zoom)
        self.label.mousePressEvent = self.getPos_and_zoom
        return 0

    def get_last_file(self, path):

        file_w_zoom = ""
        file_wo_zoom = ""

        time0 =  datetime.strptime("01/01/2000 00:00:00", "%d/%m/%Y %H:%M:%S")

        for file in os.listdir(path):
            if "zoom" not in file:
                tmp = file.replace(self.extension, "").split("___")
                date1 = tmp[-2].replace("_", "/")
                hour1 = tmp[-1].replace("_", ":")
                time1 = datetime.strptime(date1 + " " + hour1, "%d/%m/%Y %H:%M:%S")
                if time1 >= time0:
                    time0 = time1
                    file_wo_zoom = file
                else:
                    continue

        for file in os.listdir(path):
            if "zoom" in file:
                tmp = file.replace(self.extension, "").split("___")
                date1 = tmp[-2].replace("_", "/")
                hour1 = tmp[-1].replace("_", ":")
                time1 = datetime.strptime(date1 + " " + hour1, "%d/%m/%Y %H:%M:%S")
                if time1 >= time0:
                    time0 = time1
                    file_w_zoom = file
                else:
                    continue

        return file_wo_zoom, file_w_zoom

    def zoom_out(self):
        last_file_wo_zoom, last_file_w_zoom = self.get_last_file(path=self.tmp)
        pixmap = QPixmap(self.path + self.tmp + last_file_wo_zoom)
        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)
        self.switch_button_zoom_in = True
        self.btn_zoom_1.setEnabled(self.switch_button_zoom_in)
        self.switch_button_zoom_out = False
        self.btn_zoom_2.setEnabled(self.switch_button_zoom_out)
        self.ZOOM = 0
        self.last_name[0] = last_file_wo_zoom
        self.last_name[1] = last_file_w_zoom
        return 0
    
        
    def display_error_message(self):
        self.move(450, 200)
        layout = QVBoxLayout()
        pixmap = QPixmap(f"images" + os.sep + "coconfort.png")
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)
        txt = QLabel("Veuillez d'abord charger une image \navant de l'éditer...")
        layout.addWidget(txt)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setFixedWidth(300)
        self.setFixedHeight(300)


    def get_pos_in_widget(self, event):
        pos = event.pos()

        pixmapRect = self.label.pixmap().rect()
        contentsRect = QtCore.QRectF(self.label.contentsRect())

        fx = pixmapRect.width() / contentsRect.width()
        fy = pixmapRect.height() / contentsRect.height()

        x = int(pos.x() * fx)
        y = int(pos.y() * fy)

        return x, y

    def getPos_and_zoom(self, event):

        x, y = self.get_pos_in_widget(event)

        zoom_x = int(self.pixmapWidth / 2.5)
        zoom_y = int(self.pixmapHeight / 2.5)

        self.btn_zoom_1.setEnabled(self.switch_button_zoom_in)

        if self.switch_button_zoom_in and self.ZOOM:

            file_wo_zoom, file_w_zoom = self.get_last_file(self.tmp)

            A = IMAGE()
            A.load(self.path + self.tmp + file_wo_zoom)
            
            j_min = max(x-zoom_x//2, 0)
            j_max = min(x+zoom_x//2, A.data.shape[1])

            i_min = max(y-zoom_y//2, 0)
            i_max = min(y+zoom_y//2, A.data.shape[0])

            image_temp = A.data[i_min:i_max, j_min:j_max, :]

            new_name = insertnow(self.name + "_zoom_" + f"xmin{j_min}xmax{j_max}ymin{i_min}ymax{i_max}end" + self.extension)
            self.last_name[self.ZOOM] = new_name

            plt.imsave(fname=f"{self.tmp}{new_name}", arr=image_temp)

            pixmap = QPixmap(f"{self.tmp}{os.sep}{new_name}")

            self.label.setPixmap(pixmap)

            self.setCentralWidget(self.label)
        
            cursor = QCursor(Qt.ArrowCursor)
            self.setCursor(cursor)

            self.switch_button_zoom_in = False
            self.switch_button_zoom_out = True
            self.btn_zoom_1.setEnabled(self.switch_button_zoom_in)
            self.btn_zoom_2.setEnabled(self.switch_button_zoom_out)
            self.ZOOM = 1

        else:
            pass
        
        return


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analyse des ailes d'abeilles")

        try:
            os.makedirs("out")
        except:
            pass

        try:
            os.makedirs("tmp")
        except:
            pass

        self.path = os.path.abspath(os.getcwd()) + os.sep + "out"


        with open(self.path + os.sep + "results.txt", "w") as f:
            line = f"num indice_cubital angle_discoidal\n"
            f.write(line)
            f.close


        # for filename in os.listdir(self.path):
        #     file_path = self.path + os.sep + filename
        #     try:
        #         if os.path.isfile(file_path):
        #             os.unlink(file_path)
        #         elif os.path.isdir(file_path):
        #             shutil.rmtree(file_path)
        #     except Exception as e:
        #         print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        path = os.path.abspath(os.getcwd()) + os.sep + "tmp"
        for filename in os.listdir(path):
            file_path = path + os.sep + filename
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        self.tab_widget = Tab(self, self.path)
        self.setCentralWidget(self.tab_widget)
    
        self.showMaximized()

        QTimer.singleShot(100, self.calculate)

    def calculate(self):
        return self.frameGeometry().height()

    def close_all_windows(self):
        win_list = QApplication.allWindows()
        for w in win_list:
            w.close()

    # def closeEvent(self, event: QCloseEvent) -> None:
    #     close = QMessageBox()
    #     close.setText("Voulez vous vraiment quitter l'application ?")
    #     close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    #     close = close.exec()

        # if close == QMessageBox.Yes:
        #     event.accept()
        #     self.close_all_windows()
        # else:
        #     event.ignore()


class Tab(QWidget): 
    def __init__(self, parent, path): 
        super(QWidget, self).__init__(parent)

        self.num = 0
        self.path = path

        self.analyse_name = str(date.today())

        self.fileName1 = "im1.png"
        self.fileName2 = "im2.png"
        self.fileName3 = "im3.png"
        self.fileName4 = "im4.png"
        self.fileName5 = "im5.png"
        self.fileName6 = "im6.png"
        self.fileName7 = "im7.png"
        self.fileName8 = "im8.png"
        self.fileName9 = "im9.png"
        self.fileName10 = "im10.png"
        self.fileName11 = "im11.png"
        self.fileName12 = "im12.png"
        self.fileName13 = "im13.png"
        self.fileName14 = "im14.png"
        self.fileName15 = "im15.png"
        self.fileName16 = "im16.png"
        self.fileName17 = "im17.png"
        self.fileName18 = "im18.png"
        self.fileName19 = "im19.png"
        self.fileName20 = "im20.png"

        self.layout = QVBoxLayout(self)
  
        # Initialize tab screen 
        self.tabs = QTabWidget()

        self.tab0 = QWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()
        self.tab9 = QWidget()
        self.tab10 = QWidget()
  
        # Add tabs

        mf = QFont("Times New Roman", 13)

        self.tabs.addTab(self.tab0, "Main")
        self.tabs.addTab(self.tab1, "1-5")
        self.tabs.addTab(self.tab2, "6-10")
        self.tabs.addTab(self.tab3, "11-15")
        self.tabs.addTab(self.tab4, "16-20")
        self.tabs.addTab(self.tab5, "21-25")
        self.tabs.addTab(self.tab6, "26-30")
        self.tabs.addTab(self.tab7, "31-35")
        self.tabs.addTab(self.tab8, "36-40")
        self.tabs.addTab(self.tab9, "41-45")
        self.tabs.addTab(self.tab10, "46-50")

        self.width = 413
        self.height = 307

        nb_tabs = 4

        self.label_left = [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)]
        
        self.label_right = [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)]
        
        # self.dialog = [Second(self), Second(self), Second(self), Second(self), Second(self),
        #                 Second(self), Second(self), Second(self), Second(self), Second(self),
        #                 Second(self), Second(self), Second(self), Second(self), Second(self)]

        connections_load = {1:self.browseFile1, 2:self.browseFile2, 3:self.browseFile3, 4:self.browseFile4, 5:self.browseFile5,
                       6:self.browseFile6, 7:self.browseFile7, 8:self.browseFile8, 9:self.browseFile9, 10:self.browseFile10,
                       11:self.browseFile11, 12:self.browseFile12, 13:self.browseFile13, 14:self.browseFile14, 15:self.browseFile15,
                       16:self.browseFile16, 17:self.browseFile17, 18:self.browseFile18, 19:self.browseFile19, 20:self.browseFile20}
        
        connections_edit = {1:self.editFile1, 2:self.editFile2, 3:self.editFile3, 4:self.editFile4, 5:self.editFile5,
                       6:self.editFile6, 7:self.editFile7, 8:self.editFile8, 9:self.editFile9, 10:self.editFile10,
                       11:self.editFile11, 12:self.editFile12, 13:self.editFile13, 14:self.editFile14, 15:self.editFile15,
                       16:self.editFile16, 17:self.editFile17, 18:self.editFile18, 19:self.editFile19, 20:self.editFile20}

        connections_visu = {1:self.visu1, 2:self.visu2, 3:self.visu3, 4:self.visu4, 5:self.visu5,
                       6:self.visu6, 7:self.visu7, 8:self.visu8, 9:self.visu9, 10:self.visu10,
                       11:self.visu11, 12:self.visu12, 13:self.visu13, 14:self.visu14, 15:self.visu15,
                       16:self.visu16, 17:self.visu17, 18:self.visu18, 19:self.visu19, 20:self.visu20}

        layout_main = QGridLayout()
        btn1 = QPushButton("Charger \nune analyse")
        btn2 = QPushButton("Sauvegarder \nl'analyse")
        btn3 = QPushButton("Lancer \nl'analyse")
        label0 = QLabel("Nom de l'analyse : ")
        self.label00 = QLabel(self.analyse_name)
        label1 = QLabel("<u>Histogramme de l'Indice Cubital<u>")
        label2 = QLabel("<u>Indice Cubital vs Discoidal shift<u>")
        # self.edit_analyse_name = QLineEdit()

        self.pb = QPushButton("Editer")
        self.pb.clicked.connect(self.edit_name)

        my_font = QFont("Times New Roman", 20)
        my_font2 = QFont("Times New Roman", 15)
        my_font3 = QFont("Times New Roman", 13)
        label1.setFont(my_font)
        label2.setFont(my_font)
        label0.setFont(my_font2)
        btn1.setFont(my_font3)
        btn2.setFont(my_font3)
        btn3.setFont(my_font3)

        # label1.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px;");

        btn1.resize(150, 150)
        btn1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        btn2.resize(150, 150)
        btn2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        btn3.resize(150, 150)
        btn3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.pb.resize(150, 150)
        self.pb.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        pixmap = QPixmap(f"images{os.sep}empty1.png")
        image_empty1 = QLabel()
        image_empty1.setPixmap(pixmap)

        pixmap = QPixmap(f"images{os.sep}empty2.png")
        image_empty2 = QLabel()
        image_empty2.setPixmap(pixmap)

        layout_main.addWidget(label0, 0, 0, 1, 2)
        # layout_main.addWidget(self.edit_analyse_name, 0, 1, 1, 2)
        layout_main.addWidget(self.label00, 0, 1, 1, 2)
        layout_main.addWidget(self.pb, 0, 2, 1, 1)
        layout_main.addWidget(btn1, 1, 0, 2, 2)
        layout_main.addWidget(btn2, 1, 1, 2, 2)
        layout_main.addWidget(btn3, 1, 2, 2, 2)
        layout_main.addWidget(label1, 3, 0, 1, 5)
        layout_main.addWidget(label2, 3, 7, 1, 5)
        layout_main.addWidget(image_empty1, 4, 0, 5, 5)
        layout_main.addWidget(image_empty2, 4, 7, 5, 5)

        btn2.clicked.connect(self.save_project)

        self.grids = list()

        for num_tab in range(1, nb_tabs+1):
            
            self.grids.append(QGridLayout())

            for i in range(5):

                num_image = 5 * (num_tab - 1) + i + 1

                pixmap = QPixmap(f"images{os.sep}dardagnan.png")
                label = QLabel()
                label.setPixmap(pixmap)
                self.grids[-1].addWidget(label, i, 0)

                pixmap = QPixmap(f"images{os.sep}im{num_image}.png")
                label_left = self.label_left[num_image-1]
                label_left.setPixmap(pixmap)
                self.grids[-1].addWidget(label_left, i, 2, 1, 1)

                pixmap = QPixmap(f"images{os.sep}im{num_image}.png")
                label_right = self.label_right[num_image-1]
                label_right.setPixmap(pixmap)
                self.grids[-1].addWidget(label_right, i, 4, 1, 1)

                btn1 = QPushButton("Load")
                btn1.resize(50, 150)
                btn1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                
                btn2 = QPushButton("Edit")
                btn2.resize(50, 150)
                btn2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                btn3 = QPushButton("Visualize")
                btn3.resize(50, 150)
                btn3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                # self.grids[-1].addWidget(btn1, i, 1, alignment=QtCore.Qt.AlignLeft)
                # self.grids[-1].addWidget(btn2, i, 2, alignment=QtCore.Qt.AlignCenter)
                self.grids[-1].addWidget(btn1, i, 1)
                self.grids[-1].addWidget(btn2, i, 3)
                self.grids[-1].addWidget(btn3, i, 5)
                

                btn1.clicked.connect(connections_load[num_image])
                btn2.clicked.connect(connections_edit[num_image])
                btn3.clicked.connect(connections_visu[num_image])

                # pixmap = QPixmap(f"images{os.sep}dardagnan.png")
                # label = QLabel()
                # label.setPixmap(pixmap)
                # self.grids[-1].addWidget(label, i, 5)

                pixmap = QPixmap(f"images{os.sep}dardagnan.png")
                darda = QLabel()
                darda.setPixmap(pixmap)
                self.grids[-1].addWidget(darda, i, 6)

                # self.grids[-1].addWidget(label_right, i, 3)

        # Create main tab 
        self.tab0.layout = layout_main
        self.tab0.setFont(mf)
        self.tab0.setLayout(self.tab0.layout)

        # Create first tab 
        self.tab1.layout = self.grids[0]
        self.tab1.setFont(mf)
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab 
        self.tab2.layout = self.grids[1]
        self.tab2.setFont(mf)
        self.tab2.setLayout(self.tab2.layout)

        # Create third tab 
        self.tab3.layout = self.grids[2]
        self.tab3.setFont(mf)
        self.tab3.setLayout(self.tab3.layout)

        # Create fourth tab 
        self.tab4.layout = self.grids[3]
        self.tab4.setLayout(self.tab4.layout)

        # Final step
        # #######
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def edit_name(self):
        text, okPressed = QInputDialog.getText(self, " ", "Entrer le nom de l'analyse :", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.analyse_name = text
            self.label00.setText(text)


        return 0

    def editFile1(self):
        if self.fileName1 == "im1.png":
            self.dialog = Second(self, num=1)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=1)
            self.dialog.display(self.fileName1)
        self.dialog.show()
        
    def editFile2(self):
        if self.fileName2 == "im2.png":
            self.dialog = Second(self, num=2)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=2)
            self.dialog.display(self.fileName2)
        self.dialog.show()
    
    def editFile3(self):
        if self.fileName3 == "im3.png":
            self.dialog = Second(self, num=3)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=3)
            self.dialog.display(self.fileName3)
        self.dialog.show()
    
    def editFile4(self):
        if self.fileName4 == "im4.png":
            self.dialog = Second(self, num=4)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=4)
            self.dialog.display(self.fileName4)
        self.dialog.show()

    def editFile5(self):
        if self.fileName5 == "im5.png":
            self.dialog = Second(self, num=5)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=5)
            self.dialog.display(self.fileName5)
        self.dialog.show()
    
    def editFile6(self):
        if self.fileName6 == "im6.png":
            self.dialog = Second(self, num=6)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=6)
            self.dialog.display(self.fileName6)
        self.dialog.show()
    
    def editFile7(self):
        if self.fileName7 == "im7.png":
            self.dialog = Second(self, num=7)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=7)
            self.dialog.display(self.fileName7)
        self.dialog.show()
    
    def editFile8(self):
        if self.fileName8 == "im8.png":
            self.dialog = Second(self, num=8)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=8)
            self.dialog.display(self.fileName8)
        self.dialog.show()
    
    def editFile9(self):
        if self.fileName9 == "im9.png":
            self.dialog = Second(self, num=9)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=9)
            self.dialog.display(self.fileName9)
        self.dialog.show()
    
    def editFile10(self):
        if self.fileName10 == "im10.png":
            self.dialog = Second(self, num=10)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=10)
            self.dialog.display(self.fileName10)
        self.dialog.show()

    def editFile11(self):
        if self.fileName11 == "im11.png":
            self.dialog = Second(self, num=11)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=11)
            self.dialog.display(self.fileName11)
        self.dialog.show()

    def editFile12(self):
        if self.fileName12 == "im12.png":
            self.dialog = Second(self, num=12)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=12)
            self.dialog.display(self.fileName12)
        self.dialog.show()

    def editFile13(self):
        if self.fileName13 == "im13.png":
            self.dialog = Second(self, num=13)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=13)
            self.dialog.display(self.fileName13)
        self.dialog.show()

    def editFile14(self):
        if self.fileName14 == "im14.png":
            self.dialog = Second(self, num=14)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=14)
            self.dialog.display(self.fileName14)
        self.dialog.show()
    
    def editFile15(self):
        if self.fileName15 == "im15.png":
            self.dialog = Second(self, num=15)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=15)
            self.dialog.display(self.fileName15)
        self.dialog.show()

    def editFile16(self):
        if self.fileName16 == "im16.png":
            self.dialog = Second(self, num=16)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=16)
            self.dialog.display(self.fileName16)
        self.dialog.show()

    def editFile17(self):
        if self.fileName17 == "im17.png":
            self.dialog = Second(self, num=17)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=17)
            self.dialog.display(self.fileName17)
        self.dialog.show()
    
    def editFile18(self):
        if self.fileName18 == "im18.png":
            self.dialog = Second(self, num=18)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=18)
            self.dialog.display(self.fileName18)
        self.dialog.show()

    def editFile19(self):
        if self.fileName18 == "im19.png":
            self.dialog = Second(self, num=19)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=19)
            self.dialog.display(self.fileName19)
        self.dialog.show()
    
    def editFile20(self):
        if self.fileName18 == "im20.png":
            self.dialog = Second(self, num=20)
            self.dialog.display_error_message()
        else:
            self.dialog = Second(self, num=20)
            self.dialog.display(self.fileName20)
        self.dialog.show()

    def browseFile1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName1, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName1 != "":
            pixmap = QPixmap(self.fileName1)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[0].setPixmap(pixmap)
            self.grids[0].addWidget(self.label_left[0], 0, 2, 1, 1)
            self.num = 1
            self.nameOut1 = "1"
        else:
            pass
        
    def browseFile2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName2, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName2 != "":
            pixmap = QPixmap(self.fileName2)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[1].setPixmap(pixmap)
            self.grids[0].addWidget(self.label_left[1], 1, 2, 1, 1)
            self.num = 2
            self.nameOut2 = "2"
        else:
            pass
            

    def browseFile3(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName3, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName3 != "":
            pixmap = QPixmap(self.fileName3)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[2].setPixmap(pixmap)
            self.grids[0].addWidget(self.label_left[2], 2, 2, 1, 1)
            self.num = 3
            self.nameOut3 = 3
        else:
            pass

    def browseFile4(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName4, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName4 != "":
            pixmap = QPixmap(self.fileName4)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[3].setPixmap(pixmap)
            self.grids[0].addWidget(self.label_left[3], 3, 2, 1, 1)
            self.num = 4
            self.nameOut4 = "4"
        else:
            pass

    def browseFile5(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName5, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName5 != "":
            pixmap = QPixmap(self.fileName5)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[4].setPixmap(pixmap)
            self.grids[0].addWidget(self.label_left[4], 4, 2, 1, 1)
            self.num = 5
            self.nameOut5 = "5"
        else:
            pass

    def browseFile6(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName6, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName6 != "":
            pixmap = QPixmap(self.fileName6)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[5].setPixmap(pixmap)
            self.grids[1].addWidget(self.label_left[5], 0, 2, 1, 1)
        else:
            pass
    
    def browseFile7(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName7, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName7 != "":
            pixmap = QPixmap(self.fileName7)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[6].setPixmap(pixmap)
            self.grids[1].addWidget(self.label_left[6], 1, 2, 1, 1)
        else:
            pass

    def browseFile8(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName8, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName8 != "":
            pixmap = QPixmap(self.fileName8)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[7].setPixmap(pixmap)
            self.grids[1].addWidget(self.label_left[7], 2, 2, 1, 1)
        else:
            pass


    def browseFile9(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName9, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName9 != "":
            pixmap = QPixmap(self.fileName9)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[8].setPixmap(pixmap)
            self.grids[1].addWidget(self.label_left[8], 3, 2, 1, 1)
        else:
            pass

    def browseFile10(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName10, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName10 != "":
            pixmap = QPixmap(self.fileName10)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[9].setPixmap(pixmap)
            self.grids[1].addWidget(self.label_left[9], 4, 2, 1, 1)
        else:
            pass

    def browseFile11(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName11, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName11 != "":
            pixmap = QPixmap(self.fileName11)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[10].setPixmap(pixmap)
            self.grids[2].addWidget(self.label_left[10], 0, 2, 1, 1)
        else:
            pass

    def browseFile12(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName12, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName12 != "":
            pixmap = QPixmap(self.fileName12)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[11].setPixmap(pixmap)
            self.grids[2].addWidget(self.label_left[11], 1, 2, 1, 1)
        else:
            pass

    def browseFile13(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName13, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName13 != "":
            pixmap = QPixmap(self.fileName13)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[12].setPixmap(pixmap)
            self.grids[2].addWidget(self.label_left[12], 2, 2, 1, 1)
        else:
            pass

    def browseFile14(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName14, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName14 != "":
            pixmap = QPixmap(self.fileName14)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[13].setPixmap(pixmap)
            self.grids[2].addWidget(self.label_left[13], 3, 2, 1, 1)
        else:
            pass

    def browseFile15(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName15, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName15 != "":
            pixmap = QPixmap(self.fileName15)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[14].setPixmap(pixmap)
            self.grids[2].addWidget(self.label_left[14], 4, 2, 1, 1)
        else:
            pass

    def browseFile16(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName16, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName16 != "":
            pixmap = QPixmap(self.fileName16)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[15].setPixmap(pixmap)
            self.grids[3].addWidget(self.label_left[15], 0, 2, 1, 1)
        else:
            pass 

    def browseFile17(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName17, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName18 != "":
            pixmap = QPixmap(self.fileName17)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[16].setPixmap(pixmap)
            self.grids[3].addWidget(self.label_left[16], 1, 2, 1, 1)
        else:
            pass 

    def browseFile18(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName18, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName18 != "":
            pixmap = QPixmap(self.fileName18)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[17].setPixmap(pixmap)
            self.grids[3].addWidget(self.label_left[17], 2, 2, 1, 1)
        else:
            pass 

    def browseFile19(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName19, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName19 != "":
            pixmap = QPixmap(self.fileName19)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[18].setPixmap(pixmap)
            self.grids[3].addWidget(self.label_left[18], 3, 2, 1, 1)
        else:
            pass 

    def browseFile20(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName20, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        if self.fileName20 != "":
            pixmap = QPixmap(self.fileName20)
            pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label_left[19].setPixmap(pixmap)
            self.grids[3].addWidget(self.label_left[19], 4, 2, 1, 1)
        else:
            pass

    def visu1(self):
        path = self.path + os.sep + "1"
        fileName = os.listdir(path)[0]
        A = Third(self)
        A.move(50, 50)
        A.display(path + os.sep + fileName)
        A.show()
        return 0

    def visu2(self):
        path = self.path + os.sep + "1"
        fileName = os.listdir(path)[0]
        a = Second(self, path)
        a.show()
        return 0
    
    def visu3(self):
        path = self.path + os.sep + "1"
        fileName = os.listdir(path)[0]
        a = Second(self, path)
        a.show()
        return 0

    def visu4(self):
        path = self.path + os.sep + "1"
        fileName = os.listdir(path)[0]
        a = Second(self, path)
        a.show()
        return 0

    def visu5(self):
        path = self.path + "out" + os.sep + "1"
        fileName = os.listdir(path)[0]
        a = Second(self, path)
        a.show()
        return 0

    def visu6(self):
        return 0
    def visu7(self):
        return 0
    def visu8(self):
        return 0
    def visu9(self):
        return 0
    def visu10(self):
        return 0
    def visu11(self):
        return 0
    def visu12(self):
        return 0
    def visu13(self):
        return 0
    def visu14(self):
        return 0
    def visu15(self):
        return 0
    def visu16(self):
        return 0
    def visu17(self):
        return 0
    def visu18(self):
        return 0
    def visu19(self):
        return 0
    def visu20(self):
        return 0

    def save_project(self):
        DIR = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        with zipfile.ZipFile(DIR + os.sep + self.analyse_name + '.zip', "w") as zf:
            for root, _, filenames in os.walk(os.path.basename(self.path)):
                for name in filenames:
                    name = os.path.join(root, name)
                    name = os.path.normpath(name)
                    zf.write(name, name)
        return 0

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

        # for file in os.listdir(self.dialog.path + "out" + os.sep + self.dialog.name):
        #     filename = file
        # pixmap = QPixmap(self.dialog.path + "out" + os.sep + self.dialog.name + os.sep + filename)
        # print(self.dialog.path + "out" + os.sep + self.dialog.name + os.sep + filename)
        # pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        # self.label_right[0].setPixmap(pixmap)