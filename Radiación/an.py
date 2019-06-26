import sys
sys.path.insert(0, '../')

from analysis import gauss_curve, choose_line, line_param, gauss_fit
from os import listdir
import numpy as np

files = listdir("Datos/")
names =["Referencia Potasio", "Referencia Uranio", "Muestra Zapatoca",
        "Muestra Unal"]

direc_name="Datos/"
energy, counts = [1]*len(files) ,[1]*len(files)
for x in range(len(files)):
    energy[x], counts[x]= np.loadtxt(direc_name+files[x], unpack=True)

print("----------------------")
print("Equivalencia:")
for x in range(len(names)):
    print("%s ---> %i"%(names[x], x))
print("----------------------")
print()
#Procedimientos ==========================
print("----------------------")
choosing=str(input("Uranio o Potasio (U/K)"))
print("----------------------")
if choosing=="K":
    mean=1461
elif choosing=="U":
    mean=352
names =[x+"(%i keV)"%mean for x in names]
gauss_fit(int(input("# Tabla >")), energy, counts, names, mean)
