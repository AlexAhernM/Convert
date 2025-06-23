import os
import zipfile
import tempfile
import shutil
import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image # Necesitas importar Image aquí también

# Asume que Preview_kml es un módulo separado y procesar_archivo_kml es una función allí
from Preview_kml import procesar_archivo_kml


class VentanaSegunda(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Convert KML Files")
        self.geometry('1300x600')
        self.color_ventana = 'snow'
        self.configure(fg_color=self.color_ventana)
        self.grab_set()

        self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Al inicializar, creamos los widgets originales
        self._crear_widgets()
        self._cargar_imagen_amanecer() # La imagen se carga al inicio

    def _crear_widgets(self):
        """
        Crea y posiciona los elementos de la interfaz en el estado original.
        Aquí deben ir TODOS los widgets que quieras que se muestren
        cuando la ventana está en su condición original/inicial.
        """
        # Botón y Entry de KML
        self.selectdata_boton = ctk.CTkButton(
            self, text='Select your KML File', width=200, fg_color='gray7',
            font=('Arial', 16), text_color='white', command=self._select_kml
        )
        self.selectdata_boton.place(x=40, y=40)

        self.selectdata_entry = ctk.CTkEntry(self, width=270, state='disabled')
        self.selectdata_entry.place(x=270, y=40)

        # Checkbox de Altitude
        self.checkbox_altitude = ctk.CTkCheckBox(
            self, text='Get Altitude', text_color_disabled=self.color_ventana,
            border_width=1, border_color=self.color_ventana,
            text_color=self.color_ventana, state='disabled'
        )
        self.checkbox_altitude.place(x=140, y=100)

        # Botón de Preview
        self.boton_procesar_kml = ctk.CTkButton(
            self, text="Preview", width=510, fg_color='black',
            text_color='white', font=('Arial', 16),
            command=lambda: procesar_archivo_kml(self)
        )
        self.boton_procesar_kml.place(x=40, y=140)

        # Frame para mostrar archivos
        self.show_files_frame = ctk.CTkFrame(
            self, fg_color=self.color_ventana, width=510, height=320
        )
        self.show_files_frame.place(x=40, y=260)
        
        # NOTA: La imagen no se crea aquí en _crear_widgets,
        # sino en _cargar_imagen_amanecer, para mantener esa lógica separada.

    def _cargar_imagen_amanecer(self):
        """
        Carga y muestra la imagen 'amanecer.png' en la ventana.
        Este método es responsable solo de la imagen.
        """
        ruta_imagen = os.path.join(self.base_path, "amanecer.png")

        try:
            if not os.path.exists(ruta_imagen):
                raise FileNotFoundError(f"No se encontró la imagen: {ruta_imagen}")
            
            imagen_data = Image.open(ruta_imagen)
            imagen_tk = ctk.CTkImage(light_image=imagen_data, dark_image=imagen_data, size=(700, 400))
            
            # Si el label ya existe, actualiza su imagen; si no, créalo.
            if hasattr(self, 'label_amanecer') and self.label_amanecer.winfo_exists():
                self.label_amanecer.configure(image=imagen_tk)
                self.label_amanecer.image = imagen_tk # Mantener referencia
            else:
                self.label_amanecer = ctk.CTkLabel(self, text='', image=imagen_tk, width=620, height=500)
                self.label_amanecer.image = imagen_tk 
                self.label_amanecer.place(x=580, y=100)
            
        except FileNotFoundError as e:
            print(f"Error (FileNotFound): {e}")
        except Exception as e:
            print(f"Error inesperado al cargar la imagen 'amanecer.png': {e}")



    def _select_kml(self):
        """Permite al usuario seleccionar un archivo KML o KMZ y lo prepara para su procesamiento."""
        self.selectdata_entry.configure(state='normal')
        self.mapa_tkinter = None # Asegúrate de que esta variable se usa consistentemente
        self.boton_procesar_kml.configure(state='normal')
        self.grab_set()

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo KML o KMZ",
            filetypes=[("Archivos KML/KMZ", "*.kml *.kmz")],
            parent=self
        )

        if not ruta_archivo:
            return  # El usuario canceló

        if ruta_archivo.lower().endswith('.kmz'): # .lower() para ser robusto a mayúsculas/minúsculas
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
                # Usar un directorio temporal para la extracción
                with tempfile.TemporaryDirectory() as temp_dir:
                    kmz.extractall(temp_dir)
                    # Buscar el primer archivo .kml en el directorio temporal
                    for file in os.listdir(temp_dir):
                        if file.lower().endswith('.kml'): # .lower() para ser robusto
                            ruta_kml_extraido = os.path.join(temp_dir, file)
                            
                            # Definir la ruta de destino del KML extraído.
                            # Podrías querer guardarlo en un directorio de salida específico
                            # o usar el mismo directorio que el KMZ original, pero con nombre .kml
                            # Aquí se guarda en el mismo directorio del KMZ, con el mismo nombre base.
                            directorio_kmz = os.path.dirname(ruta_kmz)
                            nombre_base_kmz = os.path.splitext(os.path.basename(ruta_kmz))[0]
                            ruta_kml_destino = os.path.join(directorio_kmz, f"{nombre_base_kmz}.kml")
                            
                            shutil.copy(ruta_kml_extraido, ruta_kml_destino)
                            return ruta_kml_destino
            print(f"Advertencia: No se encontró ningún archivo KML dentro de {ruta_kmz}")
            return None # Si no se encuentra ningún KML dentro del KMZ
        except zipfile.BadZipFile:
            print(f"Error: El archivo KMZ '{ruta_kmz}' no es un archivo ZIP válido o está corrupto.")
            return None
        except Exception as e:
            print(f"Error general al convertir KMZ a KML: {e}")
            return None

    def close_windows(self):
        """Cierra la ventana actual."""
        self.destroy()

# Ejemplo de cómo podrías instanciar VentanaSegunda (normalmente desde tu VentanaPrincipal)
if __name__ == "__main__":
    # Esto es solo para probar la VentanaSegunda de forma aislada.
    # En una aplicación real, sería lanzada desde VentanaPrincipal.
    root = ctk.CTk()
    root.withdraw() # Oculta la ventana principal dummy si no la necesitas ver

    app_segunda = VentanaSegunda(root)
    app_segunda.mainloop()