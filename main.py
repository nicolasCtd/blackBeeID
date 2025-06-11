import sys
import os
import shutil
import zipfile
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCloseEvent
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
    QInputDialog,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap, QCursor, QFont

from PyQt5 import QtCore, QtGui

from functools import partial

from PIL import Image, ImageDraw, ImageFont

from modules.buttons_edit import *
from modules.buttons_visu import *
from modules.buttons_browse import *
from modules.ci_and_ds_tools import *
from modules.utile import *
from modules.analyses import *

import sys

import logging

# Définir une fonction pour attraper toutes les exceptions non gérées
def log_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Laisse le Ctrl+C s'afficher normalement
        sys._excepthook_(exc_type, exc_value, exc_traceback)
        return
    # Log complet de l'erreur avec stack trace
    logging.error("Exception non gérée :", exc_info=(exc_type, exc_value, exc_traceback))

# Remplacer le hook d'exception
sys.excepthook = log_exception

def resource_path(relative_path):
    """Retourne le chemin absolu, même si l'app est empaquetée avec PyInstaller"""
    if getattr(sys, 'frozen', False):
        # PyInstaller utilise ce répertoire temporaire
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Script normal
        return os.path.join(os.path.dirname(__file__), relative_path)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

config_path = resource_path('config.yml')

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

classif = config['visu']

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


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Abeille noire?")

        self.out = os.path.abspath(os.getcwd()) + os.sep + "out"
        self.in_ = os.path.abspath(os.getcwd()) + os.sep + "in"
        self.tmp = os.path.abspath(os.getcwd()) + os.sep + "tmp"
        self.path = os.path.abspath(os.getcwd())

        logging.basicConfig(
            filename= self.out + os.sep + 'logs.log',
            filemode="w",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info("Démarrage du programme")

        if os.path.isdir(self.out):
            print(f"nettoyage du dossier 'out' : {self.out}")
            logging.info(f"nettoyage du dossier 'out' : {self.out}")
            for filename in os.listdir(self.out):
                file_path = self.out + os.sep + filename
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        print(f"suppression du fichier {file_path}")
                        logging.info(f"suppression du fichier {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"suppression du dossier {file_path}")
                        logging.info(f"suppression du dossier {file_path}")
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                    logging.info('Failed to delete %s. Reason: %s' % (file_path, e))
        else:
            logging.info(f"Création du répertoire de sortie : {self.out}")
            os.makedirs("out")

        if os.path.isdir(self.in_):
            print(f"nettoyage du dossier 'in' : {self.in_}")
            logging.info(f"nettoyage du dossier 'in' : {self.in_}")
            for filename in os.listdir(self.in_):
                file_path = self.in_ + os.sep + filename
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        print(f"suppression du fichier {file_path}")
                        logging.info(f"suppression du fichier {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"suppression du dossier {file_path}")
                        logging.info(f"suppression du dossier {file_path}")
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                    logging.info('Failed to delete %s. Reason: %s' % (file_path, e))
        else:
            logging.info(f"Création du répertoire d'entrée : {self.in_}")
            os.makedirs("in")

        if os.path.isdir(self.tmp):
            print(f"nettoyage du dossier 'tmp' : {self.tmp}")
            logging.info(f"nettoyage du dossier 'tmp' : {self.tmp}")
            for filename in os.listdir(self.tmp):
                file_path = self.tmp + os.sep + filename
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        print(f"suppression du fichier {file_path}")
                        logging.info(f"suppression du fichier {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"suppression du dossier {file_path}")
                        logging.info(f"suppression du fichier {file_path}")
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                    logging.info('Failed to delete %s. Reason: %s' % (file_path, e))
        else:
            logging.info(f"Création du répertoire où sont stockés les fichiers temporaires : {self.tmp}")
            os.makedirs("tmp")

        with open(self.out + os.sep + "results.txt", "w") as f:
            p = self.out + os.sep + "results.txt"
            print(f"Les résultats seront écrits dans {p}")
            logging.info(f"Génération du fichier de résultats {p}")
            line = f"num indice_cubital angle_discoidal\n"
            f.write(line)
            f.close

        self.tab_widget = Tab(self, self.path)
        self.setCentralWidget(self.tab_widget)
    
        self.showMaximized()

    #     QTimer.singleShot(100, self.calculate)

    # def calculate(self):
    #     return self.frameGeometry().height()

    def close_all_windows(self):
        win_list = QApplication.allWindows()
        for w in win_list:
            w.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        close = QMessageBox()
        close.setText("Voulez vous quitter l'application ?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close.setWindowTitle(" ")
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
            self.close_all_windows()
        else:
            event.ignore()


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
        self.tabs.setCurrentIndex(1)

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
        
        self.label_analyses = [QLabel(self), QLabel(self)]
        self.label_analyses[0].setFixedWidth(900)
        self.label_analyses[0].setFixedHeight(850)

        self.label_analyses[1].setFixedWidth(900)
        self.label_analyses[1].setFixedHeight(850)

        layout_main = QGridLayout()
        btn1 = QPushButton("Charger\nune analyse")
        self.btn2 = QPushButton(f"Sauvegarder\nl'analyse\n{self.analyse_name}")
        self.btn3 = QPushButton(f"Lancer\nl'analyse\n{self.analyse_name}")
        label0 = QLabel("Nom de l'analyse : ")
        self.label00 = QLabel(self.analyse_name)
        label1 = QLabel(f">>  <u> Histogramme de l'Indice Cubital (classification {classif.upper()})<u>")
        label2 = QLabel(">>  <u> Indice Cubital vs Discoidal shift<u>")
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

        empty1 = resource_path(f"images{os.sep}empty1.png")
        pixmap = QPixmap(empty1)
        # pixmap = QPixmap(f"images{os.sep}carte_dardagnan.png")
        image_empty1 = self.label_analyses[0]
        image_empty1.setPixmap(pixmap)

        empty2 = resource_path(f"images{os.sep}empty2.png")
        pixmap = QPixmap(empty2)
        # pixmap = QPixmap(f"images{os.sep}dardagnan2.png")
        image_empty2 = self.label_analyses[1]
        image_empty2.setPixmap(pixmap)

        cd2 = resource_path(f"images{os.sep}carte_dardagnan2.png")
        pixmap = QPixmap(cd2)
        deco0 = QLabel(cd2)
        deco0.setPixmap(pixmap)

        cd1 = resource_path(f"images{os.sep}carte_dardagnan1.png")
        pixmap = QPixmap(cd1)
        deco1 = QLabel(cd1)
        deco1.setPixmap(pixmap)

        cd3 = resource_path(f"images{os.sep}carte_dardagnan3.png")
        pixmap = QPixmap(cd3)
        deco2 = QLabel()
        deco2.setPixmap(pixmap)

        # deco.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout_main.addWidget(label0, 0, 0, 1, 2)
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

        # width = deco0.geometry().width()
        # height = deco0.geometry().height()
        # print(width, height)

        # width = image_empty2.geometry().width()
        # height = image_empty2.geometry().height()
        # print(width, height)

        # width = label1.geometry().width()
        # height = label1.geometry().height()
        # print(width, height)

        # width = image_empty2.sizeHint().width()
        # height = image_empty2.sizeHint().height()
        # print(width, height)

        btn1.clicked.connect(self.load_project)
        self.btn2.clicked.connect(self.save_project)
        self.btn3.clicked.connect(self.lancer_analyse)

        self.grids = list()

        for num_tab in range(1, nb_tabs+1):
            
            self.grids.append(QGridLayout())

            for i in range(5):

                num_image = 5 * (num_tab - 1) + i + 1

                darda = resource_path(f"images{os.sep}dardagnan.png")
                pixmap = QPixmap(darda)
                label = QLabel()
                label.setPixmap(pixmap)
                self.grids[-1].addWidget(label, i, 0)

                im1 = resource_path(f"images{os.sep}im{num_image}.png")
                pixmap = QPixmap(im1)
                label_left = self.label_left[num_image-1]
                label_left.setPixmap(pixmap)
                self.grids[-1].addWidget(label_left, i, 2, 1, 1)

                pixmap = QPixmap(im1)
                label_right = self.label_right[num_image-1]
                label_right.setPixmap(pixmap)
                self.grids[-1].addWidget(label_right, i, 4, 1, 1)

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

                pixmap = QPixmap(darda)
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
            logging.info(msg)
            self.dialog.message(msg)
            self.dialog.show()
        else:
            pass
        return 0
    
    def load_project(self):
        DIR = QFileDialog.getOpenFileName(self, "Select a .zip project file")
        if DIR[0] != "":
            project_file = str(DIR[0])
            logging.info(f"Chargement du projet '{project_file}'")

            self.analyse_name = get_file_name(project_file)
            self.label00.setText(self.analyse_name)
            self.btn2.setText(f"Sauvegarder\nl'analyse\n{self.analyse_name}")
            self.btn3.setText(f"Lancer\nl'analyse\n{self.analyse_name}")
            
            shutil.unpack_archive(filename=project_file, extract_dir=self.tmp)
            copytree(src=self.tmp + os.sep + "in", dst=self.in_)
            copytree(src=self.tmp + os.sep + "out", dst=self.out)

            self.RES = load_results(self.tmp + os.sep + "out" + os.sep + "results.txt")
            print("results already computed:")
            print(self.RES)

            extension = os.listdir(self.out)[0].split(".")[1]
            for num_abeille in self.RES.keys():
                ci, ds = get_ci_ds(float(self.RES[num_abeille][0]), float(self.RES[num_abeille][1]))
                print(ci, ds)
                self.label_results[num_abeille-1].setText(f"     Ci : {ci}\n     Ds : {ds}°")

            for file in os.listdir(self.in_):
                num_abeille = int(file.split("_")[0])
                if num_abeille not in self.RES.keys():
                    print(f"Attention : l'abeille {num_abeille} n'a pas été trouvée dans le fichier de résultats")
                    logging.info(f"Attention : l'abeille {num_abeille} n'a pas été trouvée dans le fichier de résultats")
                else:
                    ff_in = self.in_ + os.sep + file
                    pixmap = QPixmap(ff_in)
                    pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
                    self.label_left[num_abeille-1].setPixmap(pixmap)
                    ff_out = self.out + os.sep + str(num_abeille) + "_out." + extension
                    self.label_left[num_abeille-1].setPixmap(pixmap)
                    pixmap_out = QPixmap(ff_out)
                    pixmap_out = pixmap_out.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
                    self.label_right[num_abeille-1].setPixmap(pixmap_out)
        else:
            pass
        # self.tabs.setCurrentIndex(1)
        return 0
    
    def lancer_analyse(self):
        if len(self.RES) <= 3:
            self.dialog = MESSAGE()
            msg = f"Le nombre d'ailes analysées ({len(self.RES)}) est trop faible"
            self.dialog.message(msg)
            self.dialog.show()
            logging.info(msg)
        else:
            print("calcul de l'histogramme de l'indice cubital")
            logging.info("calcul de l'histogramme de l'indice cubital")
            indices = []
            shifts = []
            for abeille in self.RES.keys():
                indices.append(float(self.RES[abeille][0]))
                shifts.append(float(self.RES[abeille][1]))
            ci_images, ds_image = analyse(indices, shifts, path_out=self.out)
            pixmap = QPixmap(ci_images[0])
            self.label_analyses[0].setPixmap(pixmap)
            pixmap = QPixmap(ds_image)
            self.label_analyses[1].setPixmap(pixmap)
            # self.setFixedSize(self.tab0.layout.sizeHint())()
            self.resize(self.tab0.sizeHint().width(), self.tab0.sizeHint().height())
        return 

if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()
    
    window = MainWindow()
    window.show()

    app.exec()

    # for file in os.listdir(self.dialog.path + "out" + os.sep + self.dialog.name):
    #     filename = file
    # pixmap = QPixmap(self.dialog.path + "out" + os.sep + self.dialog.name + os.sep + filename)
    # print(self.dialog.path + "out" + os.sep + self.dialog.name + os.sep + filename)
    # pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
    # self.label_right[0].setPixmap(pixmap)