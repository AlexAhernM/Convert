import customtkinter
from customtkinter import filedialog

def select_file(self):
    self.mapa_tkinter = None
    self.button_preview.configure(state= 'normal')
    self.grab_set()
    ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
    self.grab_set()
    self.selectdata_entry.delete(0, customtkinter.END)
    self.selectdata_entry.insert(customtkinter.END, ruta_archivo_kml)
    self.selectdata_boton.configure(state= 'disabled')
    
    
    
    #for widget in self.approval_frame.winfo_children():            
    #    widget.destroy()
    
    self.deseleccionar()
    self.convert_file.configure(state= 'disabled')
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