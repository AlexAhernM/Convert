import customtkinter
from customtkinter import filedialog
import zipfile
import os
import tempfile
import shutil

def select_kml(self):
    self.selectdata_entry.configure(state='normal')
    self.mapa_tkinter = None
    self.buttton_procesar_archivo_kml.configure(state='normal')
    self.grab_set()

    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo KML o KMZ",
        filetypes=[("Archivos KML/KMZ", "*.kml *.kmz")],
        parent=self
    )

    if not ruta_archivo:
        return

    ruta_archivo_kml = ruta_archivo

    if ruta_archivo.endswith('.kmz'):
        try:
            with zipfile.ZipFile(ruta_archivo, 'r') as kmz:
                with tempfile.TemporaryDirectory() as temp_dir:
                    kmz.extractall(temp_dir)
                    for file in kmz.namelist():
                        if file.endswith('.kml'):
                            ruta_kml_extraido = os.path.join(temp_dir, file)
                            ruta_archivo_kml = ruta_archivo.replace('.kmz', '.kml')
                            shutil.copy(ruta_kml_extraido, ruta_archivo_kml)
                            break
                    else:
                        print("No se encontró archivo .kml dentro del .kmz")
                        return
        except Exception as e:
            print(f"Error al procesar el archivo KMZ: {e}")
            return

    self.selectdata_entry.delete(0, customtkinter.END)
    self.selectdata_entry.insert(customtkinter.END, ruta_archivo_kml)
    self.selectdata_entry.configure(state='disabled')
    self.buttton_procesar_archivo_kml.configure(state='normal')

    return ruta_archivo_kml
