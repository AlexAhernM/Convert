import customtkinter
import os
import re
from tkinter import messagebox


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
    
    self.label_mappreview.configure(text='Vision Preliminar Area Geografica Procesada')
    
    x = 20
    y = 20

    if msg_dxf:
        self.save_dxf = customtkinter.CTkButton(self.show_files_frame, text=msg_dxf, text_color='firebrick1', fg_color="transparent", hover_color=self.show_files_frame.cget("fg_color"), border_width=0)
        self.label_dxf = customtkinter.CTkLabel(self.show_files_frame, text= 'CAD file has been generated in the following path : ')
        
        if ruta_dxf:
            self.label_dxf.place(x=x, y = y)
            self.save_dxf.configure(command=lambda ruta=ruta_dxf: abrir_archivo(ruta))
            self.save_dxf.place(x= x, y=y+20)
            y += 60  # Incrementa y para el próximo widget

    if msg_shp:
        self.save_shp = customtkinter.CTkButton(self.show_files_frame, text=msg_shp, text_color='blue', fg_color="transparent", hover_color=self.show_files_frame.cget("fg_color"), border_width=0)
        self.label_shp = customtkinter.CTkLabel(self.show_files_frame, text= 'Shapefile has been generated in the following path : ')
        
        if ruta_shp:
            self.label_shp.place(x=x, y = y)
            self.save_shp.configure(command=lambda ruta=ruta_shp: abrir_archivo(ruta))
            self.save_shp.place(x=x, y=y+20)
            y += 60  # Incrementa y para el próximo widget

    if msg_xlx:
        self.save_xlx = customtkinter.CTkButton(self.show_files_frame, text=msg_xlx, text_color='PaleGreen4', fg_color="transparent", hover_color=self.show_files_frame.cget("fg_color"), border_width=0)
        self.label_xlx = customtkinter.CTkLabel(self.show_files_frame, text= 'Excel file has been generated in the following path : ')
        
        if ruta_xlx:
            self.label_xlx.place(x=x, y = y)
            self.save_xlx.configure(command=lambda ruta=ruta_xlx: abrir_archivo(ruta))
            self.save_xlx.place(x=x, y=y+20)
            y += 60  # Incrementa y para el próximo widget
            
   
def abrir_archivo(ruta):
    try:
        os.startfile(ruta)
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo {ruta}. Asegúrate de que haya una aplicación asociada con este tipo de archivo.")
        