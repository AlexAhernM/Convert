import customtkinter as ctk
from tkinter import messagebox
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
import os

from Transforma import parseo, obtener_coordenadas_capas, encontrar_placemark, procesar_placemark
from zoom import get_zoom_level
from Crea_Checkboxes import checkboxes_convert
from genera import generate_files
from Widget_destroy import widgets_destroy
from GeoProcessorBase import GeoProcessorBase  # Asegúrate de importar correctamente

class KMLProcessor(GeoProcessorBase):
    def procesar_archivo(self):
        ruta_archivo_kml = self.parent.selectdata_entry.get()

        if not ruta_archivo_kml:
            messagebox.showerror("Error", "Por favor, seleccione un archivo KML")
            return None

        self.parent.selectdata_boton.configure(state='disabled')
        root_element_xml, altitud_value = parseo(ruta_archivo_kml, self.parent.checkbox_altitude.get())

        doc, coords, coords_dec, layers, lat_centro, lon_centro, radio, utm_point_list, layer_names = obtener_coordenadas_capas(
            root_element_xml, altitud_value)

        zoom_start = get_zoom_level(radio)
        print('zoom -preview_kml =', zoom_start, ', radio preview_kml =', radio)

        self.update_preview(lat_centro, lon_centro, zoom_start, root_element_xml, altitud_value)

        self.parent.buttton_procesar_archivo_kml.configure(state='disabled')
        self.parent.selectdata_entry.configure(state='disabled')

        self.confirmar_localizacion(doc, ruta_archivo_kml, coords, utm_point_list, layer_names)

        return doc, ruta_archivo_kml, coords, layers, coords_dec, altitud_value

    def confirmar_localizacion(self, doc, ruta_archivo_kml, coords, utm_point_list, layer_names):
        def respuesta_confirmacion(respuesta):
            if respuesta == "incorrecta":
                widgets_destroy(self.parent)
            elif respuesta == "correcta":
                checkboxes_convert(self.parent)
                self.parent.checkbox_type.enable_checkboxes()
                self.parent.boton_looks_good.destroy()
                self.parent.boton_no_good.destroy()
                generate_files(self.parent, doc, ruta_archivo_kml, coords, utm_point_list, layer_names)

        self.parent.label_mappreview = ctk.CTkLabel(self.parent, text='Visión Preliminar Área Geográfica a Procesar',
                                                    fg_color='gray69', text_color='Blue', width=290, height=25,
                                                    corner_radius=6)
        self.parent.label_mappreview.place(x=580, y=40)

        self.parent.boton_looks_good = ctk.CTkButton(self.parent, text="Looks good",
                                                     command=lambda: respuesta_confirmacion("correcta"),
                                                     fg_color='gray69', text_color='Blue', width=100, height=25,
                                                     corner_radius=6)
        self.parent.boton_looks_good.place(x=900, y=40)

        self.parent.boton_no_good = ctk.CTkButton(self.parent, text="Select another file",
                                                  command=lambda: respuesta_confirmacion("incorrecta"),
                                                  fg_color='gray69', text_color='Blue', width=100, height=25,
                                                  corner_radius=6)
        self.parent.boton_no_good.place(x=1060, y=40)

    def update_preview(self, lat_centro, lon_centro, zoom_start, root_element_xml, altitud_value):
        if self.label3:
            for widget in self.label3.winfo_children():
                widget.destroy()
            self.label3.destroy()

        self.label3 = ctk.CTkLabel(self.parent, text='', width=700, height=500)
        self.label3.place(x=580, y=80)

        self.mapa_tkinter = TkinterMapView(self.label3)
        self.mapa_tkinter.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.mapa_tkinter.set_position(lat_centro, lon_centro)
        self.mapa_tkinter.set_zoom(zoom_start)

        current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        plane_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "circle.png")).resize((15, 15)))

        placemarks = encontrar_placemark(root_element_xml)
        for placemark in placemarks:
            _, _, coords_dec, _, layer_name = procesar_placemark(placemark, altitud_value, [], [], [])
            if len(coords_dec) == 1:
                self.mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1], text=layer_name,
                                             font=("Times New Roman", 10, "bold"), text_color="blue",
                                             icon=plane_image)
            else:
                puntos = [(point[0], point[1]) for point in coords_dec]
                self.mapa_tkinter.set_path(puntos, color="red", width=1)
