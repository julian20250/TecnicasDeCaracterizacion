import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from scipy.optimize import curve_fit
from uncertainties import ufloat
plt.style.use("seaborn-bright")

def gauss_curve(x,a,sigma, x0=667):
    "Genera una curva Gaussiana."

    return a*np.e**(-(x-x0)**2/(2*sigma**2))

def choose_line(num_data, energy, counts):
    "Escoje la línea y retorna las ubicaciones de los puntos de interés"

    begin = float(input("Valor E_\gamma inicial > "))
    end = float(input("Valor E_\gamma final > "))

    calB =[abs(x-begin) for x in energy[num_data]]
    calE =[abs(x-end) for x in energy[num_data]]

    posB, posE = calB.index(min(calB)), calE.index(min(calE))
    return [posB, posE]

def line_param(num_data, pos, energy, counts):
    "Calcula los parámetros de la recta de interés."
    y_0, y_1 = counts[num_data][pos[0]], counts[num_data][pos[1]]
    x_0, x_1 = energy[num_data][pos[0]], energy[num_data][pos[1]]

    m=(y_1-y_0)/(x_1-x_0)
    b=(y_0*x_1-y_1*x_0)/(x_1-x_0)
    return [m,b]

def gauss_fit(num_data,energy, counts, names, mean=662):
    "Dibuja el fit Gaussiano"

    print("Escoja la línea")
    plt.plot(energy[num_data], counts[num_data])
    plt.show()
    pos=choose_line(num_data, energy, counts)
    space = np.linspace(energy[num_data][pos[0]], energy[num_data][pos[1]])
    intEnergy = energy[num_data][pos[0]:pos[1]]
    intCount = counts[num_data][pos[0]:pos[1]]
    m,b = line_param(num_data, pos, energy, counts)

    tmp_count = [y-m*x-b for x,y in zip(intEnergy, intCount)]
    tmp_fun=lambda x,a,sigma: gauss_curve(x, a, sigma, x0=mean)
    popt,pcov = curve_fit(gauss_curve, intEnergy, tmp_count,  p0=[1, 1, mean])
    gaussian = m*space+b+gauss_curve(space, popt[0], popt[1], popt[2])

    #Sección de Impresión
    perr=np.sqrt(np.diag(pcov))
    A=ufloat(popt[0],perr[0])
    sigma=ufloat(abs(popt[1]), perr[1])
    Intensity = abs(np.sqrt(2*np.pi)*A*sigma)
    print("=================================")
    print("Ajuste Gaussiano, %s"%names[num_data])
    print("A= "+str(A))
    print("\sigma= "+str(sigma))
    #print("x_0=%f"%popt[2])
    print("Intensidad en cuentas = "+str(Intensity))

    #Sección de Graficado
    plt.plot(intEnergy, intCount, label=names[num_data])
    plt.plot(space, gaussian, label="Ajuste Gaussiano", linestyle="--")
    plt.plot(space, m*space+b)
    plt.xlabel("$E_\gamma$ (keV)", fontsize=15)
    plt.ylabel("$I_\gamma$ (cuentas/keV)", fontsize=15)
    plt.tight_layout()
    plt.grid()
    plt.legend()
    plt.show()

#Adquisicion de datos ========================
"""
files = listdir("datosexperimentodensidadarenayparafina/")
names = ["1 Bloque, Parafina", "2 Bloques, Parafina", "Aire-Arena",
        "Caja Vacía", "Caja + 1 Capa Arena", "Aire-Parafina",
        "Caja + 9 Capas Arena", "Caja + 3 Capas Arena", "3 Bloques, Parafina"]
direc_name="datosexperimentodensidadarenayparafina/"
energy, counts = [1]*len(files) ,[1]*len(files)
for x in range(len(files)):
    energy[x], counts[x]= np.loadtxt(direc_name+files[x], unpack=True)

print("----------------------")
print("Equivalencia:")
for x in range(len(names)):
    print("%s ---> %i"%(names[x], x))
print("----------------------")
#Procedimientos ==========================

gauss_fit(int(input("# Tabla >")))
"""
