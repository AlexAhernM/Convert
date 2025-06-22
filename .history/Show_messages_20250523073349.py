import customtkinter
import os
import re
from tkinter import messagebox
from Widget_destroy import widgets_destroy

def show_messages(self, messages):
    msg_dxf, msg_shp, msg_xlx = messages
    
    ruta_dxf_match = re.search(r'C:\\.*\.dxf', msg_dxf)
    if ruta_dxf_match:
        ruta_dxf = ruta_dxf_match.group()
    else:
        ruta_dxf = None

    ruta_shp_match = re.search(r'C:\\.*\.shp', msg_shp)
    if ruta_shp_match:
        ruta_shp = ruta_shp_match.group()
    else:
        ruta_shp = None
    
    ruta_xlx_match = re.search(r'C:\\.*\.xlsx', msg_xlx)
    print('se paso super bien  ', msg_xlx)
    if ruta_xlx_match:
        ruta_xlx = ruta_xlx_match.group()
        print('hasta aca super bien  ',  msg_xlx)
    else:
        ruta_xlx = None
    
    if msg_dxf:
        self.save_dxf = customtkinter.CTkButton(self.checkbox_frame, text=msg_dxf, text_color='firebrick1', fg_color="transparent", hover_color=self.checkbox_type.cget("fg_color"), border_width=0)
        
        if ruta_dxf:
            self.save_dxf.configure(command=lambda ruta=ruta_dxf: abrir_archivo(ruta))
            self.save_dxf.grid(row=0, column=1, padx=5, pady=(10,5), sticky='w')

    if msg_shp:
        self.save_shp = customtkinter.CTkButton(self.checkbox_frame, text=msg_shp, text_color='blue', fg_color="transparent", hover_color=self.checkbox_type.cget("fg_color"), border_width=0)
        
        if ruta_shp:
            self.save_shp.configure(command=lambda ruta=ruta_shp: abrir_archivo(ruta))
            self.save_shp.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    if msg_xlx:
        self.save_xlx = customtkinter.CTkButton(self.checkbox_frame, text=msg_xlx, text_color='PaleGreen4', fg_color="transparent", hover_color=self.checkbox_type.cget("fg_color"), border_width=0)
        
        if ruta_xlx:
            self.save_xlx.configure(command=lambda ruta=ruta_xlx: abrir_archivo(ruta))
            self.save_xlx.grid(row=2, column=1, padx=5, pady=5, sticky='w')
            
    
       
    
def abrir_archivo(ruta):
    try:
        os.startfile(ruta)
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo {ruta}. Asegúrate de que haya una aplicación asociada con este tipo de archivo.")