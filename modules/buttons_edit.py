from kore.common import *
import logging
# from modules.ci_and_ds_tools import POINT

def editFile1(TAB):
    TAB.num = 1
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "1_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°1")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile2(TAB):
    TAB.num = 2
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "2_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°2")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile3(TAB):
    TAB.num = 3
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "3_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°3")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile4(TAB):
    TAB.num = 4
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "4_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°4")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile5(TAB):
    TAB.num = 5
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "5_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°5")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile6(TAB):
    TAB.num = 6
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "6_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°6")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile7(TAB):
    TAB.num = 7
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "7_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°7")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile8(TAB):
    TAB.num = 8
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "8_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°8")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile9(TAB):
    TAB.num = 9
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "9_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°9")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile10(TAB):
    TAB.num = 10
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "10_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°10")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile11(TAB):
    TAB.num = 11
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "11_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°11")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile12(TAB):
    TAB.num = 12
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "12_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°12")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile13(TAB):
    TAB.num = 13
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "13_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°13")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile14(TAB):
    TAB.num = 14
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "14_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°14")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile15(TAB):
    TAB.num = 15
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "15_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°15")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile16(TAB):
    TAB.num = 16
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "16_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°16")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile17(TAB):
    TAB.num = 17
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "17_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°17")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile18(TAB):
    TAB.num = 18
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "18_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°18")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile19(TAB):
    TAB.num = 19
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "19_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°19")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile20(TAB):
    TAB.num = 20
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "20_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°20")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile21(TAB):
    TAB.num = 21
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "21_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°21")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile22(TAB):
    TAB.num = 22
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "22_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°22")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile23(TAB):
    TAB.num = 23
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "23_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°23")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile24(TAB):
    TAB.num = 24
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "24_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°24")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile25(TAB):
    TAB.num = 25
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "25_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°25")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile26(TAB):
    TAB.num = 26
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "26_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°26")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile27(TAB):
    TAB.num = 27
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "27_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°27")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile28(TAB):
    TAB.num = 28
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "28_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°28")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile29(TAB):
    TAB.num = 29
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "29_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°29")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile30(TAB):
    TAB.num = 30
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "30_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°30")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile31(TAB):
    TAB.num = 31
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "31_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°31")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile32(TAB):
    TAB.num = 32
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "32_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°32")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile33(TAB):
    TAB.num = 33
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "33_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°33")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile34(TAB):
    TAB.num = 34
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "34_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°34")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    

def editFile35(TAB):
    TAB.num = 35
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "35_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°35")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile36(TAB):
    TAB.num = 36
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "36_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°36")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile37(TAB):
    TAB.num = 37
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "37_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°37")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile38(TAB):
    TAB.num = 38
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "38_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°38")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile39(TAB):
    TAB.num = 39
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "39_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°39")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile40(TAB):
    TAB.num = 40
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "40_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°40")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile41(TAB):
    TAB.num = 41
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "41_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°41")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile42(TAB):
    TAB.num = 42
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "42_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°42")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1() 

def editFile43(TAB):
    TAB.num = 43
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "43_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°43")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile44(TAB):
    TAB.num = 44
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "44_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°44")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile45(TAB):
    TAB.num = 45
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "45_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°45")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile46(TAB):
    TAB.num = 46
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "46_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°46")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile47(TAB):
    TAB.num = 47
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "47_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°47")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile48(TAB):
    TAB.num = 48
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "48_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°48")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()

def editFile49(TAB):
    TAB.num = 49
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "49_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°49")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
def editFile50(TAB):
    TAB.num = 50
    file_exists = 0
    name = ""
    for file in os.listdir(TAB.in_):
        if "50_in" in file:
            file_exists = True
            name = file
    if file_exists:
        TAB.dialog = EDIT(TAB, num=TAB.num)
        TAB.dialog.display(name)
        logging.info("Edition de l'image n°50")
        logging.info("----------------------")
    else:
        TAB.dialog = MESSAGE()
        TAB.dialog.message_erreur1()
    
