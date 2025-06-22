import customtkinter as ctk
from tkintermapview import TkinterMapView
from tkinter import messagebox
from Transforma import parseo,  convierte, encontrar_placemark, procesar_placemark, get_zoom_level
from Crea_Checkboxes import checkboxes_convert
from genera import generate_files_intermediate
from Show_messages import show_messages
from Widget_destroy import widgets_destroy
from genera import generate_files_intermediate
import os
from PIL import Image, ImageTk

import pywinstyles


def procesar_archivo_kml(self):
    
    self.selectdata_boton.configure(state= 'normal')   #boton seleccionar archivo kml
    ruta_archivo_kml = self.selectdata_entry.get() 
    
    if ruta_archivo_kml: 
        self.selectdata_boton.configure(state='disabled' if ruta_archivo_kml is not None else 'normal')#desactiva boton seleccionar archivo si es que se selleciono alguno
        root_element_xml, altitud_value = parseo(ruta_archivo_kml, self.checkbox_altitude.get())
        doc, coords, coords_dec, layers, lat_centro, lon_centro, radio = convierte(root_element_xml, altitud_value)
        zoom_start = get_zoom_level(radio)
        print ('zoom=',  zoom_start, ', radio =', radio)
        update_preview(self, lat_centro, lon_centro, zoom_start, root_element_xml, altitud_value)
        self.buttton_procesar_archivo_kml.configure(state= 'disabled')
        confirmar_localizacion (self, doc, ruta_archivo_kml, coords, layers, coords_dec)
        
    else:
        messagebox.showerror("Error", "Por favor, seleccione un archivo KML")
            
    return doc, ruta_archivo_kml, coords, layers, coords_dec, altitud_value
        
def confirmar_localizacion(self, doc, ruta_archivo_kml, coords, layers, coords_dec):

    def respuesta_confirmacion(respuesta):
        if respuesta == "incorrecta":
            widgets_destroy(self)
          
        elif respuesta == "correcta":
            checkboxes_convert(self)
            self.checkbox_type.enable_checkboxes()
            self.boton_looks_good.destroy()
            self.boton_no_good.destroy()
            
            generate_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec) or ("", "", "")
                 
    
    self.label_mappreview = ctk.CTkLabel(self, text='Vision Preliminar Area Geografica a Procesar',
                      fg_color='gray69', text_color='Blue' , width = 290, height=25, corner_radius=6)
    
    self.label_mappreview.place(x=580, y=40) 
    
    self.boton_looks_good = ctk.CTkButton(self, text="Looks good", command=lambda: respuesta_confirmacion("correcta"),
                                                  fg_color='gray69', text_color='Blue' , width = 100, height=25,  corner_radius=6)
                                 
    self.boton_looks_good.place(x= 900, y=40) 
    
    
    self.boton_no_good = ctk.CTkButton(self, text="select another file", command=lambda: respuesta_confirmacion("incorrecta"),
                              fg_color='gray69', text_color='Blue' , width = 100, height=25 ,corner_radius=6)
    self.boton_no_good.place(x=1060, y =40) 
    
    
def update_preview(self, lat_centro, lon_centro, zoom_start, root_element_xml, altitud_value):
     # Destruye todos los widgets hijos de self.label3 (la imagen)
    for widget in self.label3.winfo_children():
        widget.destroy()
    self.label3.destroy()

    self.label3 = ctk.CTkLabel(self, text='', width=700, height=500)
    self.label3.place(x=580, y=80)
    
    self.mapa_tkinter = TkinterMapView(self.label3)
    self.mapa_tkinter.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    self.mapa_tkinter.set_position(lat_centro, lon_centro)
    self.mapa_tkinter.set_zoom(zoom_start)
    
    current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    plane_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "circle.png")).resize((15, 15)))
    #self.plane_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "plane.png")).resize((20, 20)))
    placemarks = encontrar_placemark(root_element_xml)
    for placemark in placemarks:
        _, _, coords_dec, _, layer_name = procesar_placemark(placemark, altitud_value, [], [], [])
        if len(coords_dec) == 1:  # Point
            marker = self.mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1], text=layer_name,
                                                font=("Times New Roman", 10, "bold"), text_color="blue",
                                                icon=plane_image)
                
        else:    
            puntos = [(point[0], point[1]) for point in coords_dec]
            self.mapa_tkinter.set_path(puntos, color="red", width=1)
            
def generate_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec):
    def on_click():
        messages = generate_files_intermediate(self, doc, ruta_archivo_kml, coords, layers, coords_dec)
        show_messages(self, messages)    
    self.boton_generate_files.configure(state= 'normal', command=on_click)
    #self.boton_looks_good.destroy()
    #self.boton_no_good.destroy()
           