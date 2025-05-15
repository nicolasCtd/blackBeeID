import os 

def visu1(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.out):
        if "1_out" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + name)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu2(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    for file in os.listdir(TAB.out):
        if "2_out" in file:
            file_exists = 1
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + file)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()


def visu3(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    for file in os.listdir(TAB.out):
        if "3_out" in file:
            file_exists = 1
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + file)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu4(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    for file in os.listdir(TAB.out):
        if "4_out" in file:
            file_exists = 1
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + file)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu5(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    for file in os.listdir(TAB.out):
        if "5_out" in file:
            file_exists = 1
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + file)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu6(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    for file in os.listdir(TAB.out):
        if "6_out" in file:
            file_exists = 1
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + file)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu7(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    for file in os.listdir(TAB.out):
        if "7_out" in file:
            file_exists = 1
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + file)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu8(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    for file in os.listdir(TAB.out):
        if "8_out" in file:
            file_exists = 1
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + file)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu9(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    for file in os.listdir(TAB.out):
        if "9_out" in file:
            file_exists = 1
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + file)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu10(TAB):
    from IHM import VISU, MESSAGE
    file_exists = 0
    for file in os.listdir(TAB.out):
        if "10_out" in file:
            file_exists = 1
    if file_exists:
        TAB.dialog = VISU()
        TAB.dialog.display(TAB.out + os.sep + file)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu11(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu12(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu13(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu14(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu15(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu16(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu17(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu18(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu19(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu20(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu21(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu22(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu23(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu24(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu25(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu26(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu27(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu28(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu29(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu30(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu31(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu32(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu33(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu34(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu35(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu36(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out + os.sep + "36"
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu37(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out + os.sep + "37"
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu38(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out + os.sep + "38"
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu39(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out + os.sep + "39"
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()

def visu40(TAB):
    from IHM import VISU, MESSAGE
    path = TAB.out + os.sep + "40"
    try:
        fileName = os.listdir(path)[0]
    except:
        fileName = ""
    if fileName != "":
        TAB.dialog = VISU()
        TAB.dialog.display(path + os.sep + fileName)
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur2()