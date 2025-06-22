import folium
import tkinter as tk

# Crear un mapa
mapa = folium.Map(location=[40.7128, -74.0060], zoom_start=13)

# Agregar un punto con un icono personalizado
folium.Marker(
    location=[40.7128, -74.0060],
    icon=folium.CustomIcon('C:/Users/alex_/Downloads/Circle.png', icon_size=(50, 50))
).add_to(mapa)

# Guardar el mapa como un archivo HTML
mapa.save("mapa.html")

import folium
import matplotlib.pyplot as plt

# Crear un mapa
mapa = folium.Map(location=[40.7128, -74.0060], zoom_start=13)

# Agregar un punto con un icono personalizado
folium.Marker(
    location=[40.7128, -74.0060],
    icon=folium.Icon(color='red', icon='cloud')
).add_to(mapa)

# Guardar el mapa como una imagen
mapa.save("mapa.html")

# Leer la imagen del mapa
import webbrowser
import os
webbrowser.open('file://' + os.path.realpath("mapa.html"))

# Otra forma es utilizar mplleaflet
import mplleaflet
import matplotlib.pyplot as plt

root = tk.Tk
fig, ax = plt.subplots()
mplleaflet.show(fig=fig, path='mapa.html')

from PIL import Image, ImageTk

# Abrir la imagen
img = Image.open("mapa.png")

# Convertir la imagen a un formato compatible con Tkinter
img_tk = ImageTk.PhotoImage(img)

# Mostrar la imagen en un Label
label = tk.Label(root, image=img_tk)
label.pack()

app = root
root.mainloop