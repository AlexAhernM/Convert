import customtkinter as ctk
from tkinter import messagebox, PhotoImage
from tkintermapview import TkinterMapView
from PIL import Image, ImageTk
import os

# Importa tus módulos
from Transforma import parseo, obtener_coordenadas_capas, encontrar_placemark, procesar_placemark
from zoom import get_zoom_level
from Crea_Checkboxes import checkboxes_convert
from genera import generate_files
from Widget_destroy import widgets_destroy


# Constantes para colores y fuentes (mejoran la mantenibilidad)
COLOR_BACKGROUND_LABEL = 'gray69'
COLOR_TEXT_LABEL = 'blue'
FONT_MARKER = ("Times New Roman", 10, "bold")
IMAGE_PLANE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "circle.png")


class KMLProcessor:
    def __init__(self, parent):
        self.parent = parent
        self.mapa_tkinter = None
        self.label_map_container = None # Renombrado para mayor claridad
        self.plane_image = None # Para cargar la imagen una sola vez

        # Cargar la imagen del marcador una sola vez
        try:
            self.plane_image = ImageTk.PhotoImage(Image.open(IMAGE_PLANE_PATH).resize((15, 15)))
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró la imagen del marcador: {IMAGE_PLANE_PATH}")
            self.plane_image = None # Asegúrate de que sea None si falla

    def procesar_archivo(self):
        ruta_archivo_kml = self.parent.selectdata_entry.get()

        if not ruta_archivo_kml:
            messagebox.showerror("Error", "Por favor, seleccione un archivo KML.")
            return None

        # Validar si el archivo existe y es un KML/KMZ básico
        if not os.path.exists(ruta_archivo_kml):
            messagebox.showerror("Error", f"El archivo no existe: {ruta_archivo_kml}")
            return None
        if not (ruta_archivo_kml.endswith(".kml") or ruta_archivo_kml.endswith(".kmz")):
            messagebox.showerror("Error", "El archivo seleccionado no es un KML o KMZ válido.")
            return None

        self.parent.selectdata_boton.configure(state='disabled')

        try:
            root_element_xml, altitud_value = parseo(ruta_archivo_kml, self.parent.checkbox_altitude.get())
        except Exception as e:
            messagebox.showerror("Error de parseo", f"No se pudo procesar el archivo KML: {e}")
            self.parent.selectdata_boton.configure(state='normal') # Re-habilitar botón
            return None

        try:
            doc, coords, coords_dec, layers, lat_centro, lon_centro, radio, utm_point_list, layer_names = \
                obtener_coordenadas_capas(root_element_xml, altitud_value)
        except Exception as e:
            messagebox.showerror("Error al obtener coordenadas", f"No se pudieron obtener las coordenadas o capas: {e}")
            self.parent.selectdata_boton.configure(state='normal') # Re-habilitar botón
            return None

        zoom_start = get_zoom_level(radio)
        print(f'zoom -preview_kml = {zoom_start}, radio preview_kml = {radio}') # Usar f-string

        self.update_preview(lat_centro, lon_centro, zoom_start, root_element_xml, altitud_value)

        # Deshabilitar elementos después de una previsualización exitosa
        self.parent.buttton_procesar_archivo_kml.configure(state='disabled')
        self.parent.selectdata_entry.configure(state='disabled')

        self.confirmar_localizacion(doc, ruta_archivo_kml, coords, utm_point_list, layer_names)

        return doc, ruta_archivo_kml, coords, layers, coords_dec, altitud_value

    def confirmar_localizacion(self, doc, ruta_archivo_kml, coords, utm_point_list, layer_names):
        def respuesta_confirmacion(respuesta):
            if respuesta == "incorrecta":
                widgets_destroy(self.parent)
                # Re-habilitar y limpiar campos si se selecciona otro archivo
                self.parent.selectdata_entry.configure(state='normal')
                self.parent.selectdata_entry.delete(0, ctk.END)
                self.parent.selectdata_boton.configure(state='normal')
                self.parent.buttton_procesar_archivo_kml.configure(state='normal')
                if self.label_map_container: # Asegurarse de destruir el contenedor del mapa
                    self.label_map_container.destroy()
                    self.label_map_container = None
                self.mapa_tkinter = None # Limpiar referencia al mapa

            elif respuesta == "correcta":
                checkboxes_convert(self.parent)
                self.parent.checkbox_type.enable_checkboxes()
                
                # Destruir botones de confirmación
                if hasattr(self.parent, 'boton_looks_good'):
                    self.parent.boton_looks_good.destroy()
                    del self.parent.boton_looks_good
                if hasattr(self.parent, 'boton_no_good'):
                    self.parent.boton_no_good.destroy()
                    del self.parent.boton_no_good
                if hasattr(self.parent, 'label_mappreview'):
                    self.parent.label_mappreview.destroy()
                    del self.parent.label_mappreview

                generate_files(self.parent, doc, ruta_archivo_kml, coords, utm_point_list, layer_names)

        # Creación de widgets (pueden ser encapsulados en un método separado si la UI es más compleja)
        self.parent.label_mappreview = ctk.CTkLabel(self.parent, text='Visión Preliminar Área Geográfica a Procesar',
                                                     fg_color=COLOR_BACKGROUND_LABEL, text_color=COLOR_TEXT_LABEL,
                                                     width=290, height=25, corner_radius=6)
        self.parent.label_mappreview.place(x=580, y=40)

        self.parent.boton_looks_good = ctk.CTkButton(self.parent, text="Looks good",
                                                      command=lambda: respuesta_confirmacion("correcta"),
                                                      fg_color=COLOR_BACKGROUND_LABEL, text_color=COLOR_TEXT_LABEL,
                                                      width=100, height=25, corner_radius=6)
        self.parent.boton_looks_good.place(x=900, y=40)

        self.parent.boton_no_good = ctk.CTkButton(self.parent, text="Select another file",
                                                    command=lambda: respuesta_confirmacion("incorrecta"),
                                                    fg_color=COLOR_BACKGROUND_LABEL, text_color=COLOR_TEXT_LABEL,
                                                    width=100, height=25, corner_radius=6)
        self.parent.boton_no_good.place(x=1060, y=40)

    def update_preview(self, lat_centro, lon_centro, zoom_start, root_element_xml, altitud_value):
        # Destruir el contenedor anterior si existe
        if self.label_map_container:
            # No es necesario destruir los hijos uno por uno si destruyes el padre
            self.label_map_container.destroy()
            self.label_map_container = None # Limpiar la referencia

        self.label_map_container = ctk.CTkLabel(self.parent, text='', width=700, height=500)
        self.label_map_container.place(x=580, y=80)

        self.mapa_tkinter = TkinterMapView(self.label_map_container)
        self.mapa_tkinter.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.mapa_tkinter.set_position(lat_centro, lon_centro)
        self.mapa_tkinter.set_zoom(zoom_start)

        # Obtener los placemarks una sola vez
        try:
            placemarks = encontrar_placemark(root_element_xml)
        except Exception as e:
            messagebox.showerror("Error al encontrar Placemarks", f"No se pudieron encontrar placemarks en el KML: {e}")
            return

        for placemark in placemarks:
            try:
                # Los últimos tres argumentos de procesar_placemark parecen ser listas vacías para acumular datos
                # Asegúrate de que la función los maneje correctamente. Si son para acumular, deberías pasarlos
                # o inicializarlos de alguna manera que tenga sentido para el bucle.
                # Aquí asumo que procesar_placemark devuelve los valores que necesitas directamente.
                _, _, coords_dec, _, layer_name = procesar_placemark(placemark, altitud_value, [], [], [])
                
                if len(coords_dec) == 1:
                    # Usar la imagen precargada
                    self.mapa_tkinter.set_marker(coords_dec[0][0], coords_dec[0][1], text=layer_name,
                                                    font=FONT_MARKER, text_color=COLOR_TEXT_LABEL,
                                                    icon=self.plane_image if self.plane_image else None)
                elif len(coords_dec) > 1:
                    puntos = [(point[0], point[1]) for point in coords_dec]
                    self.mapa_tkinter.set_path(puntos, color="red", width=1)
            except Exception as e:
                print(f"Advertencia: No se pudo procesar el placemark '{placemark.tag}' - {e}")
                continue # Continuar con el siguiente placemark