def widgets_destroy(self):
    for frame in [self.selectfile_frame, self.preview_frame,  self.checkbox_frame]:
        for widget in frame.winfo_children():
            widget.destroy()
    self.habilitar()

def convert_file(self):
    widgets_destroy(self)
    self.show_image_in_preview() 
    self.selectdata_boton = customtkinter.CTkButton(self.selectfile_frame, text='Select File', command=lambda: select_file(self))
    self.selectdata_boton.grid(row=0, column=0, padx=10, pady=(25,10), sticky = 'w')
        
    self.selectdata_entry = customtkinter.CTkEntry(self.selectfile_frame, width=320, height=25, corner_radius=6 )
    self.selectdata_entry.grid(row =0, column =1, padx=10, pady=(20,10 ), sticky ='w')
    
    if self.tipo_geo.get() == "KML":
        
        self.checkbox_altitude = CheckboxFrame(self.selectfile_frame, values=['Get Altitude'], enabled=False)
        self.checkbox_altitude.grid(row =1, column = 1, padx=10, pady=1)
        
        # FRAME: ROW 0 - CHECKBOXES AND RESULT FORMAT
        self.checkbox_type = CheckboxFrame(self ,values=['DXF (CAD)', 'Shapefile', 'xlxs (Excel)'], enabled=False, width=650, height=180)
        self.checkbox_type.grid(row=0, column=2, padx= 10, pady =5, sticky='w')
        self.checkbox_type.grid_propagate(False)
        
        self.boton_generate_files = customtkinter.CTkButton(self.checkbox_type, text='Generate Files')
        self.boton_generate_files.grid(row=4, column=0, padx=10, pady=(20,0), sticky='ew')
        self.boton_generate_files.configure(state= 'disabled')
        self.selectfile_frame.configure(fg_color="gray84")
        
        self.button_preview = customtkinter.CTkButton(self.selectfile_frame, text="Preview", 
                                                     command= lambda: button_preview(self), 
                                                     width=160, height=25)
        self.button_preview.configure(state= 'disabled')
        self.button_preview.grid(row=2, column=1, padx=20, pady=(35,0))
  
    elif self.tipo_geo.get() == "Coordenadas":
        if self.checkbox_altitude:
            self.checkbox_altitude.destroy()
        self.tipo_coord = customtkinter.StringVar()
        self.rbutton_grados_decimales = customtkinter.CTkRadioButton(self.selectfile_frame, text="Dec. Coord", variable=self.tipo_coord, value="dec")
        self.rbutton_grados_decimales.grid(row = 1, column =0, padx=10, pady=10, sticky ='e')
        
        self.rbutton_grados_utm = customtkinter.CTkRadioButton(self.selectfile_frame, text="UTM Coord", variable=self.tipo_coord, value="utm")
        self.rbutton_grados_utm.grid(row = 1, column =1, padx=10, pady=10, sticky ='w')
    return