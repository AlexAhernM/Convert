from Imagen_windows2 import ventana_segunda_imagen

def widgets_destroy(self):
    self.selectdata_boton.configure(state='normal')
    self.button_preview.configure(state='disabled')
    self.selectdata_entry.delete(0, "end") # Limpiar contenido
    self.boton_looks_good.destroy()
    self.boton_no_good.destroy()
    self.label_mappreview.destroy()
    self.boton_generate_files.destroy()
    self.destroy_checkboxes()
    if self.label3.winfo_children():
        for widget in self.label3.winfo_children():
            widget.destroy()
    if  self.show_files_frame.winfo_children():       
        for widget in self.show_files_frame.winfo_children():
            widget.destroy()
    
    ventana_segunda_imagen(self)