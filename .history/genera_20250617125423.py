

from build_files import crear_files
from Show_messages import show_messages



def generate_files(self, doc, ruta_archivo_kml, coords, layers, coords_dec, utm_point_list, layer_names):
    def on_click():
        messages = generate_files_intermediate(self, doc, ruta_archivo_kml, coords, layers, coords_dec, utm_point_list, layer_names)
        show_messages(self, messages)    
    self.boton_generate_files.configure(state= 'normal', command=on_click)


def generate_files_intermediate(self, doc, ruta_archivo_kml, coords, layers, coords_dec, utm_point_list, layer_names):
    return crear_files(self, doc, ruta_archivo_kml, coords, utm_point_list, layer_names)


