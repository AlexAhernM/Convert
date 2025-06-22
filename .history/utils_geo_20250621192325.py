import xml.etree.ElementTree as ET
import utm
import re
import math
import requests


def encontrar_placemark(root_element_xml):
    return root_element_xml.findall('.//{http://www.opengis.net/kml/2.2}Placemark')


def procesar_placemark(placemark, obtener_elevacion_valor, coords, layers, coords_dec):
    name_element = placemark.find('{http://www.opengis.net/kml/2.2}name')
    layer_name = name_element.text if name_element is not None else 'Sin_nombre'
    layer_name = re.sub('[^a-zA-Z0-9_]', '_', layer_name[:255])

    ls = placemark.find('{http://www.opengis.net/kml/2.2}LineString')
    py = placemark.find('{http://www.opengis.net/kml/2.2}Polygon')
    mg = placemark.find('{http://www.opengis.net/kml/2.2}MultiGeometry')
    pt = placemark.find('{http://www.opengis.net/kml/2.2}Point')

    if ls is not None:
        coord = ls.find('{http://www.opengis.net/kml/2.2}coordinates')
    elif py is not None:
        outer_boundary = py.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
        linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing') if outer_boundary is not None else None
        coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates') if linear_ring is not None else None
    elif pt is not None:
        coord = pt.find('{http://www.opengis.net/kml/2.2}coordinates')
    else:
        coord = None

    if mg is not None:
        utm_points, coords, coords_dec, layers = procesar_multigeometrias(mg, layer_name, obtener_elevacion_valor, coords, layers, coords_dec)
    elif coord is not None:
        utm_points, coords, coords_dec, layers = procesar_coordenadas_utm(coord, layer_name, obtener_elevacion_valor, coords, layers, coords_dec)
    else:
        utm_points = []

    return utm_points, coords, coords_dec, layers, layer_name


def procesar_multigeometrias(geoms, layer_name, obtener_elevacion_valor, coords, layers, coords_dec):
    utm_points_total = []
    for geom in geoms:
        if geom.tag == '{http://www.opengis.net/kml/2.2}Polygon':
            outer_boundary = geom.find('{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            linear_ring = outer_boundary.find('{http://www.opengis.net/kml/2.2}LinearRing') if outer_boundary is not None else None
            coord = linear_ring.find('{http://www.opengis.net/kml/2.2}coordinates') if linear_ring is not None else None
        elif geom.tag in ['{http://www.opengis.net/kml/2.2}LineString', '{http://www.opengis.net/kml/2.2}Point']:
            coord = geom.find('{http://www.opengis.net/kml/2.2}coordinates')
        else:
            coord = None

        if coord is not None:
            utm_points, coords, coords_dec, layers = procesar_coordenadas_utm(coord, layer_name, obtener_elevacion_valor, coords, layers, coords_dec)
            utm_points_total.extend(utm_points)

    return utm_points_total, coords, coords_dec, layers


def procesar_coordenadas_utm(coord, layer_name, altitud_value, coords, layers, coords_dec):
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
                altitud_api = obtener_altitud_api(lat, lon)
                elevaciones_api.append((lat, lon, altitud_api))
                utm_points.append((utm_point[0], utm_point[1], altitud_api))
                coords.append((utm_point[0], utm_point[1], altitud_api))
            else:
                utm_points.append((utm_point[0], utm_point[1], 0))
                coords.append((utm_point[0], utm_point[1], 0))

    return utm_points, coords, coords_dec, layers


def obtener_altitud_api(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key=TU_API_KEY"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return round(datos["results"][0]["elevation"], 2)
    return 0


def obtener_maximos_minimos(coords_dec):
    lats, lons = zip(*coords_dec)
    lat_centro = sum(lats) / len(lats)
    lon_centro = sum(lons) / len(lons)

    lat_min = min(lats)
    lat_max = max(lats)
    lon_min = min(lons)
    lon_max = max(lons)

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    distancia_ns = haversine(lat_min, lon_centro, lat_max, lon_centro)
    distancia_ew = haversine(lat_centro, lon_min, lat_centro, lon_max)
    radio = max(distancia_ns, distancia_ew) / 2

    return {
        'lat_min': lat_min,
        'lat_max': lat_max,
        'lon_min': lon_min,
        'lon_max': lon_max,
        'lat_centro': lat_centro,
        'lon_centro': lon_centro,
        'radio': radio
    }


def agregar_polilinea(coords, layer_name, doc):
    # Verificar si el nombre ya existe en el documento DXF
    if layer_name in doc.layers:
        i = 1
        while f"{layer_name} ({i})" in doc.layers:
            i += 1
        layer_name = f"{layer_name} ({i})"

    layer = doc.layers.new(layer_name)
    layer.dxf.color = 154  # azul (índice de color AutoCAD)
    msp = doc.modelspace()

    if len(coords) == 1:
        radius = 20
        num_points = 36
        circle_points = [
            (
                coords[0][0] + radius * math.cos(math.radians(i * 360 / num_points)),
                coords[0][1] + radius * math.sin(math.radians(i * 360 / num_points))
            )
            for i in range(num_points)
        ]
        msp.add_polyline2d(circle_points, dxfattribs={'layer': layer_name, 'color': 7})
        polyline = msp.add_polyline2d(circle_points, dxfattribs={'layer': layer_name, 'color': 7})
        polyline.set_xdata('ACAD', [(1000, 'CIRCULO')])
        hatch = msp.add_hatch(color=1)
        hatch.paths.add_polyline_path(circle_points + [circle_points[0]])
        msp.add_mtext(layer_name, dxfattribs={
            'layer': layer_name, 'color': 7,
            'insert': (coords[0][0], coords[0][1] + radius + 5),
            'char_height': 30
        })
    else:
        msp.add_polyline2d(coords, dxfattribs={'layer': layer_name, 'color': 7})
