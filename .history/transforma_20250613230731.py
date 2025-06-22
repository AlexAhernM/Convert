
import xml.etree.ElementTree as ET
import utm
import re
import math
import ezdxf
import requests
     
#Diccionario para utilizar niveles de zoom en acuerdo a un rango de radios    
zoom_levels = {
    (0 , 50) :    19, 
    (50, 100) :   18,
    (101, 200) :  17,
    (201, 500) :  16,
    (501, 999) :  16,
    (1000, 1500): 15,
    (1501, 4500): 14,
    (4501, 12500): 13,
    (12501, 30000):12,
    (30001, 45000):11,
    (45001, 60000):10,
    (60001, 100000):9,
    (100001,170000):8,
    (170001,400000):7,
    (400001,700000):6,
    (700001,1500000):5,
    (1500001,2500000):4,
    (2500001, float('inf')):3    
}

#Funcion que determina el zoom para TkinterMapView
def get_zoom_level(radio):
            for (min_radio, max_radio), zoom in zoom_levels.items():
                if min_radio <= radio <= max_radio:
                    return zoom
# Funcion que analiza la estructura del archivo kml, altitud value no se utiliza, se incorpora para usos futuros a traves de una API
def parseo(ruta_archivo_klm, checkbox_frame_2_get):
    altitude_value = checkbox_frame_2_get
    
    try:
        tree = ET.parse(ruta_archivo_klm)
        root_element_xml = tree.getroot()
     
    except ET.ParseError as e:
        print(f"Error al parsear el archivo KML: {e}")
        return
      
    return root_element_xml, altitude_value
    
def encontrar_placemark(root_element_xml):
    placemark  = root_element_xml.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
    
    return placemark

def procesar_placemark(placemark, obtener_elevacion_valor, coords, layers, coords_dec):
    name_element = placemark.find('{http://www.opengis.net/kml/2.2}name')
    layer_name = name_element.text if name_element is not None else 'Sin_nombre'
    if len(layer_name) > 255:
        layer_name = layer_name[:255]
    layer_name = re.sub('[^a-zA-Z0-9_]', '_', layer_name)

    ls = placemark.find('{http://www.opengis.net/kml/2.2}LineString')
    py = placemark.find('{http://www.opengis.net/kml/2.2}Polygon')
    mg = placemark.find('{http://www.opengis.net/kml/2.2}MultiGeometry')
    pt = placemark.find('{http://www.opengis.net/kml/2.2}Point')

    if ls is not None:
        coord = ls.find('{http://www.opengis.net/kml/2.2}coordinates')
    elif py is not None:
        outer_boundary = py.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
        if outer_boundary is not None:
            linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
            if linear_ring is not None:
                coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates')
    elif pt is not None:
        coord = pt.find('{http://www.opengis.net/kml/2.2}coordinates')

    if mg is not None:
        coords coords, coords_dec, layers = procesar_multigeometrias(mg, layer_name, obtener_elevacion_valor, coords, layers, coords_dec)
    elif coord is not None:
        coords coords, coords_dec, layers = obtener_coordenadas_utm(coord, layer_name, obtener_elevacion_valor, coords, layers, coords_dec)

    return coords coords, coords_dec, layers, layer_name
    
def obtener_coordenadas_capas(root_element_xml, altitude_value):
    doc = ezdxf.new('R2013')
    coords = []
    layers = []
    coords_dec = []
    utm_points_list = []
    layer_names = []

    for placemark in encontrar_placemark(root_element_xml):
        coords coords, coords_dec, layers, layer_name = procesar_placemark(placemark, altitude_value, coords, layers, coords_dec)
        utm_points_list.append(utm_points)
        layer_names.append(layer_name)
    
    #print (coords)
    #print (coords_dec)    
    resultados = obtener_maximos_minimos(coords, coords_dec)
    lat_min = resultados['lat_min']
    lat_max = resultados['lat_max']
    lon_min = resultados['lon_min']
    lon_max = resultados['lon_max']
    lat_centro = resultados['lat_centro']
    lon_centro = resultados['lon_centro']
    radio = max(abs(lat_max - lat_min), abs(lon_max - lon_min))

    for coords layer_name in zip(utm_points_list, layer_names):
        agregar_polilinea(coords layer_name, doc)
           
    return doc, coords, coords_dec, layers, lat_centro, lon_centro, radio

def procesar_multigeometrias(geoms, layer_name, obtener_elevacion_valor, coords, layers, coords_dec):
    utm_points_total = []
    coords_total = coords
    coords_dec_total = coords_dec
    layers_total = layers
    
    for geom in geoms:
        if geom.tag == '{http://www.opengis.net/kml/2.2}Polygon':
            outer_boundary = geom.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            if outer_boundary is not None:
                linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing')
                if linear_ring is not None:
                    coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates')
                    coords coords, coords_dec, layers = obtener_coordenadas_utm(coord, layer_name, obtener_elevacion_valor, coords, layers, coords_dec)
                    utm_points_total.extend(utm_points)
                    coords_total.extend(coords)
                    coords_dec_total.extend(coords_dec)
        elif geom.tag in ['{http://www.opengis.net/kml/2.2}LineString', '{http://www.opengis.net/kml/2.2}Point']:
            coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
            coords coords, coords_dec, layers = obtener_coordenadas_utm(coord, layer_name, obtener_elevacion_valor, coords, layers, coords_dec)
            utm_points_total.extend(utm_points)
            coords_total.extend(coords)
            coords_dec_total.extend(coords_dec)
    
    return utm_points_total, coords_total, coords_dec_total, layers_total

def obtener_maximos_minimos(coords, coords_dec):
        
    # Calcula el promedio de las coordenadas x e y
    lats, lons = zip(*coords_dec)
    lat_centro = sum(lats) / len(lats)
    lon_centro = sum(lons) / len(lons)
      
    # Obtener los máximos y mínimos de x e y
    lat_min = min(coords, key=lambda x: x[0])[0]
    lat_max = max(coords, key=lambda x: x[0])[0]
    lon_min = min(coords, key=lambda x: x[1])[1]
    lon_max = max(coords, key=lambda x: x[1])[1]
    
    return {
        'lat_min': lat_min,
        'lat_max': lat_max,
        'lon_min': lon_min,
        'lon_max': lon_max,
        'lat_centro': lat_centro,
        'lon_centro': lon_centro
    }
     
def obtener_coordenadas_utm(coord, layer_name,  altitud_value ,coords, layers, coords_dec):
                       
    utm_points = []
    elevaciones_api = []  
    
    if coord is not None:
        points = [c.split(',') for c in coord.text.split()]
        
        for point in points:
            lat, lon = float(point[1]), float(point[0])
            utm_point = utm.from_latlon(lat, lon)
            layers.append(layer_name)
            coords_dec.append((lat, lon))
            if altitud_value:
                print("Obteniendo altitud de la API de Google Maps...")
                altitud_api = obtener_altitud_api(lat, lon)
                elevaciones_api.append((lat, lon, altitud_api))
                utm_points.append((utm_point[0], utm_point[1], altitud_api))
                coords.append((utm_point[0], utm_point[1], altitud_api))
            else:
                utm_points.append((utm_point[0], utm_point[1], 0))
                coords.append((utm_point[0], utm_point[1], 0))
   
    return coords coords, coords_dec, layers

def obtener_altitud_api(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key=AIzaSyACWL7hMm-4fAymx2DY5IkJ5iDlVUy4zEA"
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        print("Respuesta de la API de Google Maps recibida correctamente")
        datos = respuesta.json()
        return round(datos["results"][0]["elevation"], 2)
    else:
        return 0

def agregar_polilinea(coords layer_name, doc):
    """
    Agrega una polilínea o un círculo a un documento DXF.

    Parámetros:
    utm_points (list): Lista de puntos UTM.
    layer_name (str): Nombre de la capa.
    doc (ezdxf.document): Documento DXF.
    radio (float): Radio del círculo.
    """
    # Verificar si el nombre ya existe en el documento DXF
    if layer_name in doc.layers:
        # Si ya existe, agregar un sufijo para hacerlo único
        i = 1
        while f"{layer_name} ({i})" in doc.layers:
            i += 1
        layer_name = f"{layer_name} ({i})"    
    layer = doc.layers.new(layer_name)
    layer.dxf.color = 154  # azul (utiliza el índice de color de AutoCAD)
    msp = doc.modelspace()
    
    if len(utm_points) == 1:  # Si es un punto
        # Generar un círculo de radio un metro alrededor del punto
        radius = 20  # Radio del círculo en metros
        num_points = 36  # Número de puntos que conforman el círculo
        circle_points = []
        for i in range(num_points):
            angle = i * 360 / num_points
            x = utm_points[0][0] + radius * math.cos(math.radians(angle))
            y = utm_points[0][1] + radius * math.sin(math.radians(angle))
            circle_points.append((x, y))
            
        # Agregar el círculo al documento DXF
        msp.add_polyline2d(circle_points, dxfattribs={'layer': layer_name, 'color': 7})
        
        # Crear un hatch (relleno) para rellenar el círculo
        hatch = msp.add_hatch(color=1)  # Color negro
        hatch.paths.add_polyline_path(circle_points + [circle_points[0]])  # Agregar el primer punto al final para cerrar el hatch
        
        # Agregar el nombre de la capa encima del círculo
        msp.add_mtext(layer_name, dxfattribs={'layer': layer_name, 'color': 7, 'insert': (utm_points[0][0], utm_points[0][1] + radius + 5), 'char_height': 30})
        
    else:
        # Agregar la polilínea al documento DXF
        msp.add_polyline2d(coords dxfattribs={'layer': layer_name, 'color': 7})
                  
    
