# -*- coding: utf-8 -*-

import re
import numpy as np
import matplotlib.pyplot as plt


with open("correlation_matrix_merged.txt", "r") as file:
    lines = file.readlines()

# Obtener los nombres de las columnas y los valores de la matriz
column_names = re.findall(r"'(.*?)'", lines[0])
correlation_matrix = np.loadtxt([line.strip().replace("[","").replace("]","").replace(",", " ") for line in lines[1:]])
column_names = [name for name in column_names if name not in ["type", "features"]]

fig, ax = plt.subplots()

# Generar el mapa de calor con la matriz de correlación
im = ax.imshow(correlation_matrix, cmap="coolwarm")

# Configurar los ticks de los ejes
ax.set_xticks(np.arange(len(column_names)))
ax.set_yticks(np.arange(len(column_names)))

# Configurar las etiquetas de los ejes
ax.set_xticklabels(column_names, rotation=45, ha="right")
ax.set_yticklabels(column_names)

# En caso de querer mostrar valores en las celdas, decomentar. Se monta mucho barullo y no se ve bien, así que prescindimos de ello.
"""
for i in range(len(column_names)):
    for j in range(len(column_names)):
        text = ax.text(j, i, round(correlation_matrix[i, j], 2), ha="center", va="center", color="black")
"""

cbar = ax.figure.colorbar(im, ax=ax)

ax.set_title("Matriz de correlación")
plt.tight_layout()
plt.show()  # Mostrar el gráfico. Lo puedo guardar desde la GUI haciendo zoom para que se vea el nombre de las variables.
