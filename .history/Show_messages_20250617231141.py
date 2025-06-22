import customtkinter
import os
import re
from Widget_destroy import widgets_destroy
from tkinter import messagebox



def show_messages(self, messages):
    msg_dxf, msg_shp, msg_xlx, msg_pdf = messages
    color_texto = 'black'
    font_texto = ('Arial', 12)
    
    ruta_dxf_match = re.search(r'C:\\.*\.dxf', msg_dxf)
    if ruta_dxf_match:
        ruta_dxf = ruta_dxf_match.group()
    else:
        ruta_dxf= None

    ruta_shp_match = re.search(r'C:\\.*\.shp', msg_shp)
    if ruta_shp_match:
        ruta_shp = ruta_shp_match.group()
    else:
        ruta_shp = None
    
    ruta_xlx_match = re.search(r'C:\\.*\.xlsx', msg_xlx)
    if ruta_xlx_match:
        ruta_xlx = ruta_xlx_match.group()
    else:
        ruta_xlx = None
        
    ruta_pdf_match = re.search(r'C:\\.*\.pdf', msg_pdf)
    if ruta_pdf_match:
        ruta_pdf = ruta_pdf_match.group()
    else:
        ruta_pdf = None
    
    def close_windows():
        self.destroy()
    
    
    self.label_mappreview.configure(text='Vision Preliminar Area Geografica Procesada')
    self.boton_limpiar = customtkinter.CTkButton(self, text="CLEAN", command=lambda: widgets_destroy(self),
                               fg_color='black', text_color='white' , width = 150, height=25 ,corner_radius=6)
    self.boton_limpiar.place(x=40, y = 520)
    
    self.boton_cerrar = customtkinter.CTkButton(self, text ="CLOSE",  command= close_windows,
                            fg_color='black', text_color='white' , width = 150, height=25 ,corner_radius=6)
    self.boton_cerrar.place(x = 300, y = 520)
    
         
    
    x = 20
    y = 10

    if msg_dxf:
        self.save_dxf = customtkinter.CTkButton(self.show_files_frame, text=msg_dxf, text_color=color_texto, fg_color="transparent", 
                                                hover_color=self.show_files_frame.cget("fg_color"), border_width=0,
                                                font =font_texto)
        self.label_dxf = customtkinter.CTkLabel(self.show_files_frame, text= 'CAD file has been generated in the following path : ')
        
        if ruta_dxf:
            self.label_dxf.place(x=x, y = y)
            self.save_dxf.configure(command=lambda ruta=ruta_dxf: abrir_archivo(ruta))
            self.save_dxf.place(x= x, y=y+20)
            y += 60  # Incrementa y para el próximo widget

    if msg_shp:
        self.save_shp = customtkinter.CTkButton(self.show_files_frame, text=msg_shp, text_color=color_texto, fg_color="transparent", 
                                                hover_color=self.show_files_frame.cget("fg_color"), border_width=0,
                                                font =font_texto)
        self.label_shp = customtkinter.CTkLabel(self.show_files_frame, text= 'Shapefile has been generated in the following path : ')
        
        if ruta_shp:
            self.label_shp.place(x=x, y = y)
            self.save_shp.configure(command=lambda ruta=ruta_shp: abrir_archivo(ruta))
            self.save_shp.place(x=x, y=y+20)
            y += 60  # Incrementa y para el próximo widget

    if msg_xlx:
        self.save_xlx = customtkinter.CTkButton(self.show_files_frame, text=msg_xlx, text_color=color_texto, fg_color="transparent",
                                                hover_color=self.show_files_frame.cget("fg_color"), border_width=0,
                                                font = font_texto)
        self.label_xlx = customtkinter.CTkLabel(self.show_files_frame, text= 'Excel file has been generated in the following path : ')
        
        if ruta_xlx:
            self.label_xlx.place(x=x, y = y)
            self.save_xlx.configure(command=lambda ruta=ruta_xlx: abrir_archivo(ruta))
            self.save_xlx.place(x=x, y=y+20)
            y += 60  # Incrementa y para el próximo widget
            
    if msg_pdf:
        self.save_pdf = customtkinter.CTkButton(self.show_files_frame, text=msg_pdf, text_color= color_texto, fg_color="transparent",
                                                hover_color=self.show_files_frame.cget("fg_color"), border_width=0,
                                                font = font_texto)
        self.label_pdf = customtkinter.CTkLabel(self.show_files_frame, text= 'PDF file has been generated in the following path : ')
        
        if ruta_pdf:
            self.label_pdf.place(x=x, y=y)
            self.save_pdf.configure(command=lambda ruta=ruta_pdf: abrir_archivo(ruta))
            self.save_pdf.place(x=x, y=y+20)
            y += 60  # Incrementa y para el próximo widget
        
   
def abrir_archivo(ruta):
    try:
        os.startfile(ruta)
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo {ruta}. Asegúrate de que haya una aplicación asociada con este tipo de archivo.")
        