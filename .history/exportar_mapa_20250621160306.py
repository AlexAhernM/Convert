
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
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
    ruta_guardado = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")],
        title="Guardar imagen del mapa"
    )

    if ruta_guardado:
        image.save(ruta_guardado)
        messagebox.showinfo("Éxito", f"Imagen guardada en:
{ruta_guardado}")

# Ejemplo de cómo agregar un botón en la interfaz para llamar a esta función
class VentanaEjemplo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ejemplo Exportar Mapa")
        self.geometry('800x600')
        
        self.boton_exportar_imagen = ctk.CTkButton(
            self, text="Export Map as Image",
            command=lambda: exportar_mapa_como_imagen(self),
            fg_color='gray69', text_color='Blue', width=150, height=25, corner_radius=6
        )
        self.boton_exportar_imagen.place(x=580, y=550)
        
        # Aquí podrías agregar el mapa y otros widgets necesarios

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = VentanaEjemplo()
    app.run()
