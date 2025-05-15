from datetime import datetime, date
import os 
import shutil
import numpy as np

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

