
import os
import fiona
import pandas as pd
import utm
import matplotlib.pyplot as plt
import ezdxf






COLUMNAS = ['X °','Y º', 'X UTM', 'Y UTM', 'Altitud', 'Capa']

def generate_files_intermediate(self, doc, ruta_archivo_kml, coords, layers, coords_dec, utm_point_list, layer_names):
    return crear_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec, utm_point_list, layer_names)


def crear_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec, utm_points_list, layer_names):
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
            nombre_archivo_salida_dxf = ruta_archivo_kml.split('/')[-1].split('.')[0] + '.dxf'
            ruta_archivo_salida_dxf = os.path.join(downloads_folder, nombre_archivo_salida_dxf)

            # Renombrar el archivo si ya existe
            if os.path.exists(ruta_archivo_salida_dxf):
                base, extension = os.path.splitext(ruta_archivo_salida_dxf)
                i = 1
                while os.path.exists(ruta_archivo_salida_dxf):
                    ruta_archivo_salida_dxf = f"{base} ({i}){extension}"
                    i += 1
            doc.saveas(ruta_archivo_salida_dxf)
            msg_dxf= f"DXF File save in {ruta_archivo_salida_dxf}"
            temp_file = False
            
        else:
            # Guarda el archivo DXF temporal
            ruta_archivo_salida_dxf = os.path.join(downloads_folder, "temp.dxf")
            doc.saveas(ruta_archivo_salida_dxf)
            temp_file = True

        if shp_selected:
            nombre_archivo_salida_shp = ruta_archivo_kml.split('/')[-1].split('.')[0] + '.shp'
            ruta_archivo_salida_shp = os.path.join(downloads_folder, nombre_archivo_salida_shp)
                    
            # Renombrar el archivo SHP si ya existe
            if os.path.exists(ruta_archivo_salida_shp):
                base, extension = os.path.splitext(ruta_archivo_salida_shp)
                i = 1
                while os.path.exists(ruta_archivo_salida_shp):
                    ruta_archivo_salida_shp = f"{base} ({i}){extension}"
                    i += 1
                    
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
       

            # Abrir el archivo DXF
            doc = ezdxf.readfile(ruta_archivo_salida_dxf)
            msp = doc.modelspace()

            fig, ax = plt.subplots()
            for entity in msp:
                if entity.dxftype() == 'LINE':
                    ax.plot([entity.dxf.start[0], entity.dxf.end[0]], [entity.dxf.start[1], entity.dxf.end[1]], 'k-')
                elif entity.dxftype() == 'CIRCLE':
                    circle = plt.Circle((entity.dxf.center[0], entity.dxf.center[1]), entity.dxf.radius, edgecolor='black', facecolor='none')
                    ax.add_artist(circle)

            ax.set_aspect('equal')
            ax.axis('off')

            # Guarda el archivo PDF
            nombre_archivo_salida_pdf = ruta_archivo_kml.split('/')[-1].split('.')[0] + '.pdf'
            ruta_archivo_salida_pdf = os.path.join(downloads_folder, nombre_archivo_salida_pdf)

            # Renombrar el archivo si ya existe
            if os.path.exists(ruta_archivo_salida_pdf):
                base, extension = os.path.splitext(ruta_archivo_salida_pdf)
                i = 1
                while os.path.exists(ruta_archivo_salida_pdf):
                    ruta_archivo_salida_pdf = f"{base} ({i}){extension}"
                    i += 1

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

        df = pd.DataFrame(data, columns=COLUMNAS)
        
        
        
        # Crear DataFrame
        df = pd.DataFrame(data, columns=COLUMNAS)

        # Comprobación para asegurarte de que el DataFrame no esté vacío
        if df.empty:
            print("No hay datos para exportar.")
            return

        # Crear la ruta del archivo de salida
        nombre_archivo_salida = f"{ruta_archivo_kml.split('/')[-1].split('.')[0]}.xlsx"
        ruta_archivo_salida = os.path.join(downloads_folder, nombre_archivo_salida)

        # Renombrar el archivo si ya existe
        if os.path.exists(ruta_archivo_salida):
            base, extension = os.path.splitext(ruta_archivo_salida)
            i = 1
            while os.path.exists(ruta_archivo_salida):
                ruta_archivo_salida = f"{base} ({i}){extension}"
                i += 1

        # Exportar DataFrame a Excel
        df.to_excel(ruta_archivo_salida, index=False)
        msg_xlx =  f"Excel File save in  {ruta_archivo_salida}"
        print(' archivo generado correctamente  ', msg_xlx)
    
    self.checkbox_type.checkboxes[0].configure(state='disabled')
    self.checkbox_type.checkboxes[0].deselect()
    
    self.checkbox_type.checkboxes[1].configure(state='disabled')
    self.checkbox_type.checkboxes[1].deselect()
    
    self.checkbox_type.checkboxes[2].configure(state='disabled')
    self.checkbox_type.checkboxes[2].deselect()    
    
    #self.boton_looks_good.configure(state='disabled')
    #self.boton_no_good.configure(state='disabled')
    self.boton_generate_files.configure(state='disabled')
    return msg_dxf, msg_shp, msg_xlx, msg_pdf