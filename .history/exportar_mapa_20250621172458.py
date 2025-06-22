
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from build_files import FileCreator

import io

def exportar_mapa_como_imagen(self):
    if not hasattr(self, 'mapa_tkinter'):
        messagebox.showerror("Error", "No hay mapa para exportar.")
        return

    # Exportar como PostScript
    ps_data = self.mapa_tkinter.canvas.postscript(colormode='color')

    # Convertir a imagen con PIL
    image = Image.open(io.BytesIO(ps_data.encode('utf-8')))
    image = image.convert("RGB")

    # Guardar como PNG
    
    
# Usar FileCreator para generar la ruta de guardado
    file_creator = FileCreator(None, None)
    ruta_guardado = file_creator._generar_ruta_archivo(ruta_archivo_kml, '.png')

    #Guardar la imagen
    image.save(ruta_guardado)
    messagebox.showinfo("Éxito", f"Imagen guardada en:\n{ruta_guardado}")

   
