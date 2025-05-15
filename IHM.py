import sys
import os
import shutil
import zipfile
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QSizePolicy,
    QTabWidget,
    QDockWidget,
    QLineEdit,
    QFileDialog,
    QInputDialog
)
from PyQt5.QtGui import QPixmap, QCursor, QFont

from PyQt5 import QtCore, QtGui

from functools import partial

from PIL import Image, ImageDraw, ImageFont

from buttons_edit import *
from buttons_visu import *
from buttons_browse import *
from ci_and_ds_tools import *
from utile import *
from analyses import *


connections_edit = {1:editFile1, 2:editFile2, 3:editFile3, 4:editFile4, 5:editFile5,
                    6:editFile6, 7:editFile7, 8:editFile8, 9:editFile9, 10:editFile10,
                    11:editFile11, 12:editFile12, 13:editFile13, 14:editFile14, 15:editFile15,
                    16:editFile16, 17:editFile17, 18:editFile18, 19:editFile19, 20:editFile20,
                    21:editFile21, 22:editFile22, 23:editFile23, 24:editFile24, 25:editFile25,
                    26:editFile26, 27:editFile27, 28:editFile28, 29:editFile29, 30:editFile30,
                    31:editFile31, 32:editFile32, 33:editFile33, 34:editFile34, 35:editFile35,
                    36:editFile36, 37:editFile37, 38:editFile38, 39:editFile39, 40:editFile40,
                    41:editFile41, 42:editFile42, 43:editFile43, 44:editFile44, 45:editFile45,
                    46:editFile46, 47:editFile37, 48:editFile48, 49:editFile49, 50:editFile50}

connections_visu = {1:visu1, 2:visu2, 3:visu3, 4:visu4, 5:visu5,
                       6:visu6, 7:visu7, 8:visu8, 9:visu9, 10:visu10,
                       11:visu11, 12:visu12, 13:visu13, 14:visu14, 15:visu15,
                       16:visu16, 17:visu17, 18:visu18, 19:visu19, 20:visu20,
                       21:visu21, 22:visu22, 23:visu23, 24:visu24, 25:visu25,
                       26:visu26, 27:visu27, 28:visu28, 29:visu29, 30:visu30,
                       31:visu31, 32:visu32, 33:visu33, 34:visu34, 35:visu35,
                       36:visu36, 37:visu37, 38:visu38, 39:visu39, 40:visu40}

connections_load = {1:browseFile1, 2:browseFile2, 3:browseFile3, 4:browseFile4, 5:browseFile5,
                       6:browseFile6, 7:browseFile7, 8:browseFile8, 9:browseFile9, 10:browseFile10,
                       11:browseFile11, 12:browseFile12, 13:browseFile13, 14:browseFile14, 15:browseFile15,
                       16:browseFile16, 17:browseFile17, 18:browseFile18, 19:browseFile19, 20:browseFile20,
                       21:browseFile21, 22:browseFile22, 23:browseFile23, 24:browseFile24, 25:browseFile25,
                       26:browseFile26, 27:browseFile27, 28:browseFile28, 29:browseFile29, 30:browseFile30,
                       31:browseFile31, 32:browseFile32, 33:browseFile33, 34:browseFile34, 35:browseFile35,
                       36:browseFile36, 37:browseFile37, 38:browseFile38, 39:browseFile39, 40:browseFile40}

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


class MESSAGE(QMainWindow):
    def __init__(self):
        super(MESSAGE, self).__init__()
        self.error1 = "Veuillez d'abord charger une \nimage avant de l'éditer..."
        self.error2 = "Veuillez d'abord éditer \nune image..."

    def message_erreur1(self):
        self.setWindowTitle(' ')
        layout = QVBoxLayout()
        pixmap = QPixmap(f"images" + os.sep + "coconfort.png")
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
        pixmap = QPixmap(f"images" + os.sep + "aspicot.png")
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


    def display(self, fileName):

        self.name = get_file_name(fileName).replace(".jpg", "").replace("png", "")
        self.extension = "." + fileName.split(".")[-1]
        self.path = get_path(fileName)

        # self.tmp = "tmp" + os.sep + self.num + os.sep
        # self.out = "out" + os.sep + self.num + os.sep

        self.tmp = self.path + os.sep + "tmp" + os.sep + self.num + os.sep
        self.out = self.path + os.sep + "out" + os.sep

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
            shutil.copyfile(fileName, self.tmp + self.last_name[self.ZOOM])
            
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


    # def display_error_message(self, error_msg):
    #     print("display error message")
    #     self.move(600, 300)
    #     # self.w = QVBoxLayout()
    #     pixmap = QPixmap(f"images" + os.sep + "coconfort.png")
    #     self.label = QLabel()
    #     self.label.setPixmap(pixmap)
    #     # self.w.addWidget(self.label)
    #     # txt = QLabel(error_msg)
    #     # txt.setFont(QFont('Times', 13))
    #     # self.w.addWidget(txt)
    #     # self.w.setLayout(self.layout)

    #     self.label.setFixedSize(300, 300)
    #     self.setCentralWidget(self.label)
    #     # self.setFixedWidth(300)
    #     # self.setFixedHeight(300)
    #     # self.label.setScaledContents(True)

    #     # self.set_dock()

    #     self.show()

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
        im.load(f"{self.tmp}{file_wo_zoom}")
        im.ci_points = sort_ci_points(self.ci_points)
        im.ds_points = sort_ds_points(self.ds_points)
        im.draw_ci_lines(self.color_ci)
        im.draw_ds_line_02(self.color_ds)
        im.draw_ds_line_02_perpendicular(self.color_ds)
        self.ci_value = compute_cubital_index(self.ci_points)
        self.ds_value = compute_discoidal_shift(im.point1, im.point2, im.ds_points)
        # im.customize()
        # shutil.copyfile(f"{self.path}{self.tmp}{file_wo_zoom}", f"{self.path}{self.out}{file_wo_zoom}")

        # try:
        #     for filename in os.listdir(f"{self.out}"):
        #         file_path = self.out + os.sep + filename
        #         os.unlink(file_path)
        #         print(f"suppression du fichier {file_path}")
        # except:
        #     pass
        
        plt.imsave(fname=f"{self.out}{self.NUM}_out{self.extension}", arr=im.data)
        self.add_infos()
        # self.write_results()
        
        pixmap = QPixmap(f"{self.out}{self.NUM}_out{self.extension}")
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
        img = Image.open(f"{self.out}{self.NUM}_out{self.extension}")
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
        img.save(f"{self.out}{self.NUM}_out{self.extension}")

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
        os.remove(self.tmp + last_file_wo_zoom)
        try:
            os.remove(self.tmp + last_file_w_zoom)
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
        file_wo_zoom, file_w_zoom = self.get_last_file(self.tmp)
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
        pixmap = QPixmap(self.tmp + last_file_wo_zoom)
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

            file_wo_zoom, file_w_zoom = self.get_last_file(self.tmp)

            A = IMAGE()
            A.load(self.tmp + file_wo_zoom)
            
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
            print("Le dossier 'out' existe déjà")

        try:
            os.makedirs("in")
        except:
            print("Le dossier 'in' existe déjà")

        try:
            os.makedirs("tmp")
        except:
            print("Le dossier 'tmp' existe déjà")

        self.out = os.path.abspath(os.getcwd()) + os.sep + "out"
        self.in_ = os.path.abspath(os.getcwd()) + os.sep + "in"
        self.tmp = os.path.abspath(os.getcwd()) + os.sep + "tmp"
        self.path = os.path.abspath(os.getcwd())

        # for filename in os.listdir(self.path):
        #     file_path = self.path + os.sep + filename
        #     try:
        #         if os.path.isfile(file_path):
        #             os.unlink(file_path)
        #         elif os.path.isdir(file_path):
        #             shutil.rmtree(file_path)
        #     except Exception as e:
        #         print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        print(f"nettoyage du dossier 'tmp' : {self.tmp}")
        for filename in os.listdir(self.tmp):
            file_path = self.tmp + os.sep + filename
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"suppression du fichier {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"suppression du dossier {file_path}")
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        print(f"nettoyage du dossier 'in' : {self.in_}")
        for filename in os.listdir(self.in_):
            file_path = self.in_ + os.sep + filename
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"suppression du fichier {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"suppression du dossier {file_path}")
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


        print(f"nettoyage du dossier 'out' : {self.out}")
        for filename in os.listdir(self.out):
            file_path = self.out + os.sep + filename
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"suppression du fichier {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"suppression du dossier {file_path}")
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        with open(self.out + os.sep + "results.txt", "w") as f:
            line = f"num indice_cubital angle_discoidal\n"
            f.write(line)
            f.close

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

        self.path = path
        self.in_ = path + os.sep + "in"
        self.out = path + os.sep + "out"
        self.tmp = path + os.sep + "tmp"

        self.RES = {}
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
        self.fileName21 = "im21.png"
        self.fileName22 = "im22.png"
        self.fileName23 = "im23.png"
        self.fileName24 = "im24.png"
        self.fileName25 = "im25.png"
        self.fileName26 = "im26.png"
        self.fileName27 = "im27.png"
        self.fileName28 = "im28.png"
        self.fileName29 = "im29.png"
        self.fileName30 = "im30.png"
        self.fileName31 = "im31.png"
        self.fileName32 = "im32.png"
        self.fileName33 = "im33.png"
        self.fileName34 = "im34.png"
        self.fileName35 = "im35.png"
        self.fileName36 = "im36.png"
        self.fileName37 = "im37.png"
        self.fileName38 = "im38.png"
        self.fileName39 = "im39.png"
        self.fileName40 = "im40.png"
        self.fileName41 = "im41.png"
        self.fileName42 = "im42.png"
        self.fileName43 = "im43.png"
        self.fileName44 = "im44.png"
        self.fileName45 = "im45.png"
        self.fileName46 = "im46.png"
        self.fileName47 = "im47.png"
        self.fileName48 = "im48.png"
        self.fileName49 = "im49.png"
        self.fileName50 = "im50.png"

        # self.fileNames = [self.fileName1, self.fileName2, self.fileName3, self.fileName4, self.fileName5,
        #                   self.fileName6, self.fileName7, self.fileName8, self.fileName9, self.fileName10,
        #                   self.fileName11, self.fileName12, self.fileName13, self.fileName14, self.fileName15,
        #                   self.fileName16, self.fileName17, self.fileName18, self.fileName19, self.fileName20,
        #                   self.fileName21, self.fileName22, self.fileName23, self.fileName24, self.fileName25,
        #                   self.fileName26, self.fileName27, self.fileName28, self.fileName29, self.fileName30,
        #                   self.fileName31, self.fileName32, self.fileName33, self.fileName34, self.fileName35,
        #                   self.fileName36, self.fileName37, self.fileName38, self.fileName39, self.fileName40,
        #                   self.fileName41, self.fileName42, self.fileName43, self.fileName44, self.fileName45,
        #                   self.fileName46, self.fileName47, self.fileName48, self.fileName49, self.fileName50]


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

        mf = QFont("Times New Roman", 14)

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

        self.tabs.setFont(QFont('Times', 13))

        self.width = 413
        self.height = 307

        nb_tabs = 8

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
        
        self.label_results = [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self),
                           QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)]

        layout_main = QGridLayout()
        btn1 = QPushButton("Charger \nune analyse")
        self.btn2 = QPushButton(f"Sauvegarder \nl'analyse\n{self.analyse_name}")
        self.btn3 = QPushButton(f"Lancer \nl'analyse\n{self.analyse_name}")
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
        self.btn2.setFont(my_font3)
        self.btn3.setFont(my_font3)

        self.btn2.setStyleSheet("QPushButton {background-color: plum}")
        self.btn3.setStyleSheet("QPushButton {background-color: lightblue}")

        # label1.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px;");

        btn1.resize(150, 150)
        btn1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btn2.resize(150, 150)
        self.btn2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.btn3.resize(150, 150)
        self.btn3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.pb.resize(150, 150)
        self.pb.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        pixmap = QPixmap(f"images{os.sep}empty1.png")
        # pixmap = QPixmap(f"images{os.sep}carte_dardagnan.png")
        image_empty1 = QLabel()
        image_empty1.setPixmap(pixmap)

        pixmap = QPixmap(f"images{os.sep}empty2.png")
        # pixmap = QPixmap(f"images{os.sep}dardagnan2.png")
        image_empty2 = QLabel()
        image_empty2.setPixmap(pixmap)

        pixmap = QPixmap(f"images{os.sep}carte_dardagnan2.png")
        pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        # pixmap = QPixmap(f"images{os.sep}dardagnan2.png")
        deco0 = QLabel()
        deco0.setPixmap(pixmap)

        pixmap = QPixmap(f"images{os.sep}carte_dardagnan1.png")
        pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        # pixmap = QPixmap(f"images{os.sep}dardagnan2.png")
        deco1 = QLabel()
        deco1.setPixmap(pixmap)

        pixmap = QPixmap(f"images{os.sep}carte_dardagnan3.png")
        pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        # pixmap = QPixmap(f"images{os.sep}dardagnan2.png")
        deco2 = QLabel()
        deco2.setPixmap(pixmap)

        # deco.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout_main.addWidget(label0, 0, 0, 1, 2)
        # layout_main.addWidget(self.edit_analyse_name, 0, 1, 1, 2)
        layout_main.addWidget(self.label00, 0, 1, 1, 2)
        layout_main.addWidget(self.pb, 0, 2, 1, 1)
        layout_main.addWidget(btn1, 1, 0, 2, 2)
        layout_main.addWidget(self.btn2, 1, 1, 2, 2)
        layout_main.addWidget(self.btn3, 1, 2, 2, 2)
        layout_main.addWidget(label1, 3, 0, 1, 5)
        layout_main.addWidget(label2, 3, 7, 1, 5)
        layout_main.addWidget(image_empty1, 4, 0, 5, 5)
        layout_main.addWidget(image_empty2, 4, 7, 5, 5)
        layout_main.addWidget(deco0, 0, 4, 2, 2)
        layout_main.addWidget(deco1, 0, 8, 2, 2)
        layout_main.addWidget(deco2, 0, 10, 2, 2)

        btn1.clicked.connect(self.load_project)
        self.btn2.clicked.connect(self.save_project)

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

                # self.label_results = QLabel()
                label_results = self.label_results[num_image-1]
                label_results.setText("     Ci : \n     Ds :")
                self.grids[-1].addWidget(label_results, i, 6, 1, 1)

                btn1 = QPushButton("Load")
                btn1.resize(50, 150)
                btn1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                
                btn2 = QPushButton("Edit")
                btn2.resize(50, 150)
                btn2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                btn3 = QPushButton("Visualize")
                btn3.resize(50, 150)
                btn3.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

                self.grids[-1].addWidget(btn1, i, 1)
                self.grids[-1].addWidget(btn2, i, 3)
                self.grids[-1].addWidget(btn3, i, 5)
                
                btn1.clicked.connect(partial(connections_load[num_image], TAB=self))
                btn2.clicked.connect(partial(connections_edit[num_image], TAB=self))
                btn3.clicked.connect(partial(connections_visu[num_image], TAB=self))

                pixmap = QPixmap(f"images{os.sep}dardagnan.png")
                darda = QLabel()
                darda.setPixmap(pixmap)
                self.grids[-1].addWidget(darda, i, 7)

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

        # Create fifth tab 
        self.tab5.layout = self.grids[4]
        self.tab5.setLayout(self.tab5.layout)

        # Create sixth tab 
        self.tab6.layout = self.grids[5]
        self.tab6.setLayout(self.tab6.layout)

        # Create seventh tab 
        self.tab7.layout = self.grids[6]
        self.tab7.setLayout(self.tab7.layout)

        # Create eighth tab 
        self.tab8.layout = self.grids[7]
        self.tab8.setLayout(self.tab8.layout)

        # Final step
        # #######
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def edit_name(self):
        text, okPressed = QInputDialog.getText(self, " ", "Entrer le nom de l'analyse :", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.analyse_name = text
            self.label00.setText(text)
            self.btn2.setText(f"Sauvegarder\nl'analyse\n{self.analyse_name}")
            self.btn3.setText(f"Lancer\nl'analyse\n{self.analyse_name}")
        return 0


    def save_project(self):
        DIR = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if DIR != "":
            with zipfile.ZipFile(DIR + os.sep + self.analyse_name + '.zip', "w") as zf:
                for root, _, filenames in os.walk(os.path.basename(self.out)):
                    for name in filenames:
                        name = os.path.join(root, name)
                        name = os.path.normpath(name)
                        zf.write(name, name)
                for root, _, filenames in os.walk(os.path.basename(self.in_)):
                    for name in filenames:
                        name = os.path.join(root, name)
                        name = os.path.normpath(name)
                        zf.write(name, name)
            self.dialog = MESSAGE()
            msg = f"L'analyse '{self.analyse_name}' a bien été enregistrée dans {DIR}"
            self.dialog.message(msg)
            self.dialog.show()
        else:
            pass
        return 0
    
    def load_project(self):
        DIR = QFileDialog.getOpenFileName(self, "Select a .zip project file")
        if DIR[0] != "":
            project_file = str(DIR[0])

            self.analyse_name = get_file_name(project_file)
            self.label00.setText(self.analyse_name)
            self.btn2.setText(f"Sauvegarder\nl'analyse\n{self.analyse_name}")
            self.btn3.setText(f"Lancer\nl'analyse\n{self.analyse_name}")
            
            shutil.unpack_archive(filename=project_file, extract_dir=self.tmp)
            copytree(src=self.tmp + os.sep + "out", dst=self.out)

            self.RES = load_results(self.tmp + os.sep + "out" + os.sep + "results.txt")
            print("results already computed:")
            print(self.RES)
                    
            for file in os.listdir(self.in_):
                num_abeille = int(file.split(".")[0])
                print(num_abeille)
                if num_abeille not in self.RES.keys():
                    print(f"Attention : l'abeille {num_abeille} n'a pas été trouvée dans le fichier de résultats")
                else:
                    ff_in = self.in_ + os.sep + file
                    pixmap = QPixmap(ff_in)
                    pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
                    self.label_left[num_abeille-1].setPixmap(pixmap)
                    # attention mieux gérer l'extension du fichier qui n'est pas forcément en .jpg
                    ff_out = self.out + os.sep + str(num_abeille) + os.sep + file.replace(".png", "_out.jpg") 
                    self.label_left[num_abeille-1].setPixmap(pixmap)
                    pixmap_out = QPixmap(ff_out)
                    pixmap_out = pixmap_out.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
                    self.label_right[num_abeille-1].setPixmap(pixmap_out)
                    # self.fileNames[num_abeille-1] = file
                    print(ff_in, ff_out)

        else:
            pass
        return 0

if __name__ == '__main__':
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