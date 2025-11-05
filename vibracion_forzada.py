import matplotlib
matplotlib.use('Qt5Agg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- 1. Definir los rangos para 'r' y 'zeta' ---
# Usamos los rangos que me diste:
# r = 0 a 4, en pasos de 0.1
# zeta = 0 a 1.5, en pasos de 0.1
r_vec = np.arange(0, 4 + 0.1, 0.1)
zeta_vec = np.arange(0, 1.5 + 0.1, 0.1)

# --- 2. Crear la malla 3D (El "lienzo") ---
# R y ZETA serán matrices 2D que contienen todas las combinaciones
R, ZETA = np.meshgrid(r_vec, zeta_vec)

# --- 3. Calcular el Eje Z para la Magnificación (M) ---
# Ecuación: M = 1 / sqrt( (1-r^2)^2 + (2*zeta*r)^2 )

# Calculamos el denominador
denominador_M = np.sqrt((1 - R**2)**2 + (2 * ZETA * R)**2)

# Evitamos la división por cero en el punto (r=1, zeta=0)
# 'np.errstate' ignora temporalmente el aviso de división por cero
with np.errstate(divide='ignore'):
    M = 1.0 / denominador_M

# ¡IMPORTANTE! El valor en (r=1, zeta=0) es infinito.
# Para que la gráfica sea legible, "cortamos" (clip) la altura
# máxima a un valor razonable, por ejemplo, 10.
M_clipped = np.clip(M, 0, 10)


# --- 4. Calcular el Eje Z para el Ángulo de Fase (phi) ---
# Ecuación: phi = arctan( (2*zeta*r) / (1-r^2) )

# Usamos np.arctan2(y, x) porque es más robusto que np.arctan(y/x).
# Maneja automáticamente el caso r=1 (x=0) y da el ángulo correcto (90°)
# También maneja r > 1 (x negativo) para darnos ángulos > 90°
phi_rad = np.arctan2( (2 * ZETA * R), (1 - R**2) )

# Convertimos de radianes a grados (0 a 180)
phi_deg = np.degrees(phi_rad)


# --- 5. Graficar ---

# Creamos una figura grande para poner ambas gráficas
fig = plt.figure(figsize=(20, 10))
fig.suptitle('Análisis de Vibración Forzada (M y φ)', fontsize=16)

# --- Gráfica 1: Factor de Magnificación (M) ---
ax1 = fig.add_subplot(1, 2, 1, projection='3d')

surf1 = ax1.plot_surface(R, ZETA, M_clipped, cmap='viridis', edgecolor='none')
ax1.set_title('1. Factor de Magnificación (M)', fontsize=14)
ax1.set_xlabel('Razón de Frecuencias (r)', labelpad=10)
ax1.set_ylabel('Amortiguamiento (ζ)', labelpad=10)
ax1.set_zlabel('Magnificación (M)')
ax1.set_zlim(0, 10) # Fijamos el límite Z de 0 a 10 (por el clip)
fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10, pad=0.1)

# Ajustamos el ángulo de vista inicial
ax1.view_init(elev=20., azim=-120)


# --- Gráfica 2: Ángulo de Fase (phi) ---
ax2 = fig.add_subplot(1, 2, 2, projection='3d')

surf2 = ax2.plot_surface(R, ZETA, phi_deg, cmap='twilight_shifted', edgecolor='none')
ax2.set_title('2. Ángulo de Fase (φ)', fontsize=14)
ax2.set_xlabel('Razón de Frecuencias (r)', labelpad=10)
ax2.set_ylabel('Amortiguamiento (ζ)', labelpad=10)
ax2.set_zlabel('Ángulo de Fase (φ) [grados]')
ax2.set_zlim(0, 180) # La fase va de 0 a 180 grados
fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=10, pad=0.1)

# Ajustamos el ángulo de vista inicial
ax2.view_init(elev=20., azim=-120)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()