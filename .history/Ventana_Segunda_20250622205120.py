import os
import zipfile
import tempfile
import shutil
import customtkinter as ctk
from customtkinter import filedialog
from Preview_kml import procesar_archivo_kml
from Imagen_windows2 import ventana_segunda_imagen

class VentanaSegunda(ctk.CTkToplevel):
    """
    Ventana secundaria para seleccionar y previsualizar archivos KML o KMZ.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Convert KML Files")
        self.geometry('1300x600')
        self.color_ventana = 'snow'
        self.configure(fg_color=self.color_ventana)
        self.grab_set()

        self._crear_widgets()
        ventana_segunda_imagen(self)

    def _crear_widgets(self):
        """Crea y posiciona los elementos de la interfaz."""
        self.selectdata_boton = ctk.CTkButton(
            self,
            text='Select your KML File',
            width=200,
            fg_color='gray7',
            font=('Arial', 16),
            text_color='white',
            command=self._select_kml
        )
        self.selectdata_boton.place(x=40, y=40)

        self.selectdata_entry = ctk.CTkEntry(self, width=270, state='disabled')
        self.selectdata_entry.place(x=270, y=40)

        self.checkbox_altitude = ctk.CTkCheckBox(
            self,
            text='Get Altitude',
            text_color_disabled=self.color_ventana,
            border_width=1,
            border_color=self.color_ventana,
            text_color=self.color_ventana,
            state='disabled'
        )
        self.checkbox_altitude.place(x=140, y=100)

        self.boton_procesar_kml = ctk.CTkButton(
            self,
            text="Preview",
            width=510,
            fg_color='black',
            text_color='white',
            font=('Arial', 16),
            command=lambda: procesar_archivo_kml(self)
        )
        self.boton_procesar_kml.place(x=40, y=140)

        self.show_files_frame = ctk.CTkFrame(
            self,
            fg_color=self.color_ventana,
            width=510,
            height=320
        )
        self.show_files_frame.place(x=40, y=260)

    def _select_kml(self):
        """Permite al usuario seleccionar un archivo KML o KMZ y lo prepara para su procesamiento."""
        self.selectdata_entry.configure(state='normal')
        self.mapa_tkinter = None
        self.boton_procesar_kml.configure(state='normal')
        self.grab_set()

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo KML o KMZ",
            filetypes=[("Archivos KML/KMZ", "*.kml *.kmz")],
            parent=self
        )

        if not ruta_archivo:
            return  # El usuario canceló

        if ruta_archivo.endswith('.kmz'):
            ruta_archivo_kml = self._convertir_kmz_a_kml(ruta_archivo)
            if not ruta_archivo_kml:
                print("No se pudo extraer el archivo KML del KMZ.")
                return
        else:
            ruta_archivo_kml = ruta_archivo

        self.selectdata_entry.delete(0, ctk.END)
        self.selectdata_entry.insert(ctk.END, ruta_archivo_kml)
        self.selectdata_entry.configure(state='disabled')
        self.boton_procesar_kml.configure(state='normal')

    def _convertir_kmz_a_kml(self, ruta_kmz):
        """Extrae el archivo KML de un archivo KMZ y lo guarda en la misma carpeta."""
        try:
            with zipfile.ZipFile(ruta_kmz, 'r') as kmz:
                with tempfile.TemporaryDirectory() as temp_dir:
                    kmz.extractall(temp_dir)
                    for file in os.listdir(temp_dir):
                        if file.endswith('.kml'):
                            ruta_kml_extraido = os.path.join(temp_dir, file)
                            ruta_kml_destino = ruta_kmz.replace('.kmz', '.kml')
                            shutil.copy(ruta_kml_extraido, ruta_kml_destino)
                            return ruta_kml_destino
        except Exception as e:
            print(f"Error al convertir KMZ a KML: {e}")
            return None

    def close_windows(self):
        """Cierra la ventana actual."""
        self.destroy()
