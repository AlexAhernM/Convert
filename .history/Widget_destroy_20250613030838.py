from Imagen_windows2 import ventana_segunda_imagen

def widgets_destroy(self):
    self.selectdata_boton.configure(state='normal')
    self.buttton_procesar_archivo_kml.configure(state='disabled')
    
    self.selectdata_entry.configure(state='normal')
    self.selectdata_entry.delete(0, "end") # Limpiar contenido
    self.selectdata_entry.configure(state='disabled')
    
    self.boton_looks_good.destroy()
    self.boton_no_good.destroy()
    self.label_mappreview.destroy()
    if hasattr(self, 'boton_generate_files') and self.boton_generate_files.winfo_exists():
        self.boton_generate_files.destroy()
    if hasattr(self, 'checkbox_type') :  
        self.checkbox_type.destroy_checkboxes()
    if hasattr(self, 'boton_limpiar') and self.boton_limpiar.winfo_exists():
        self.boton_limpiar.destroy()
    if self.label3.winfo_children():
        for widget in self.label3.winfo_children():
            widget.destroy()
    if  self.show_files_frame.winfo_children():       
        for widget in self.show_files_frame.winfo_children():
            widget.destroy()
    
    ventana_segunda_imagen(self)