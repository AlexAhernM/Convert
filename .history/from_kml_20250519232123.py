
import customtkinter
from customtkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from tkintermapview import TkinterMapView
from transforma import parseo, encontrar_placemark, convierte, procesar_placemark, get_zoom_level
from genera import generate_files_intermediate
from Convert_file import convert_file, widgets_destroy
import os
import re
import requests
from PIL import Image
import pywinstyles
from io import BytesIO


class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values, enabled=True, width=650, height = 180):
        super().__init__(master, width=width, height= height)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            inputdata = customtkinter.CTkCheckBox(self, text=value)
            inputdata.grid(row=i, column=0, padx=10, pady= (10, 5), sticky="w")
            inputdata.configure(border_width = 1, border_color = 'black')
            if not enabled:
                inputdata.configure(state="disabled")
            self.checkboxes.append(inputdata)
            
    def get(self):
        checked_checkboxes = []
        for inputdata in self.checkboxes:
            if inputdata.get() == 1:
                checked_checkboxes.append(inputdata.cget("text"))
        return checked_checkboxes
    
    def enable_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.configure(state="normal")
    
    def disable_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.deselect()
            checkbox.configure(state="disabled")     

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Geo Convert Program by Ambylog")
        self.after(0, lambda:app.state('zoomed'))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
                
        # FRAME: ROW 0 - SELECT FILE
        self.selectfile_frame = customtkinter.CTkFrame(self, width=550, height=180)
        self.selectfile_frame.grid(row=0, column = 0, padx=10, pady=10, sticky='w')
        self.selectfile_frame.grid_propagate(False)
        
        
        # FRAME: ROW 0 - INTERMEDIO RADIOBUTTOMS - TIPO DE FORMATO A TRANSFORMAR
        self.intermedio_frame = customtkinter.CTkFrame(self, width=280, height=180)
        self.intermedio_frame.grid(row=0, column = 1, padx=10, pady=10, sticky='e')
        self.intermedio_frame.grid_propagate(False)
        
        self.tipo_geo = customtkinter.StringVar()
        self.rbuttomkml = customtkinter.CTkRadioButton(self.intermedio_frame, text=" From KML", variable=self.tipo_geo, value="KML",
                                                       command=self.habilitar_boton)
        self.rbuttomkml.grid(row=0, column=0, padx=10, pady=(20,10),  sticky='w')
        
        self.rbuttomcord = customtkinter.CTkRadioButton(self.intermedio_frame, text="From Coords", variable=self.tipo_geo, value="Coordenadas",
                                                        command=self.habilitar_boton)
        self.rbuttomcord.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        self.convert_file = customtkinter.CTkButton(self.intermedio_frame, text='Convert File', command=lambda: convert_file(self))
        self.convert_file.grid(row=2, column=0, padx=(65,0), pady=(44,0), sticky='w')
        self.convert_file.configure(state='disabled')
        self.habilitar()
        # FRAME: ROW 0 -  CHECKBOXS Y MESSAGES
        
        self.checkbox_frame = customtkinter.CTkFrame(self, width=650, height=180)
        self.checkbox_frame.grid(row=0, column=2, padx =10, pady=10, sticky = 'nsew' )
        
        # FRAME: ROW 2 - MAP PREVIEW
        # Creación del frame de vista previa
        self.preview_frame = customtkinter.CTkFrame(self,  fg_color='white')
        self.preview_frame.grid(row=2, column=0, padx=10, pady=5, columnspan=4, sticky='nsew')
        self.preview_frame.grid_columnconfigure(0, weight=1)
        
        self.show_image_in_preview() 
        self.show_image_in_labels()

    def deseleccionar(self):
        self.rbuttomkml.configure(state='disabled')
        self.rbuttomcord.configure(state='disabled') 
        self.tipo_geo.set("")
        
    def habilitar (self):
        self.rbuttomkml.configure(state='normal')
        self.rbuttomcord.configure(state='normal') 
        
    def habilitar_boton(self):
        if self.tipo_geo.get() == "KML":
            self.convert_file.configure(state='normal')
        elif self.tipo_geo.get() == "Coordenadas":
            self.convert_file.configure(state='normal')  # o cualquier otra lógica que desees aplicar
        else:
            self.convert_file.configure(state='disabled')

    def show_image_in_preview(self):

        images_config = [
            {"url": "https://raw.githubusercontent.com/AlexAhernM/Converter/master/earth1.png", "size": (1440, 530)},
            {"url": "https://raw.githubusercontent.com/AlexAhernM/Converter/master/Atardecer_anf.png", "size": (300, 180)},
            {"url": "https://raw.githubusercontent.com/AlexAhernM/Converter/master/amanecer.png", "size": (300, 180)}
        ]
        
         # Descargar las imágenes y crear CTkImage
        self.preview_images = []
        for config in images_config:
            response = requests.get(config["url"])
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                preview_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=config["size"])
                self.preview_images.append(preview_image)
            else:
                print(f"Error al descargar la imagen: {response.status_code}")
                
        # Crear y mostrar el CTkLabel (si no existe)
        
        self.preview_label1 = customtkinter.CTkLabel(self.preview_frame, text="", image=self.preview_images[0])
        self.preview_label1.pack(expand = True, fill ='both')
        
    def show_image_in_labels(self):
        self.preview_label2 = customtkinter.CTkLabel(self.selectfile_frame, text="", image=self.preview_images[1])
        self.preview_label2.grid(row=0, column=0, padx=120, pady=2, sticky='nsew')
        
        self.preview_label3 = customtkinter.CTkLabel(self.checkbox_frame, text="", image=self.preview_images[2])
        self.preview_label3.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        

         
def select_file(self):
    self.mapa_tkinter = None
    self.button_preview.configure(state= 'normal')
    self.convert_file.configure(state='disabled')
    if self.tipo_geo.get() in ["KML", None]:
        ruta_archivo_kml = filedialog.askopenfilename(title="Seleccionar archivo KML", filetypes=[("Archivo KML", "*.kml")])
        self.selectdata_entry.delete(0, customtkinter.END)
        self.selectdata_entry.insert(customtkinter.END, ruta_archivo_kml)
        self.selectdata_boton.configure(state= 'disabled')
    else:
        ruta_archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivo Excel", "*.xlsx")])
        self.selectdata_entry.delete(0, customtkinter.END)
        self.selectdata_entry.insert(customtkinter.END, ruta_archivo_excel)
    
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

def update_preview(self, lat_centro, lon_centro, zoom_start, root, altitud_value):
    for widget in self.preview_frame.winfo_children():            
        widget.destroy()
    
    self.mapa_tkinter = TkinterMapView(self.preview_frame)
    self.mapa_tkinter.pack(expand=True, fill='both')
    self.mapa_tkinter.set_position(lat_centro, lon_centro)
    self.mapa_tkinter.set_zoom(zoom_start)

    placemarks = encontrar_placemark(root)
    for placemark in placemarks:
        _, _, coords_dec, _, layer_name = procesar_placemark(placemark, altitud_value, [], [], [])
        if len(coords_dec) == 1:  # Point
            marker = self.mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1], text=layer_name,
                                                font=("Times New Roman", 8, "bold"), text_color="blue")
            self.mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1])
                
        else:    
            puntos = [(point[0], point[1]) for point in coords_dec]
            self.mapa_tkinter.set_path(puntos, color="red", width=1)
           
    
def button_preview(self):
    self.selectdata_boton.configure(state= 'disabled')
    ruta_archivo_kml = self.selectdata_entry.get()
    print(ruta_archivo_kml)
    if ruta_archivo_kml: 
        
        root, altitud_value = parseo(ruta_archivo_kml, self.checkbox_altitude.get())
        doc, coords, coords_dec, layers, lat_centro, lon_centro, radio = convierte(root, altitud_value)
        zoom_start = get_zoom_level(radio)
        update_preview(self, lat_centro, lon_centro, zoom_start, root, altitud_value)
        self.button_preview.configure(state= 'disabled')
        confirmar_localizacion (self, doc, ruta_archivo_kml, coords, layers, coords_dec)
        
    else:
        messagebox.showerror("Error", "Por favor, seleccione un archivo KML")
            
    return doc, ruta_archivo_kml, coords, layers, coords_dec, altitud_value
        
def confirmar_localizacion(self, doc, ruta_archivo_kml, coords, layers, coords_dec):
    approval_frame = customtkinter.CTkFrame(self.mapa_tkinter, height=40, fg_color="#000001", bg_color="#000001")
    approval_frame.grid (row=0, column =0, padx=(60,0), pady=(0,520), columnspan=3,sticky='we')
    pywinstyles.set_opacity(approval_frame, color="#000001") 

    def respuesta_confirmacion(respuesta):
        if respuesta == "incorrecta":
            self.button_preview.configure(state='disabled')
            self.boton_looks_good.configure(state='disabled')
            self.boton_no_good.configure(state='disabled')
            widgets_destroy(self)
            
        elif respuesta == "correcta":
            self.checkbox_type.enable_checkboxes()
            self.boton_looks_good.configure(state='disabled')
            self.boton_no_good.configure(state='disabled')
            generate_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec) or ("", "", "")
                 
    
    label_mappreview = customtkinter.CTkLabel(approval_frame, text='Vision Preliminar Area Geografica a Procesar', 
                                                       fg_color='gray69', text_color='Blue' , width = 290, height=25, corner_radius=6)
    label_mappreview.grid(row=0,column=0,padx=10, pady =(5,500)) 
    
    
    
    self.boton_looks_good = customtkinter.CTkButton(approval_frame, text="Looks good", command=lambda: respuesta_confirmacion("correcta"),
                                                  fg_color='gray69', text_color='Blue' , width = 100, height=25,  corner_radius=6)
                                 
    self.boton_looks_good.grid(row=0,column=1,padx=(600,0), pady =(5,500)) 
    
    
    self.boton_no_good = customtkinter.CTkButton(approval_frame, text="select another file", command=lambda: respuesta_confirmacion("incorrecta"),
                              fg_color='gray69', text_color='Blue' , width = 100, height=25 ,corner_radius=6)
    self.boton_no_good.grid(row=0,column=2,padx=50, pady =(5,500)) 
    
  
def generate_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec):
    def on_click():
        messages = generate_files_intermediate(self, doc, ruta_archivo_kml, coords, layers, coords_dec)
        show_messages(self, messages)
        
    self.boton_generate_files.configure(state= 'normal', command=on_click)
                                                            

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
        self.save_dxf = customtkinter.CTkButton(self.checkbox_type, text=msg_dxf, text_color='firebrick1', fg_color="transparent", hover_color=self.checkbox_type.cget("fg_color"), border_width=0)
        
        if ruta_dxf:
            self.save_dxf.configure(command=lambda ruta=ruta_dxf: abrir_archivo(ruta))
            self.save_dxf.grid(row=0, column=1, padx=5, pady=(10,5), sticky='w')

    if msg_shp:
        self.save_shp = customtkinter.CTkButton(self.checkbox_type, text=msg_shp, text_color='blue', fg_color="transparent", hover_color=self.checkbox_type.cget("fg_color"), border_width=0)
        
        if ruta_shp:
            self.save_shp.configure(command=lambda ruta=ruta_shp: abrir_archivo(ruta))
            self.save_shp.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    if msg_xlx:
        self.save_xlx = customtkinter.CTkButton(self.checkbox_type, text=msg_xlx, text_color='PaleGreen4', fg_color="transparent", hover_color=self.checkbox_type.cget("fg_color"), border_width=0)
        
        if ruta_xlx:
            self.save_xlx.configure(command=lambda ruta=ruta_xlx: abrir_archivo(ruta))
            self.save_xlx.grid(row=2, column=1, padx=5, pady=5, sticky='w')
            

    widgets_destroy(self) 

def abrir_archivo(ruta):
    try:
        os.startfile(ruta)
    except OSError as e:
        messagebox.showerror("Error", f"No se pudo abrir el archivo {ruta}. Asegúrate de que haya una aplicación asociada con este tipo de archivo.")
          

    
app = App()
app.mainloop()