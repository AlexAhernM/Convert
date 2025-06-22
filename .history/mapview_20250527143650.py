import folium
import tkinter as tk
from PIL import Image, ImageTk
import webbrowser

# Crear un mapa
mapa = folium.Map(location=[40.7128, -74.0060], zoom_start=13)

# Agregar un punto con un icono personalizado
folium.Marker(
    location=[40.7128, -74.0060],
    icon=folium.CustomIcon('C:/Users/alex_/Downloads/Circle.png', icon_size=(50, 50))
).add_to(mapa)

# Guardar el mapa como un archivo HTML
mapa.save("mapa.html")

# Abrir el mapa en un navegador web
webbrowser.open("mapa.html")

# Crear una ventana de Tkinter
root = tk.Tk()

# Abrir una imagen
img = Image.open("D:/OneDrive/tuto_vscode/Conversion/amanecer.png")

# Convertir la imagen a un formato compatible con Tkinter
img_tk = ImageTk.PhotoImage(img)

# Mostrar la imagen en un Label
label = tk.Label(root, image=img_tk)
label.pack()

root.mainloop()