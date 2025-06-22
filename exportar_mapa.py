
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
from build_files import FileCreator
from Show_messages import ShowMessages
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

    # Agregar marca de agua
    draw = ImageDraw.Draw(image)
    texto_marca = "© TuNombre o Proyecto"
    fuente = ImageFont.load_default()
    ancho, alto = image.size
    margen = 10
    texto_ancho, texto_alto = draw.textsize(texto_marca, font=fuente)
    posicion = (ancho - texto_ancho - margen, alto - texto_alto - margen)
    draw.text(posicion, texto_marca, fill=(255, 255, 255), font=fuente)

    # Usar FileCreator para generar la ruta de guardado
    file_creator = FileCreator(None, None)
    ruta_guardado = file_creator._generar_ruta_archivo(self.ruta_archivo_kml, '.png')

    # Guardar la imagen
    image.save(ruta_guardado)
    messagebox.showinfo("Éxito", f"Imagen guardada en:\n{ruta_guardado}")

    # Mostrar la imagen exportada en la interfaz
    show = ShowMessages(self)
    show.show_single_file(ruta_guardado, "PNG")
