# Premiers développements pour pouvoir utiliser une IHM.
# L'IHM doit permettre de :
#   - sélectionner et charger une image d'aile d'abeille dans un dossier ;
#   - positionner 6 points d'intérêt sur l'image ;
#   - Enregistrer l'image en sortie avec les valeurs de l'indice cubital et du shift discoidal ;
#   - Lancer l'analyse sur toutes les images traitées
#           (histogramme de l'indice cubital, scatter plot de l'indice cubital vs discoidal shift, ...)
	

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap



class IHM(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle("IHM")
        self.setGeometry(100, 100, 1200, 900)

        layout = QGridLayout()

        pixmap = QPixmap('im.png')
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.label)
        self.setLayout(self.hbox)
        self.setWindowTitle('IHM')

        button = QPushButton("Browse", self)
        button.clicked.connect(self.browseFile)
        button.move(100, 100)

        layout.addWidget(pixmap, 1, 0)
        layout.addWidget(button, 0, 0)
        
        self.setLayout(layout)

        self.show()
        
    def browseFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)", options=options)
        print(f"Selected file: {fileName}")
        
        pixmap = QPixmap(fileName)
        print(pixmap.width(), pixmap.height())
        self.label.setPixmap(pixmap)
        self.hbox.addWidget(self.label)
        self.setLayout(self.hbox)
        self.move(100, 100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myIHM = IHM()
    sys.exit(app.exec_())