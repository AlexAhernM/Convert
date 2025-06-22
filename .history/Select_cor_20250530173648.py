from Convert_cor import convert_cor

import customtkinter as ctk
from customtkinter import filedialog

def select_cor(self):
    self.mapa_tkinter = None
    self.selectcor_boton.configure(state='normal')
    self.ventana_tercera.grab_set()
    ruta_archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivo XLSX", "*.xlsx")])
    self.selectcor_entry.delete(0, ctk.END)
    self.selectcor_entry.insert(ctk.END, ruta_archivo_excel)
    convert_cor(self)
    return ruta_archivo_excel