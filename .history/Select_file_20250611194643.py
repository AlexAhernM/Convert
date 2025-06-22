import customtkinter
from customtkinter import filedialog

def select_file(self):
    self.mapa_tkinter = None
    self.buttton_preview_kml.configure(state='normal')
    self.grab_set()
    ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo KML o KMZ", filetypes=[("Archivos KML/KMZ", "*.kml *.kmz")], parent=self)
    
    if ruta_archivo.endswith('.kmz'):
        # Conversión de KMZ a KML
        import zipfile
        import os
        ruta_archivo_kml = ruta_archivo.replace('.kmz', '.kml')
        with zipfile.ZipFile(ruta_archivo, 'r') as kmz:
            kmz.extractall()
            for file in kmz.namelist():
                if file.endswith('.kml'):
                    with open(file, 'r') as kml:
                        contenido_kml = kml.read()
                        with open(ruta_archivo_kml, 'w') as nuevo_kml:
                            nuevo_kml.write(contenido_kml)
                    # Elimina los archivos extraídos
                    for f in kmz.namelist():
                        os.remove(f)
    else:
        ruta_archivo_kml = ruta_archivo
    
    self.selectdata_entry.delete(0, customtkinter.END)
    self.selectdata_entry.insert(customtkinter.END, ruta_archivo_kml)
    
   
    
    self.buttton_preview_kml.configure(state ='normal')
            
    
           
    return ruta_archivo_kml