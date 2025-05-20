import customtkinter
from transforma import parseo, encontrar_placemark, convierte, procesar_placemark, get_zoom_level
from tkintermapview import TkinterMapView
from tkinter import messagebox
from Convert_file import widgets_destroy
from Show_messages import show_messages
from genera import generate_files_intermediate
import pywinstyles


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
            
def generate_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec):
    def on_click():
        messages = generate_files_intermediate(self, doc, ruta_archivo_kml, coords, layers, coords_dec)
        show_messages(self, messages)
        
    self.boton_generate_files.configure(state= 'normal', command=on_click)           