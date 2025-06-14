import sys
import os
import shutil
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QDockWidget,
)
from PyQt5.QtGui import QPixmap, QCursor, QFont

from PyQt5 import QtCore, QtGui

from functools import partial

from PIL import Image, ImageDraw, ImageFont
from modules.ci_and_ds_tools import *
from modules.utile import *
import logging

def resource_path(relative_path):
    """Retourne le chemin absolu, même si l'app est empaquetée avec PyInstaller"""
    if getattr(sys, 'frozen', False):
        # PyInstaller utilise ce répertoire temporaire
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Script normal
        return os.path.join(os.path.dirname(__file__), relative_path)

class MESSAGE(QMainWindow):
    def __init__(self):
        super(MESSAGE, self).__init__()
        self.error1 = "Veuillez d'abord charger une \nimage avant de l'éditer..."
        self.error2 = "Veuillez d'abord éditer \nune image..."

    def message_erreur1(self):
        self.setWindowTitle(' ')
        layout = QVBoxLayout()
        coconfort = resource_path(f"images" + os.sep + "coconfort.png")
        pixmap = QPixmap(coconfort)
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)
        txt = QLabel(self.error1)
        txt.setFont(QFont('Times', 12))
        layout.addWidget(txt)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def message_erreur2(self):
        self.setWindowTitle(' ')
        layout = QVBoxLayout()
        pixmap = QPixmap(f"images" + os.sep + "coconfort.png")
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)
        txt = QLabel(self.error2)
        txt.setFont(QFont('Times', 12))
        layout.addWidget(txt)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    def message(self, msg):
        self.move(100, 200)
        self.setWindowTitle(' ')
        layout = QHBoxLayout()
        aspicot = resource_path(f"images" + os.sep + "aspicot.png")
        pixmap = QPixmap(aspicot)
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)
        txt = QLabel(msg)
        txt.setFont(QFont('Times', 12))
        layout.addWidget(txt)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

class EDIT(QMainWindow):
    def __init__(self, tab, num, title=' ', parent=None):
        super(EDIT, self).__init__(parent)
        self.setWindowTitle(title)
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

        self.LAB_RIGHT = tab.label_right

        self.GRIDS = tab.grids
        self.WIDTH = tab.width
        self.HEIGHT = tab.height
        self.NUM = tab.num
        self.LAB_RES = tab.label_results
        self.RES = tab.RES

        self.ci_points = [POINT(), POINT(), POINT()]
        self.ds_points = [POINT(), POINT(), POINT(), POINT()]

        self.path = tab.path + os.sep


    def display(self, fileName):
        logging.info(f"Edition de l'image : {fileName}")
        self.name = get_file_name(fileName).replace(".jpg", "").replace("png", "")
        self.extension = "." + fileName.split(".")[-1]

        self.TMP = self.path + os.sep + "tmp" + os.sep + self.num + os.sep
        self.OUT = self.path + os.sep + "out" + os.sep

        self.last_name[self.ZOOM] = insertnow(self.name + self.extension)

        try:
            os.makedirs(self.TMP)
            logging.info(f"Création du répertoire : {self.TMP}")
        except:
            pass

        try:
            shutil.copyfile(fileName, self.TMP + self.last_name[self.ZOOM])
            logging.info(f"Copie du fichier : {fileName} >> {self.TMP}{self.last_name[self.ZOOM]}")
            
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
        self.show()
    
    def set_dock(self):
        search = resource_path(f"search.png")
        self.btn_zoom_1 = QPushButton("  ZOOM IN ")
        self.btn_zoom_1.setIcon(QtGui.QIcon(search))
        self.btn_zoom_1.setFont(QFont('Times', 14))
        self.btn_zoom_1.clicked.connect(partial(self.zoom_in, True))

        fusee = resource_path(f"fusee.webp")
        self.btn_zoom_2 = QPushButton("  ZOOM OUT")
        self.btn_zoom_2.setIcon(QtGui.QIcon(fusee))
        self.btn_zoom_2.setFont(QFont('Times', 14))
        self.btn_zoom_2.clicked.connect(self.zoom_out)

        self.btn_zoom_1.setEnabled(self.switch_button_zoom_in)
        self.btn_zoom_2.setEnabled(self.switch_button_zoom_out)

        back = resource_path(f"back.png")
        self.btn_cancel = QPushButton("")
        self.btn_cancel.setIcon(QtGui.QIcon(back))
        self.btn_cancel.clicked.connect(self.cancel)

        self.btn_cancel.setEnabled(self.switch_back)

        self.btn_ci_points = QPushButton("3 CI points")
        self.btn_ci_points.setFont(QFont('Times', 13))
        self.btn_ci_points.clicked.connect(partial(self.set_ci_points, switch=self.switch_ci))

        self.btn_ds_points = QPushButton("4 DS points")
        self.btn_ds_points.setFont(QFont('Times', 13))
        self.btn_ds_points.clicked.connect(partial(self.set_ds_points, switch=self.switch_ds))

        done = resource_path(f"done.jpg")
        self.btn_done = QPushButton("  Done")
        self.btn_done.setIcon(QtGui.QIcon(done))
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
        file_wo_zoom, file_w_zoom = self.get_last_file(self.TMP)
        im = IMAGE()
        img = resource_path(f"{self.TMP}{file_wo_zoom}")
        im.load(img)
        im.ci_points = sort_ci_points(self.ci_points)
        logging.info(f"Point Ci n°1 : (i,j)=({im.ci_points[0].i}, {im.ci_points[0].j})")
        logging.info(f"Point Ci n°2 : (i,j)=({im.ci_points[1].i}, {im.ci_points[1].j})")
        logging.info(f"Point Ci n°3 : (i,j)=({im.ci_points[2].i}, {im.ci_points[2].j})")
        logging.info("----------------------")

        im.ds_points = sort_ds_points(self.ds_points)
        logging.info(f"Point Ds n°1 : (i,j)=({im.ds_points[0].i}, {im.ds_points[0].j})")
        logging.info(f"Point Ds n°2 : (i,j)=({im.ds_points[1].i}, {im.ds_points[1].j})")
        logging.info(f"Point Ds n°3 : (i,j)=({im.ds_points[2].i}, {im.ds_points[2].j})")
        logging.info(f"Point Ds n°4 : (i,j)=({im.ds_points[3].i}, {im.ds_points[3].j})")

        im.draw_ci_lines(self.color_ci)
        im.draw_ds_line_02(self.color_ds)
        im.draw_ds_line_02_perpendicular(self.color_ds)
        self.ci_value = compute_cubital_index(self.ci_points)
        self.ds_value = compute_discoidal_shift(im.point1, im.point2, im.ds_points)

        logging.info(f"Indice cubital Abeille #{self.NUM}) : {self.ci_value}")
        logging.info(f"Shift discoidal Abeille #{self.NUM}) : {clean(self.ds_value)}°")
        
        plt.imsave(fname=f"{self.OUT}{self.NUM}_out{self.extension}", arr=im.data)
        logging.info(f"Image sauvegardée : {self.OUT}{self.NUM}_out{self.extension}")

        self.add_infos()
        # self.write_results()
        logging.info(f"Les infos ont été ajoutées sur l'image.")
        
        img = resource_path(f"{self.OUT}{self.NUM}_out{self.extension}")
        pixmap = QPixmap(img)
        pixmap = pixmap.scaled(self.WIDTH, self.HEIGHT, Qt.KeepAspectRatio, Qt.FastTransformation)
        
        self.LAB_RIGHT[self.NUM-1].setPixmap(pixmap)

        self.close()

        # write_line(f"{self.path}{os.sep}out{os.sep}results.txt", self.num, clean(self.ci_value), clean(self.ds_value))

        ci, ds = get_ci_ds(self.ci_value, self.ds_value)

        self.LAB_RES[self.NUM-1].setText(f"     Ci : {ci}\n     Ds : {ds}°")

        self.RES[int(self.NUM)] = (clean(self.ci_value), clean(self.ds_value))

        save_results_txt(f"{self.path}{os.sep}out{os.sep}", self.RES)

        return 0

    def add_infos(self):
        img_path = resource_path(f"{self.OUT}{self.NUM}_out{self.extension}")
        img = Image.open(img_path)
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
        font_path = resource_path(f"Paul.ttf")
        font = ImageFont.truetype(font_path, size=40)
        text_color = (255, 0, 0)  # Red color

        # Position of the text
        position = (50, 25)

        # Add text to the image
        draw.text(position, text, fill=text_color, font=font)

        # Save or display the image
        img.save(f"{self.OUT}{self.NUM}_out{self.extension}")

    # def write_results(self):
    #     with open(self.path + os.sep + "out" + os.sep + "results.txt", "a") as f:
    #         ds_value = float(str(self.ds_value).replace("[", "").replace("]", ""))
    #         line = f"{self.num} {int(self.ci_value*100)/100} {int(ds_value*100)/100}\n"
    #         f.write(line)
    #     f.close()
    #     return 0

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
            A.load(self.TMP + file)
            node, node_zoom = POINT(), POINT()
            node_zoom.j, node_zoom.i = x, y
            node.j, node.i = x+xmin, y+ymin
            self.ci_points[self.count_ci_points-1] = node
            # logging.info(f"coordonnées (ligne, col) du point Ci : ({node.i}, {node.j})")
            if self.ZOOM:
                A.highlight(node_zoom, self.color_ci)
            else:
                A.highlight(node, self.color_ci)
            plt.imsave(fname=f"{self.TMP}{self.last_name[self.ZOOM]}", arr=A.data)
            pixmap = QPixmap(f"{self.TMP}{os.sep}{self.last_name[self.ZOOM]}")
            self.label.setPixmap(pixmap)
            self.setCentralWidget(self.label)
            self.setCursor(Qt.ArrowCursor)
            if self.ZOOM:
                file_wo_zoom, file_w_zoom = self.get_last_file(self.TMP)
                B = IMAGE()
                B.load(self.TMP + file_wo_zoom)
                B.highlight(node, self.color_ci)
                new_name = insertnow(self.name + f"_CI_{self.count_ci_points}" + f"_DS_{self.count_ds_points}" + self.extension)
                plt.imsave(fname=f"{self.TMP}{new_name}", arr=B.data)
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
            A.load(self.TMP + file)
            node, node_zoom = POINT(), POINT()
            node_zoom.j, node_zoom.i = x, y
            node.j, node.i = x+xmin, y+ymin
            # logging.info(f"coordonnées (ligne, col) du point Ds : ({node.i}, {node.j})")
            self.ds_points[self.count_ds_points-1] = node
            if self.ZOOM:
                A.highlight(node_zoom, self.color_ds)
            else:
                A.highlight(node, self.color_ds)

            A.highlight(node, self.color_ds)
            plt.imsave(fname=f"{self.TMP}{self.last_name[self.ZOOM]}", arr=A.data)
            pixmap = QPixmap(f"{self.TMP}{os.sep}{self.last_name[self.ZOOM]}")
            self.label.setPixmap(pixmap)
            self.setCentralWidget(self.label)
            self.setCursor(Qt.ArrowCursor)
            if self.ZOOM:
                file_wo_zoom, file_w_zoom = self.get_last_file(self.TMP)
                B = IMAGE()
                B.load(self.TMP + file_wo_zoom)
                B.highlight(node, self.color_ds)
                new_name = insertnow(self.name + f"_CI_{self.count_ci_points}" + f"_DS_{self.count_ds_points}" + self.extension)
                plt.imsave(fname=f"{self.TMP}{new_name}", arr=B.data)
            
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
        last_file_wo_zoom, last_file_w_zoom = self.get_last_file(path=self.TMP)
        os.remove(self.TMP + last_file_wo_zoom)
        try:
            os.remove(self.TMP + last_file_w_zoom)
        except:
            pass
        last_file_wo_zoom, last_file_w_zoom = self.get_last_file(path=self.TMP)
        self.last_name[0] = last_file_wo_zoom
        self.last_name[1] = last_file_w_zoom

        pixmap = QPixmap(f"{self.TMP}{os.sep}{self.last_name[self.ZOOM]}")
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
        file_wo_zoom, file_w_zoom = self.get_last_file(self.TMP)
        self.ZOOM = ZOOM
        zm = resource_path(f"search.png")
        pixmap = QPixmap(zm)
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
        last_file_wo_zoom, last_file_w_zoom = self.get_last_file(path=self.TMP)
        pixmap = QPixmap(self.TMP + last_file_wo_zoom)
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

            file_wo_zoom, file_w_zoom = self.get_last_file(self.TMP)

            A = IMAGE()
            A.load(self.TMP + file_wo_zoom)
            
            j_min = max(x-zoom_x//2, 0)
            j_max = min(x+zoom_x//2, A.data.shape[1])

            i_min = max(y-zoom_y//2, 0)
            i_max = min(y+zoom_y//2, A.data.shape[0])

            image_temp = A.data[i_min:i_max, j_min:j_max, :]

            new_name = insertnow(self.name + "_zoom_" + f"xmin{j_min}xmax{j_max}ymin{i_min}ymax{i_max}end" + self.extension)
            self.last_name[self.ZOOM] = new_name

            plt.imsave(fname=f"{self.TMP}{new_name}", arr=image_temp)

            pixmap = QPixmap(f"{self.TMP}{os.sep}{new_name}")

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


class VISU(QMainWindow):
    def __init__(self):
        super(VISU, self).__init__()

    def display(self, path_to_image):
        self.setWindowTitle(' ')
        self.label = QLabel(self)
        pixmap = QPixmap(path_to_image)

        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)

        self.pixmapWidth = pixmap.width()
        self.pixmapHeight = pixmap.height()

        coeff = 0.83
        self.label.setFixedSize(int(self.pixmapWidth*coeff), int(self.pixmapHeight*coeff))

        self.label.setScaledContents(True)
        self.move(50, 50)
        self.show()