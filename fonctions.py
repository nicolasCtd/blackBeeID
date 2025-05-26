import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import csv
from matplotlib.ticker import MultipleLocator
from scipy.stats import pearsonr


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