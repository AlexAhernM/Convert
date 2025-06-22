from Imagen_windows2 import ventana_segunda_imagen

def widgets_destroy(self):
    self.selectdata_boton.configure(state='normal')
    self.button_preview.configure(state='disabled')
    self.boton_looks_good.destroy()
    self.boton_no_good.destroy()
    self.label_mappreview.destroy()
    for widget in self.label3.winfo_children():
        widget.destroy()
    ventana_segunda_imagen(self)