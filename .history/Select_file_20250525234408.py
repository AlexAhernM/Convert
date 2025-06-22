import customtkinter
from customtkinter import filedialog

def select_file(self):
    self.mapa_tkinter = None
    self.button_preview.configure(state= 'normal')
    self.ventana_segunda.grab_set()
    ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")], parent=self.ventana_segunda)
    self.selectdata_entry.delete(0, customtkinter.END)
    self.selectdata_entry.insert(customtkinter.END, ruta_archivo_kml)
    
   
    
    self.button_preview.configure(state ='normal')
            
    try:
        self.save_dxf.destroy()
    except AttributeError:
        pass
       
    try:
        self.save_shp.destroy()
    except AttributeError:
        pass   
       
    try:
        self.save_xlx.destroy()
    except AttributeError:
        pass      
           
    return ruta_archivo_kml