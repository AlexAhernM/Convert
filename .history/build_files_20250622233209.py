
import os
import fiona
import pandas as pd
import utm
import matplotlib.pyplot as plt
from Crear_PDF import crear_pdf


COLUMNAS = ['X °','Y º', 'X UTM', 'Y UTM', 'Altitud', 'Capa']

def crear_files(self, doc, ruta_archivo_kml, coords, utm_points_list, layer_names):
    # Establece la carpeta Downloads del Sistema Operativo para alojar los archivos convertidos        
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    dxf_selected = False
    shp_selected = False
    xlsx_selected = False
    pdf_selected = False
    
    msg_dxf = ""
    msg_shp = ""
    msg_xlx = ""
    msg_pdf = ""
    
    for checkbox in self.checkbox_type.checkboxes:
        if checkbox.get():
            text = checkbox.cget('text')
            if "DXF" in text:
                dxf_selected = True
            elif "Shapefile" in text:
                shp_selected = True
            elif "xlxs" in text:
                xlsx_selected = True
            elif "PDF" in text:
                pdf_selected = True

    if dxf_selected or shp_selected or pdf_selected:
        # Calcular las coordenadas de extensión
        x_coords = [point[0] for point in coords]
        y_coords = [point[1] for point in coords]
        ext_min = (min(x_coords), min(y_coords), 0)
        ext_max = (max(x_coords), max(y_coords), 0)

        doc.header['$EXTMIN'] = ext_min
        doc.header['$EXTMAX'] = ext_max

        if dxf_selected:
            # Guarda el archivo DXF
            temp_file = False
            ruta_archivo_salida_dxf = generar_ruta_archivo(ruta_archivo_kml, '.dxf', downloads_folder, temp_file)
            doc.saveas(ruta_archivo_salida_dxf)
            msg_dxf = f"DXF File save in {ruta_archivo_salida_dxf}"      
            
        else:
            # Guarda el archivo DXF temporal
            ruta_archivo_salida_dxf = os.path.join(downloads_folder, "temp.dxf")
            doc.saveas(ruta_archivo_salida_dxf)
            temp_file = True

        if shp_selected:
            ruta_archivo_salida_shp = generar_ruta_archivo(ruta_archivo_kml, '.shp', downloads_folder)
                         
            # Abrir el archivo DXF
            with fiona.open(ruta_archivo_salida_dxf, 'r', driver='DXF') as src:
                # Crear un nuevo Shapefile para líneas
                with fiona.open(ruta_archivo_salida_shp, 'w', driver='ESRI Shapefile', crs=src.crs, schema={'geometry': 'LineString', 'properties': src.schema['properties']}) as dst_lineas:
                    # Agregar los datos del archivo DXF
                    for feature in src:
                        if feature.geometry.type == 'Polygon':
                            new_feature = {'geometry': {'type': 'LineString','coordinates': feature.geometry.coordinates[0]},
                                'properties': feature.properties}
                            dst_lineas.write(new_feature)
                        elif feature.geometry.type == 'LineString':
                            dst_lineas.write(feature)

                msg_shp = f"SHP File save in  {ruta_archivo_salida_shp}"
                
            if temp_file and not pdf_selected:
                os.remove(ruta_archivo_salida_dxf)
                
        if  pdf_selected:
            crear_pdf(ruta_archivo_salida_dxf)
            ruta_archivo_salida_pdf = generar_ruta_archivo(ruta_archivo_kml, '.pdf', downloads_folder)
            plt.savefig(ruta_archivo_salida_pdf, bbox_inches='tight')
            msg_pdf = f"PDF File save in {ruta_archivo_salida_pdf}"
            plt.close()

    if temp_file and not shp_selected:
        os.remove(ruta_archivo_salida_dxf)         

    if xlsx_selected:
        # Combinar las listas en una sola lista de tuplas
        data = []
        for utm_points, layer_name in zip(utm_points_list, layer_names):
            for point in utm_points:
                coord_dec = utm.to_latlon(point[0], point[1], 19, 'S')
                data.append([coord_dec[0], coord_dec[1], point[0], point[1], point[2], layer_name])

        # Crear DataFrame
        df = pd.DataFrame(data, columns=COLUMNAS)

        # Comprobación para asegurarte de que el DataFrame no esté vacío
        if df.empty:
            print("No hay datos para exportar.")
            return

        # Crear la ruta del archivo de salida
        ruta_archivo_salida = generar_ruta_archivo(ruta_archivo_kml, '.xlsx', downloads_folder)
        # Exportar DataFrame a Excel
        df.to_excel(ruta_archivo_salida, index=False)
        msg_xlx =  f"Excel File save in  {ruta_archivo_salida}"
        print(' archivo generado correctamente  ', msg_xlx)
   
    self.checkbox_type.disable_checkboxes()
    
    self.boton_generate_files.configure(state='disabled')
    return msg_dxf, msg_shp, msg_xlx, msg_pdf

def generar_ruta_archivo(ruta_archivo_kml, extension, downloads_folder, temp=False):
    nombre_archivo_salida = ruta_archivo_kml.split('/')[-1].split('.')[0] + extension
    ruta_archivo_salida = os.path.join(downloads_folder, nombre_archivo_salida)

    if not temp:
        # Renombrar el archivo si ya existe
        if os.path.exists(ruta_archivo_salida):
            base, ext = os.path.splitext(ruta_archivo_salida)
            i = 1
            while os.path.exists(ruta_archivo_salida):
                ruta_archivo_salida = f"{base} ({i}){ext}"
                i += 1

    return ruta_archivo_salida


    
    