from fonctions import *


path = os.sep.join([os.path.dirname(__file__), "OUTPUT", "analyses", "comparaison_DeepWings"]) + os.sep

print(path)

ID = list()
IC_deep = list()
IC = list()
DS_deep = list()
DS = list()

avoid = [10, 14, 17, 19, 21, 29, 30, 34, 50, 52, 60, 61, 62, 66, 68, 73]
avoid = avoid + [i for i in range(20, 30)]

with open(f"{path}comparaison.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    line = row[0].split(";")
    if line[0] == 'num':
      continue
    else:
        if int(line[0]) not in avoid:
            ID.append(int(line[0]))
            IC.append(float(line[1]))
            IC_deep.append(float(line[2]))
            DS.append(float(line[3]))
            DS_deep.append(float(line[4]))
        else:
           continue

visu = "RUTTNER"
H = HISTOGRAM(indices=IC, visu=visu, path=path + os.sep + "blackBee" + os.sep)
H.plot_histogram(show=False, save=False)

I = HISTOGRAM(indices=IC_deep, visu=visu, path=path + os.sep + "DeepWings" + os.sep)
I.histogram()
I.MCLC()

# H.add_plot(I.x, I.y, I.indices, I.mclc, show=False, save=True)

scatter_plot(path=path, indices=[IC, IC_deep], shifts=[DS, DS_deep], name_fig="comp_BeeID_deepWings", legends=["Bee ID", "deepWings"])

# scatter_plot(path=path, indices=IC, shifts=DS, name_fig="Bee_ID", title="BEE ID")
# scatter_plot(path=path, indices=IC_deep, shifts=DS_deep, name_fig="DeepWings", title="DeepWings")

