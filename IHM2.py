import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QGridLayout,
    QSizePolicy,
    QTabWidget
)
from PyQt5.QtGui import QPixmap

from PyQt5.QtGui import QPainter, QColor
from PyQt5 import QtCore, QtGui, QtWidgets



class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analyse des ailes d'abeilles")

        self.tab_widget = Tab(self) 
        self.setCentralWidget(self.tab_widget) 


class Tab(QWidget): 
    def __init__(self, parent): 
        super(QWidget, self).__init__(parent) 
        # self.layout = QVBoxLayout(self)
        # self.layout = QGridLayout(self) 

        self.layout = QVBoxLayout(self) 
  
        # Initialize tab screen 
        self.tabs = QTabWidget() 
        self.tab1 = QWidget() 
        self.tab2 = QWidget() 
        self.tab3 = QWidget() 
        # self.tabs.resize(300, 200) 
  
        # Add tabs 
        self.tabs.addTab(self.tab1, "1-5") 
        self.tabs.addTab(self.tab2, "6-10") 
        self.tabs.addTab(self.tab3, "11-15")
        # self.tabs.addTab(self.tab4, "16-20") 
        # self.tabs.addTab(self.tab5, "21-25") 
        # self.tabs.addTab(self.tab6, "26-30")
   
        self.width = 500
        self.height = 500

        self.grid = QGridLayout()
        self.label_left = [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)]
        self.label_right = [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)]

        for i in range(5):
            pixmap = QPixmap(f"im{i+1}.png")
            label_left = self.label_left[i]
            label_left.setPixmap(pixmap)
            self.grid.addWidget(label_left, i, 1)

            pixmap = QPixmap(f"im{i+1}.png")
            label_right = self.label_right[i]
            label_right.setPixmap(pixmap)
            self.grid.addWidget(label_right, i, 3)

            btn1 = QPushButton("Load")
            btn1.resize(50, 150)
            btn1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            btn2 = QPushButton("Edit")
            btn2.resize(50, 150)
            btn2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            if i == 0:
                btn1.clicked.connect(self.browseFile0)
                btn2.clicked.connect(self.editFile0)
            elif i == 1:
                btn1.clicked.connect(self.browseFile1)
                btn2.clicked.connect(self.editFile1)
            elif i == 2:
                btn1.clicked.connect(self.browseFile2)
                btn2.clicked.connect(self.editFile2)
            elif i == 3:
                btn1.clicked.connect(self.browseFile3)
                btn2.clicked.connect(self.editFile3)
            elif i == 4:
                btn1.clicked.connect(self.browseFile4)
                btn2.clicked.connect(self.editFile4)
            else:
                pass

            self.grid.addWidget(btn1, i, 0)
            self.grid.addWidget(btn2, i, 2)
		

        # Create first tab 
        # self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout = self.grid
        # self.l = QLabel()
        # self.l.setText("This is the first tab")
        # self.tab1.layout.addWidget(self.l)
        self.tab1.setLayout(self.tab1.layout)

        # self.tab1.layout.addWidget(self.grid)
        # self.tab1.setLayout(self.tab1.layout)
        # widget = QWidget()
        # widget.setLayout(self.grid)
        # self.setCentralWidget(widget)

        # Add tabs to widget
        # widget = QWidget()
        # widget.setLayout(self.grid)
        # self.layout.addWidget(self.tabs) 
        # self.setLayout(self.tab1.layout)

        # self.tab1.layout.addWidget(self.l)
        # self.tab1.setLayout(self.tab1.layout)

        # self.tab1.setLayout(self.tab1.layout)

        # self.tab1.layout.addWidget(self.l)
        # self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs) 
        self.setLayout(self.layout) 



    def browseFile0(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        print(f"Selected file: {fileName}")
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label_left[0].setPixmap(pixmap)
        self.grid.addWidget(self.label_left[0], 0, 1)
        self.label_left[0].mousePressEvent = self.getPos
    
    def browseFile1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        print(f"Selected file: {fileName}")
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label_left[1].setPixmap(pixmap)
        self.grid.addWidget(self.label_left[1], 1, 1)
        self.label_left[1].mousePressEvent = self.getPos

    def browseFile2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        print(f"Selected file: {fileName}")
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label_left[2].setPixmap(pixmap)
        self.grid.addWidget(self.label_left[2], 2, 1)
        self.label_left[2].mousePressEvent = self.getPos

    def browseFile3(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        print(f"Selected file: {fileName}")
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label_left[3].setPixmap(pixmap)
        self.grid.addWidget(self.label_left[3], 3, 1)
        self.label_left[3].mousePressEvent = self.getPos

    def browseFile4(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        print(f"Selected file: {fileName}")
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label_left[4].setPixmap(pixmap)
        self.grid.addWidget(self.label_left[4], 4, 1)
        self.label_left[4].mousePressEvent = self.getPos
    
    def browseFile5(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        print(f"Selected file: {fileName}")
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(self.width, self.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label_left[5].setPixmap(pixmap)
        self.grid.addWidget(self.label, 5, 1)
        self.label_left[5].mousePressEvent = self.getPos

    def editFile0(self):
        return 0
    
    def editFile1(self):
        return 0

    def editFile2(self):
        return 0
    
    def editFile3(self):
        return 0

    def editFile4(self):
        return 0


    def getPos(self , event):
        x = event.pos().x()
        y = event.pos().y()




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

