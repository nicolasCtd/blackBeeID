from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
import shutil
import os
from PyQt5.QtCore import Qt
import logging
from PIL import Image, ImageDraw, ImageFont

def browseFile1(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName1, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName1, TAB.in_, 1)

    if TAB.fileName1 != "":
        pixmap = QPixmap(TAB.fileName1)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[0].setPixmap(pixmap)
        TAB.grids[0].addWidget(TAB.label_left[0], 0, 2, 1, 1)
    else:
        pass
    
def browseFile2(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName2, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName2, TAB.in_, 2)

    if TAB.fileName2 != "":
        pixmap = QPixmap(TAB.fileName2)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[1].setPixmap(pixmap)
        TAB.grids[0].addWidget(TAB.label_left[1], 1, 2, 1, 1)
    else:
        pass

def browseFile3(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName3, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName3, TAB.in_, 3)

    if TAB.fileName3 != "":
        pixmap = QPixmap(TAB.fileName3)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[2].setPixmap(pixmap)
        TAB.grids[0].addWidget(TAB.label_left[2], 2, 2, 1, 1)
    else:
        pass

def browseFile4(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName4, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName4, TAB.in_, 4)

    if TAB.fileName4 != "":
        pixmap = QPixmap(TAB.fileName4)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[3].setPixmap(pixmap)
        TAB.grids[0].addWidget(TAB.label_left[3], 3, 2, 1, 1)
    else:
        pass

def browseFile5(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName5, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName5, TAB.in_, 5)

    if TAB.fileName5 != "":
        pixmap = QPixmap(TAB.fileName5)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[4].setPixmap(pixmap)
        TAB.grids[0].addWidget(TAB.label_left[4], 4, 2, 1, 1)
    else:
        pass

def browseFile6(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName6, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName6, TAB.in_, 6)

    if TAB.fileName6 != "":
        pixmap = QPixmap(TAB.fileName6)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[5].setPixmap(pixmap)
        TAB.grids[1].addWidget(TAB.label_left[5], 0, 2, 1, 1)
    else:
        pass

def browseFile7(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName7, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName7, TAB.in_, 7)

    if TAB.fileName7 != "":
        pixmap = QPixmap(TAB.fileName7)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[6].setPixmap(pixmap)
        TAB.grids[1].addWidget(TAB.label_left[6], 1, 2, 1, 1)
    else:
        pass

def browseFile8(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName8, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName8, TAB.in_, 8)

    if TAB.fileName8 != "":
        pixmap = QPixmap(TAB.fileName8)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[7].setPixmap(pixmap)
        TAB.grids[1].addWidget(TAB.label_left[7], 2, 2, 1, 1)
    else:
        pass

def browseFile9(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName9, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName9, TAB.in_, 9)

    if TAB.fileName9 != "":
        pixmap = QPixmap(TAB.fileName9)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[8].setPixmap(pixmap)
        TAB.grids[1].addWidget(TAB.label_left[8], 3, 2, 1, 1)
    else:
        pass

def browseFile10(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName10, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName10, TAB.in_, 10)

    if TAB.fileName10 != "":
        pixmap = QPixmap(TAB.fileName10)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[9].setPixmap(pixmap)
        TAB.grids[1].addWidget(TAB.label_left[9], 4, 2, 1, 1)
    else:
        pass

def browseFile11(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName11, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName11, TAB.in_, 11)

    if TAB.fileName11 != "":
        pixmap = QPixmap(TAB.fileName11)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[10].setPixmap(pixmap)
        TAB.grids[2].addWidget(TAB.label_left[10], 0, 2, 1, 1)
    else:
        pass

def browseFile12(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName12, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName12, TAB.in_, 12)

    if TAB.fileName12 != "":
        pixmap = QPixmap(TAB.fileName12)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[11].setPixmap(pixmap)
        TAB.grids[2].addWidget(TAB.label_left[11], 1, 2, 1, 1)
    else:
        pass

def browseFile13(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName13, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName13, TAB.in_, 13)

    if TAB.fileName13 != "":
        pixmap = QPixmap(TAB.fileName13)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[12].setPixmap(pixmap)
        TAB.grids[2].addWidget(TAB.label_left[12], 2, 2, 1, 1)
    else:
        pass

def browseFile14(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName14, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName14, TAB.in_, 14)

    if TAB.fileName14 != "":
        pixmap = QPixmap(TAB.fileName14)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[13].setPixmap(pixmap)
        TAB.grids[2].addWidget(TAB.label_left[13], 3, 2, 1, 1)
    else:
        pass

def browseFile15(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName15, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName15, TAB.in_, 15)

    if TAB.fileName15 != "":
        pixmap = QPixmap(TAB.fileName15)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[14].setPixmap(pixmap)
        TAB.grids[2].addWidget(TAB.label_left[14], 4, 2, 1, 1)
    else:
        pass

def browseFile16(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName16, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName16, TAB.in_, 16)

    if TAB.fileName16 != "":
        pixmap = QPixmap(TAB.fileName16)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[15].setPixmap(pixmap)
        TAB.grids[3].addWidget(TAB.label_left[15], 0, 2, 1, 1)
    else:
        pass 

def browseFile17(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName17, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName17, TAB.in_, 17)

    if TAB.fileName17 != "":
        pixmap = QPixmap(TAB.fileName17)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[16].setPixmap(pixmap)
        TAB.grids[3].addWidget(TAB.label_left[16], 1, 2, 1, 1)
    else:
        pass 

def browseFile18(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName18, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName18, TAB.in_, 18)

    if TAB.fileName18 != "":
        pixmap = QPixmap(TAB.fileName18)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[17].setPixmap(pixmap)
        TAB.grids[3].addWidget(TAB.label_left[17], 2, 2, 1, 1)
    else:
        pass 

def browseFile19(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName19, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName19, TAB.in_, 19)

    if TAB.fileName19 != "":
        pixmap = QPixmap(TAB.fileName19)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[18].setPixmap(pixmap)
        TAB.grids[3].addWidget(TAB.label_left[18], 3, 2, 1, 1)
    else:
        pass 

def browseFile20(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName20, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName20, TAB.in_, 20)

    if TAB.fileName20 != "":
        pixmap = QPixmap(TAB.fileName20)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[19].setPixmap(pixmap)
        TAB.grids[3].addWidget(TAB.label_left[19], 4, 2, 1, 1)
    else:
        pass

def browseFile21(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName21, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName21, TAB.in_, 21)

    if TAB.fileName21 != "":
        pixmap = QPixmap(TAB.fileName21)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[20].setPixmap(pixmap)
        TAB.grids[4].addWidget(TAB.label_left[20], 0, 2, 1, 1)
    else:
        pass

def browseFile22(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName22, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName22, TAB.in_, 22)

    if TAB.fileName22 != "":
        pixmap = QPixmap(TAB.fileName22)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[21].setPixmap(pixmap)
        TAB.grids[4].addWidget(TAB.label_left[21], 1, 2, 1, 1)
    else:
        pass

def browseFile23(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName23, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName23, TAB.in_, 23)

    if TAB.fileName23 != "":
        pixmap = QPixmap(TAB.fileName23)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[22].setPixmap(pixmap)
        TAB.grids[4].addWidget(TAB.label_left[22], 2, 2, 1, 1)
    else:
        pass

def browseFile24(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName24, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName24, TAB.in_, 24)

    if TAB.fileName24 != "":
        pixmap = QPixmap(TAB.fileName24)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[23].setPixmap(pixmap)
        TAB.grids[4].addWidget(TAB.label_left[23], 3, 2, 1, 1)
    else:
        pass

def browseFile25(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName25, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName25, TAB.in_, 25)

    if TAB.fileName25 != "":
        pixmap = QPixmap(TAB.fileName25)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[24].setPixmap(pixmap)
        TAB.grids[4].addWidget(TAB.label_left[24], 4, 2, 1, 1)
    else:
        pass

def browseFile26(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName26, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName26, TAB.in_, 26)

    if TAB.fileName26 != "":
        pixmap = QPixmap(TAB.fileName26)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[25].setPixmap(pixmap)
        TAB.grids[5].addWidget(TAB.label_left[25], 0, 2, 1, 1)
    else:
        pass

def browseFile27(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName27, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName27, TAB.in_, 27)

    if TAB.fileName27 != "":
        pixmap = QPixmap(TAB.fileName27)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[26].setPixmap(pixmap)
        TAB.grids[5].addWidget(TAB.label_left[26], 1, 2, 1, 1)
    else:
        pass

def browseFile28(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName28, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName28, TAB.in_, 28)

    if TAB.fileName28 != "":
        pixmap = QPixmap(TAB.fileName28)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[27].setPixmap(pixmap)
        TAB.grids[5].addWidget(TAB.label_left[27], 2, 2, 1, 1)
    else:
        pass

def browseFile29(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName29, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName29, TAB.in_, 29)

    if TAB.fileName29 != "":
        pixmap = QPixmap(TAB.fileName29)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[28].setPixmap(pixmap)
        TAB.grids[5].addWidget(TAB.label_left[28], 3, 2, 1, 1)
    else:
        pass

def browseFile30(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName30, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName30, TAB.in_, 30)

    if TAB.fileName30 != "":
        pixmap = QPixmap(TAB.fileName30)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[29].setPixmap(pixmap)
        TAB.grids[5].addWidget(TAB.label_left[29], 4, 2, 1, 1)
    else:
        pass

def browseFile31(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName31, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName31, TAB.in_, 31)

    if TAB.fileName31 != "":
        pixmap = QPixmap(TAB.fileName31)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[30].setPixmap(pixmap)
        TAB.grids[6].addWidget(TAB.label_left[30], 0, 2, 1, 1)
    else:
        pass

def browseFile32(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName32, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName32, TAB.in_, 32)

    if TAB.fileName32 != "":
        pixmap = QPixmap(TAB.fileName32)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[31].setPixmap(pixmap)
        TAB.grids[6].addWidget(TAB.label_left[31], 1, 2, 1, 1)
    else:
        pass

def browseFile33(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName33, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName33, TAB.in_, 33)

    if TAB.fileName33 != "":
        pixmap = QPixmap(TAB.fileName33)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[32].setPixmap(pixmap)
        TAB.grids[6].addWidget(TAB.label_left[32], 2, 2, 1, 1)
    else:
        pass

def browseFile34(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName34, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName34, TAB.in_, 34)

    if TAB.fileName34 != "":
        pixmap = QPixmap(TAB.fileName34)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[33].setPixmap(pixmap)
        TAB.grids[6].addWidget(TAB.label_left[33], 3, 2, 1, 1)
    else:
        pass

def browseFile35(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName35, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName35, TAB.in_, 35)

    if TAB.fileName35 != "":
        pixmap = QPixmap(TAB.fileName35)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[34].setPixmap(pixmap)
        TAB.grids[6].addWidget(TAB.label_left[34], 4, 2, 1, 1)
    else:
        pass

def browseFile36(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName36, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName36, TAB.in_, 36)

    if TAB.fileName36 != "":
        pixmap = QPixmap(TAB.fileName36)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[35].setPixmap(pixmap)
        TAB.grids[7].addWidget(TAB.label_left[35], 0, 2, 1, 1)
    else:
        pass

def browseFile37(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName37, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName37, TAB.in_, 37)

    if TAB.fileName37 != "":
        pixmap = QPixmap(TAB.fileName37)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[36].setPixmap(pixmap)
        TAB.grids[7].addWidget(TAB.label_left[36], 1, 2, 1, 1)
    else:
        pass

def browseFile38(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName38, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName38, TAB.in_, 38)

    if TAB.fileName38 != "":
        pixmap = QPixmap(TAB.fileName38)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[37].setPixmap(pixmap)
        TAB.grids[7].addWidget(TAB.label_left[37], 2, 2, 1, 1)
    else:
        pass

def browseFile39(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName39, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName39, TAB.in_, 39)

    if TAB.fileName39 != "":
        pixmap = QPixmap(TAB.fileName39)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[38].setPixmap(pixmap)
        TAB.grids[7].addWidget(TAB.label_left[38], 3, 2, 1, 1)
    else:
        pass

def browseFile40(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName40, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName40, TAB.in_, 40)

    if TAB.fileName40 != "":
        pixmap = QPixmap(TAB.fileName40)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[39].setPixmap(pixmap)
        TAB.grids[7].addWidget(TAB.label_left[39], 4, 2, 1, 1)
    else:
        pass

def browseFile41(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName41, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName41, TAB.in_, 41)

    if TAB.fileName41 != "":
        pixmap = QPixmap(TAB.fileName41)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[40].setPixmap(pixmap)
        TAB.grids[8].addWidget(TAB.label_left[40], 0, 2, 1, 1)
    else:
        pass

def browseFile42(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName42, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName42, TAB.in_, 42)

    if TAB.fileName42 != "":
        pixmap = QPixmap(TAB.fileName42)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[41].setPixmap(pixmap)
        TAB.grids[8].addWidget(TAB.label_left[41], 1, 2, 1, 1)
    else:
        pass

def browseFile43(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName43, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName43, TAB.in_, 43)

    if TAB.fileName43 != "":
        pixmap = QPixmap(TAB.fileName43)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[42].setPixmap(pixmap)
        TAB.grids[8].addWidget(TAB.label_left[42], 2, 2, 1, 1)
    else:
        pass

def browseFile44(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName44, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName44, TAB.in_, 44)

    if TAB.fileName44!= "":
        pixmap = QPixmap(TAB.fileName44)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[43].setPixmap(pixmap)
        TAB.grids[8].addWidget(TAB.label_left[43], 3, 2, 1, 1)
    else:
        pass

def browseFile45(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName45, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName45, TAB.in_, 45)

    if TAB.fileName45 != "":
        pixmap = QPixmap(TAB.fileName45)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[44].setPixmap(pixmap)
        TAB.grids[8].addWidget(TAB.label_left[44], 4, 2, 1, 1)
    else:
        pass

def browseFile46(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName46, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName46, TAB.in_, 46)

    if TAB.fileName46 != "":
        pixmap = QPixmap(TAB.fileName46)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[45].setPixmap(pixmap)
        TAB.grids[9].addWidget(TAB.label_left[45], 0, 2, 1, 1)
    else:
        pass

def browseFile47(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName47, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName47, TAB.in_, 47)

    if TAB.fileName47 != "":
        pixmap = QPixmap(TAB.fileName47)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[46].setPixmap(pixmap)
        TAB.grids[9].addWidget(TAB.label_left[46], 1, 2, 1, 1)
    else:
        pass

def browseFile48(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName48, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)
    
    save_image(TAB.fileName48, TAB.in_, 48)

    if TAB.fileName48 != "":
        pixmap = QPixmap(TAB.fileName48)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[47].setPixmap(pixmap)
        TAB.grids[9].addWidget(TAB.label_left[47], 2, 2, 1, 1)
    else:
        pass

def browseFile49(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName49, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName49, TAB.in_, 49)

    if TAB.fileName49 != "":
        pixmap = QPixmap(TAB.fileName49)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[48].setPixmap(pixmap)
        TAB.grids[9].addWidget(TAB.label_left[48], 3, 2, 1, 1)
    else:
        pass

def browseFile50(TAB):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    TAB.fileName50, _ = QFileDialog.getOpenFileName(TAB, "Select File", "", "All Files (*)", options=options)

    save_image(TAB.fileName50, TAB.in_, 50)

    if TAB.fileName50 != "":
        pixmap = QPixmap(TAB.fileName50)
        pixmap = pixmap.scaled(TAB.width, TAB.height, Qt.KeepAspectRatio, Qt.FastTransformation)
        TAB.label_left[49].setPixmap(pixmap)
        TAB.grids[9].addWidget(TAB.label_left[49], 4, 2, 1, 1)
    else:
        pass

def save_image(nameFile, destination, num):
    img = Image.open(nameFile)
    img.save(destination + os.sep + f"{num}_in.jpg")
    logging.info(f"Image n°{num} : " + destination + os.sep + f"{num}_in.jpg")
