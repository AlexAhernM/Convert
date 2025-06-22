import os
import customtkinter as ctk
from PIL import Image
from Ventana_kml import VentanaSegunda
from Ventana_coord import VentanaTercera

class VentanaPrincipal(ctk.CTk):
    """
    Ventana principal del programa Geo Convert de Ambylog.
    Permite al usuario elegir entre dos tipos de conversión geoespacial.
    """

    def __init__(self):
        super().__init__()
        self.title("Geo Convert Program by Ambylog")
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color='white')

        self._crear_botones()
        self._cargar_imagenes()

    def _crear_botones(self):
        """Crea los botones principales de la interfaz."""
        self.boton_inic1 = ctk.CTkButton(
            self,
            text='Convert your KML/KMZ files into   \n CAD, Shapefile or Excel',
            font=('Arial', 36),
            text_color='white',
            width=520,
            height=140,
            fg_color='salmon3',
            hover_color='salmon4',
            command=lambda: VentanaSegunda(self),
            corner_radius=20
        )
        self.boton_inic1.configure(cursor='hand2')
        self.boton_inic1.place(x=30, y=200)

        self.boton_inic2 = ctk.CTkButton(
            self,
            text='Convert coordinates (in Excel) into\n KML, CAD or Shapefile',
            font=('Arial', 36),
            text_color='white',
            width=520,
            height=140,
            fg_color='green3',
            hover_color='green4',
            command=lambda: VentanaTercera(self),
            corner_radius=20
        )
        self.boton_inic2.configure(cursor='hand2')
        self.boton_inic2.place(x=30, y=400)

    def _cargar_imagenes(self):
        """Carga y muestra las imágenes en la interfaz."""
        try:
            ruta_mundo = os.path.join("Convert", "mundo.png")
            imagen1 = Image.open(ruta_mundo)
            imagen_tk1 = ctk.CTkImage(light_image=imagen1, dark_image=imagen1, size=(760, 360))
            label1 = ctk.CTkLabel(self, image=imagen_tk1, text="")
            label1.image = imagen_tk1
            label1.place(x=700, y=180)
        except FileNotFoundError:
            print(f"No se encontró la imagen: {ruta_mundo}")

        try:
            ruta_logo = os.path.join("Conversion", "AMBYLOG.png")
            imagen2 = Image.open(ruta_logo)
            imagen_tk2 = ctk.CTkImage(light_image=imagen2, dark_image=imagen2, size=(240, 100))
            label2 = ctk.CTkLabel(self, image=imagen_tk2, text="")
            label2.image = imagen_tk2
            label2.place(x=30, y=20)
        except FileNotFoundError:
            print(f"No se encontró la imagen: {ruta_logo}")

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        self.mainloop()


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.run()
