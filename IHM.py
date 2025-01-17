from images import *
import matplotlib.pyplot as plt

import sys
import os

from datetime import datetime

import shutil

from PyQt5.QtCore import Qt, QSize, QTimer
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
    QMessageBox
)
from PyQt5.QtGui import QPixmap, QCursor, QFont

from PyQt5.QtGui import QPainter, QColor, QCloseEvent
from PyQt5 import QtCore, QtGui, QtWidgets

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

class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        self.setWindowTitle("Fenêtre d'édition")
        self.windowSize = QSize(int(640*2.8), int(480*2.8))
        self.move(100, 100)

        self.zoom_power = (270, 200)

        self.w = QWidget()
        self.layout = QVBoxLayout(self.w)

    def display(self, fileName):

        self.name = get_file_name(fileName).replace(".jpg", "").replace("png", "")
        self.extension = "." + fileName.split(".")[-1]
        self.path = get_path(fileName)

        self.path2image = fileName

        self.out = "out" + os.sep + self.name + os.sep

        try:
            os.makedirs("out" + os.sep + self.name)
        except:
            pass

        try:
            shutil.copyfile(fileName, insertnow(self.path + self.out + self.name + self.extension))
        except:
            pass

        self.label = QLabel(self)
        pixmap = QPixmap(fileName)
        scaled_pixmap = pixmap.scaled(self.windowSize, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

        self.label.setPixmap(scaled_pixmap)
        self.setCentralWidget(self.label)

        self.set_dock()
    
    def set_dock(self):
        btn_zoom_1 = QPushButton("  ZOOM IN ")
        # btn_zoom_1.resize(400, 400)
        btn_zoom_1.setIcon(QtGui.QIcon(f"images{os.sep}search.png"))
        btn_zoom_1.setFont(QFont('Times', 14))
        btn_zoom_1.clicked.connect(self.zoom_in)

        btn_zoom_2 = QPushButton("  ZOOM OUT")
        # btn_zoom_2.resize(400, 400)
        btn_zoom_2.setIcon(QtGui.QIcon(f"images{os.sep}earth.png"))
        btn_zoom_2.setFont(QFont('Times', 14))
        btn_zoom_2.clicked.connect(self.zoom_out)

        btn_ci_points = QPushButton("Add CI points")
        btn_ci_points.setFont(QFont('Times', 14))
        btn_ci_points.clicked.connect(self.set_ci_points)

        self.layout.addWidget(btn_zoom_1)
        self.layout.addWidget(btn_zoom_2)
        self.layout.addWidget(btn_ci_points)
        self.dock = QDockWidget(f"{self.name}{self.extension}", self)
        self.dock.setFeatures(QDockWidget.DockWidgetMovable)
        # self.dock.setStyleSheet("QDockWidget {background : }")
        self.dock.setWidget(self.w)

    def set_ci_points(self):
        # Set the cursor to a cross cursor
        self.setCursor(Qt.CrossCursor)

        A = IMAGE()
        A.load(self.file)
    
    def zoom_in(self):
        pixmap = QPixmap(f"images{os.sep}search.png")
        pixmap = pixmap.scaled(32, 32)
        cursor = QCursor(pixmap, 32, 32)
        # QApplication.setOverrideCursor(cursor)
        self.setCursor(cursor)

        pixmap = QPixmap(self.path2image)

        self.label.mousePressEvent = self.getPos_and_zoom
        
        return 0

    def zoom_out(self):

        file_out =  os.listdir(self.out)[0].replace(self.extension, "")
        tmp = file_out.split("___")

        date0 = tmp[-2].replace("_", "/")
        hour0 = tmp[-1].replace("_", ":")
        time0 =  datetime.strptime("01/01/2000 00:00:00", "%d/%m/%Y %H:%M:%S")

        for file in os.listdir(self.out):
            if "zoom" in file:
                continue
            else:
                tmp = file.replace(self.extension, "").split("___")
                date0 = tmp[-2].replace("_", "/")
                hour0 = tmp[-1].replace("_", ":")
                time1 = datetime.strptime(date0 + " " + hour0, "%d/%m/%Y %H:%M:%S")
                if time1 >= time0:
                    time0 = time1
                    file_out = file
                else:
                    continue

        
        # self.display(self.path + self.out + file_out)
        

        pixmap = QPixmap(self.path + self.out + file_out)
        scaled_pixmap = pixmap.scaled(self.windowSize, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

        self.label.setPixmap(scaled_pixmap)
        self.setCentralWidget(self.label)
        # self.set_dock()
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

    def getPos_and_zoom(self , event):
        
        print("get_pos_and_zoom")
        
        delta_x = self.zoom_power[1]
        delta_y = self.zoom_power[0]

        x = event.pos().x()
        y = event.pos().y()

        A = IMAGE()
        A.load(self.path2image)

        i_max = min(y+delta_y, A.data.shape[0])
        i_min = max(y-delta_y, 0)

        j_max = min(x+delta_x, A.data.shape[1])
        j_min = max(x-delta_x, 0)

        image_temp = A.data[i_min:i_max, j_min:x+j_max, :]

        new_name = insertnow(self.name + "_" + "zoom" + self.extension)

        plt.imsave(fname=f"{self.out}{new_name}", arr=image_temp)

        pixmap = QPixmap(f"{self.out}{os.sep}{new_name}")
        # scaled_pixmap = pixmap.scaled(QSize(delta_y*3, delta_x*3), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        scaled_pixmap = pixmap.scaled(self.windowSize, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

        self.label.setPixmap(scaled_pixmap)
        self.setCentralWidget(self.label)

        cursor = QCursor(Qt.ArrowCursor)
        self.setCursor(cursor)


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analyse des ailes d'abeilles")

        self.tab_widget = Tab(self)
        self.setCentralWidget(self.tab_widget)
    
        self.showMaximized()

        QTimer.singleShot(100, self.calculate)

        try:
            os.makedirs("out")
        except:
            pass

    def calculate(self):
        return self.frameGeometry().height()

    def close_all_windows(self):
        win_list = QApplication.allWindows()
        for w in win_list:
            w.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        close = QMessageBox()
        close.setText("Voulez vous vraiment quitter l'application ?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
            self.close_all_windows()
        else:
            event.ignore()


class Tab(QWidget): 
    def __init__(self, parent): 
        super(QWidget, self).__init__(parent)

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

        # self.tabs.resize(300, 200)
  
        # Add tabs 
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
        
        self.dialog = [Second(self), Second(self), Second(self), Second(self), Second(self),
                        Second(self), Second(self), Second(self), Second(self), Second(self),
                        Second(self), Second(self), Second(self), Second(self), Second(self)]

        connections_load = {1:self.browseFile1, 2:self.browseFile2, 3:self.browseFile3, 4:self.browseFile4, 5:self.browseFile5,
                       6:self.browseFile6, 7:self.browseFile7, 8:self.browseFile8, 9:self.browseFile9, 10:self.browseFile10,
                       11:self.browseFile11, 12:self.browseFile12, 13:self.browseFile13, 14:self.browseFile14, 15:self.browseFile15,
                       16:self.browseFile16, 17:self.browseFile17, 18:self.browseFile18, 19:self.browseFile19, 20:self.browseFile20}
        
        connections_edit = {1:self.editFile1, 2:self.editFile2, 3:self.editFile3, 4:self.editFile4, 5:self.editFile5,
                       6:self.editFile6, 7:self.editFile7, 8:self.editFile8, 9:self.editFile9, 10:self.editFile10,
                       11:self.editFile11, 12:self.editFile12, 13:self.editFile13, 14:self.editFile14, 15:self.editFile15,
                       16:self.editFile16, 17:self.editFile17, 18:self.editFile18, 19:self.editFile19, 20:self.editFile20}

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

                # self.grids[-1].addWidget(btn1, i, 1, alignment=QtCore.Qt.AlignLeft)
                # self.grids[-1].addWidget(btn2, i, 2, alignment=QtCore.Qt.AlignCenter)
                self.grids[-1].addWidget(btn1, i, 1)
                self.grids[-1].addWidget(btn2, i, 3)
                

                btn1.clicked.connect(connections_load[num_image])
                btn2.clicked.connect(connections_edit[num_image])

                pixmap = QPixmap(f"images{os.sep}dardagnan.png")
                label = QLabel()
                label.setPixmap(pixmap)
                self.grids[-1].addWidget(label, i, 5)

                pixmap = QPixmap(f"images{os.sep}dardagnan.png")
                aaa = QLabel()
                aaa.setPixmap(pixmap)
                self.grids[-1].addWidget(aaa, i, 6)

                # self.grids[-1].addWidget(label_right, i, 3)

        # Create first tab 
        self.tab1.layout = self.grids[0]
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab 
        self.tab2.layout = self.grids[1]
        self.tab2.setLayout(self.tab2.layout)

        # Create third tab 
        self.tab3.layout = self.grids[2]
        self.tab3.setLayout(self.tab3.layout)

        # Create fourth tab 
        self.tab4.layout = self.grids[3]
        self.tab4.setLayout(self.tab4.layout)

        # Final step
        # #######
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    def editFile1(self):
        if self.fileName1 == "im1.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName1)
        self.dialog.show()
        
    def editFile2(self):
        if self.fileName2 == "im2.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName2)
        self.dialog.show()
    
    def editFile3(self):
        if self.fileName3 == "im3.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName3)
        self.dialog.show()
    
    def editFile4(self):
        if self.fileName4 == "im4.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName4)
        self.dialog.show()

    def editFile5(self):
        if self.fileName5 == "im5.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName5)
        self.dialog.show()
    
    def editFile6(self):
        if self.fileName6 == "im6.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName6)
        self.dialog.show()
    
    def editFile7(self):
        if self.fileName7 == "im7.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName7)
        self.dialog.show()
    
    def editFile8(self):
        if self.fileName8 == "im8.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName8)
        self.dialog.show()
    
    def editFile9(self):
        if self.fileName9 == "im9.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName8)
        self.dialog.show()
    
    def editFile10(self):
        if self.fileName10 == "im10.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName10)
        self.dialog.show()

    def editFile11(self):
        if self.fileName11 == "im11.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName11)
        self.dialog.show()

    def editFile12(self):
        if self.fileName12 == "im12.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName12)
        self.dialog.show()

    def editFile13(self):
        if self.fileName13 == "im13.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName13)
        self.dialog.show()

    def editFile14(self):
        if self.fileName14 == "im14.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName14)
        self.dialog.show()
    
    def editFile15(self):
        if self.fileName15 == "im15.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName15)
        self.dialog.show()

    def editFile16(self):
        if self.fileName16 == "im16.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName16)
        self.dialog.show()

    def editFile17(self):
        if self.fileName17 == "im17.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName17)
        self.dialog.show()
    
    def editFile18(self):
        if self.fileName18 == "im18.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName18)
        self.dialog.show()

    def editFile19(self):
        if self.fileName18 == "im19.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
            self.dialog.display(self.fileName19)
        self.dialog.show()
    
    def editFile20(self):
        if self.fileName18 == "im20.png":
            self.dialog = Second()
            self.dialog.display_error_message()
        else:
            self.dialog = Second()
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

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()