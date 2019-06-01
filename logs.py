import matplotlib.pyplot as plt
import numpy as np
plt.style.use("seaborn-bright")

#Parafina
x = [0, 1.95, 3.9, 5.85] #largo en cm
I = [37553.107017, 34199.494249, 30250.258076, 23896.792959] #Intensidad cuentas

#Arena
#x=[0,1,3,9]
#I=[35333.066248, 30586.241669, 23197.905931, 14119.421695]
rango=np.linspace(min(x), max(x))
log_I = [np.log10(ii) for ii in I]
fit = np.polyfit(x, log_I, 1, full=True)

mu, b = fit[0]
res, = fit[1]
I_0=10**b
mu = mu*np.log(10)
print("============================")
print("Mu : %f \pm %f"%(-mu,res))
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(x, I, "-o", label="Datos Experimentales, Arena")
ax.plot(rango, I_0*np.exp(mu*rango), label="Ajuste Mínimos Cuadrados")
ax.set_yscale("log")
ax.set_yticks(np.linspace(min(I), max(I)+1, 11))

ax.set_xlabel("Espesor (cm)")
ax.set_ylabel("Intensidad (cuentas)")
plt.tight_layout()
plt.grid()
plt.legend()
plt.show()
