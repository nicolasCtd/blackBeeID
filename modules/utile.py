from datetime import datetime, date
import os 
import shutil
import numpy as np
import os
import matplotlib.pyplot as plt
import csv
from matplotlib.ticker import MultipleLocator
from scipy.stats import pearsonr
    
def copytree(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

def clean(value):
    return str(value).replace("[", "").replace("]", "")

def get_ci_ds(ci_value, ds_value):
    ci = int(ci_value * 100)/100
    ds_ = clean(ds_value)
    
    tt = "+"
    if float(ds_) < 0:
        tt = "-"

    return str(ci), tt + str(np.abs(int(float(ds_)*100)/100))

def load_results(file):
    res = {}
    with open(file, "r") as f:
        a = f.readlines()
    for i in range(len(a)):
        line = a[i].replace("\n", "").split(" ")
        res[int(line[0])] = (line[1], line[2])
    return res

def save_results_txt(path, res):
    with open(path + "results.txt", "w") as f:
        liste_abeilles = [int(key) for key in res.keys()]
        for num in sorted(liste_abeilles):
            line = f"{num} {clean(res[num][0])} {res[num][1]}\n"
            f.write(line)
        f.close()

def write_line(file, num, ci_value, ds_value):
    line = f"{num} {ci_value} {ds_value}\n"
    with open(file, "a") as f:
        f.write(line)
    f.close()
    return 0

def insertnow(file):       
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S").replace("/", "_").replace(" ", "___").replace(":", "_")
    tmp = file.split(".")
    return tmp[0] + "___" + dt_string + "." + tmp[-1]

def get_file_name(path):
    path_split = path.replace(os.sep, "/").split("/")
    name = path_split[-1].replace(".zip","")
    return name.split("_")[0]

def get_path(path2file):
    path_split = path2file.replace(os.sep, "/").split("/")
    return os.sep.join(path_split[:-1]) + os.sep



def gauss(x, mu, sigma):
    return 1/(np.sqrt(2*np.pi) * sigma) * np.exp(-(x - mu)**2/(2*sigma**2))

def denoise_images(path):
    ech_denoise = list()
    ech_input = list()

    for file in os.listdir(path):
        if '.jpg' in file:
            ech_input.append(int(file.split('.')[0]))

    for file in os.listdir(path + os.sep + "denoise"):
        ech_denoise.append(int(file.split("_")[0]))

    done = np.intersect1d(ech_input, ech_denoise)

    for file in os.listdir(path):
        if '.jpg' in file:
            if int(file.split('.')[0]) not in done:
                print(f"denoising of image {file}...")
                denoise(file, "denoise" + file, save=True)
                print('done')
            

def denoise(path_in, path_out, save=False):
    image = cv2.imread(path_in)
    dst = cv2.fastNlMeansDenoisingColored(image, None, 11, 6, 7, 21)
    verbose = ""
    if save:
        verbose += f"save image {path_out}"
        cv2.imwrite(path_out, dst)
    return dst, verbose


def check_new_files(Rref, R):
    """Check files that are present in directory 'Rref' but not present in directory 'R' """
    
    files_in_Rref = files(Rref)

    for i in range(len(files_in_Rref)):
        files_in_Rref[i] = int(files_in_Rref[i].replace(".", "_").split("_")[0])

    files_in_R = files(R)

    for i in range(len(files_in_R)):
        files_in_R[i] = int(files_in_R[i].replace(".", "_").split("_")[0])

    UU = [True] * len(files_in_Rref)
    for index, in_Rref in enumerate(files_in_Rref):
        for file in files_in_R:
            if file == in_Rref:
                UU[index] = False

    unique = list()
    present_in_both = list()
    for idx, value in enumerate(UU):
        if value == True:
            unique.append(files_in_Rref[idx])
        else:
            present_in_both.append(files_in_Rref[idx])

    return unique, present_in_both

def files(directory):
    F = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            F.append(file)
    return F