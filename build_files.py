
import os
import fiona
import pandas as pd
import utm
import matplotlib.pyplot as plt
from Crear_PDF import crear_pdf

COLUMNAS = ['X °', 'Y º', 'X UTM', 'Y UTM', 'Altitud', 'Capa']

class FileCreator:
    """
    Clase responsable de generar archivos de salida (DXF, SHP, PDF, XLSX) a partir de datos geoespaciales.
    Se integra con una interfaz gráfica basada en customtkinter.
    """

    def __init__(self, checkbox_type, boton_generate_files):
        """
        Inicializa la clase con los elementos de la interfaz gráfica.

        :param checkbox_type: Objeto que contiene los checkboxes de tipo de archivo.
        :param boton_generate_files: Botón que se desactiva tras la generación de archivos.
        """
        self.checkbox_type = checkbox_type
        self.boton_generate_files = boton_generate_files
        self.downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    def _generar_ruta_archivo(self, ruta_archivo_kml, extension, temp=False):
        """
        Genera una ruta de archivo única en la carpeta de descargas.

        :param ruta_archivo_kml: Ruta del archivo KML original.
        :param extension: Extensión del archivo de salida.
        :param temp: Si es True, no renombra archivos existentes.
        :return: Ruta completa del archivo de salida.
        """
        nombre_archivo = os.path.splitext(os.path.basename(ruta_archivo_kml))[0] + extension
        ruta_salida = os.path.join(self.downloads_folder, nombre_archivo)

        if not temp:
            base, ext = os.path.splitext(ruta_salida)
            i = 1
            while os.path.exists(ruta_salida):
                ruta_salida = f"{base} ({i}){ext}"
                i += 1

        return ruta_salida

    def crear_archivos(self, doc, ruta_archivo_kml, coords, utm_points_list, layer_names):
        """
        Genera los archivos seleccionados por el usuario (DXF, SHP, PDF, XLSX).

        :param doc: Documento DXF generado.
        :param ruta_archivo_kml: Ruta del archivo KML original.
        :param coords: Lista de coordenadas geográficas.
        :param utm_points_list: Lista de listas de puntos UTM.
        :param layer_names: Lista de nombres de capas.
        :return: Tupla con mensajes de estado para cada tipo de archivo.
        """
        # Determinar qué archivos generar
        tipos = {cb.cget('text'): cb.get() for cb in self.checkbox_type.checkboxes}
        dxf_selected = tipos.get("DXF", False)
        shp_selected = tipos.get("Shapefile", False)
        xlsx_selected = tipos.get("xlxs", False)
        pdf_selected = tipos.get("PDF", False)

        msg_dxf = msg_shp = msg_xlx = msg_pdf = ""
        temp_file = False

        if dxf_selected or shp_selected or pdf_selected:
            # Calcular extensión del dibujo
            x_coords = [p[0] for p in coords]
            y_coords = [p[1] for p in coords]
            doc.header['$EXTMIN'] = (min(x_coords), min(y_coords), 0)
            doc.header['$EXTMAX'] = (max(x_coords), max(y_coords), 0)

            # Guardar DXF
            ruta_dxf = self._generar_ruta_archivo(ruta_archivo_kml, '.dxf', temp=not dxf_selected)
            doc.saveas(ruta_dxf)
            if dxf_selected:
                msg_dxf = f"DXF File saved in {ruta_dxf}"
            else:
                temp_file = True

            # Generar SHP
            if shp_selected:
                ruta_shp = self._generar_ruta_archivo(ruta_archivo_kml, '.shp')
                with fiona.open(ruta_dxf, 'r', driver='DXF') as src:
                    with fiona.open(ruta_shp, 'w', driver='ESRI Shapefile', crs=src.crs,
                                    schema={'geometry': 'LineString', 'properties': src.schema['properties']}) as dst:
                        for feature in src:
                            if feature.geometry.type == 'Polygon':
                                dst.write({
                                    'geometry': {'type': 'LineString', 'coordinates': feature.geometry.coordinates[0]},
                                    'properties': feature.properties
                                })
                            elif feature.geometry.type == 'LineString':
                                dst.write(feature)
                msg_shp = f"SHP File saved in {ruta_shp}"
                if temp_file and not pdf_selected:
                    os.remove(ruta_dxf)

            # Generar PDF
            if pdf_selected:
                crear_pdf(ruta_dxf)
                ruta_pdf = self._generar_ruta_archivo(ruta_archivo_kml, '.pdf')
                plt.savefig(ruta_pdf, bbox_inches='tight')
                msg_pdf = f"PDF File saved in {ruta_pdf}"
                plt.close()

        if temp_file and not shp_selected:
            os.remove(ruta_dxf)

        # Generar Excel
        if xlsx_selected:
            data = []
            for utm_points, layer in zip(utm_points_list, layer_names):
                for point in utm_points:
                    latlon = utm.to_latlon(point[0], point[1], 19, 'S')
                    data.append([latlon[0], latlon[1], point[0], point[1], point[2], layer])
            df = pd.DataFrame(data, columns=COLUMNAS)
            if not df.empty:
                ruta_xlsx = self._generar_ruta_archivo(ruta_archivo_kml, '.xlsx')
                df.to_excel(ruta_xlsx, index=False)
                msg_xlx = f"Excel File saved in {ruta_xlsx}"
                print('Archivo generado correctamente:', msg_xlx)

        # Desactivar controles de la interfaz
        self.checkbox_type.disable_checkboxes()
        self.boton_generate_files.configure(state='disabled')

        return msg_dxf, msg_shp, msg_xlx, msg_pdf



    
    