import customtkinter

def convert_files(self):
    class Checkbox:
        def __init__(self, master, values, enabled=True):
            self.values = values
            self.checkboxes = []

            for i, value in enumerate(self.values):
                inputdata = customtkinter.CTkCheckBox(master, text=value, corner_radius=90)
                inputdata.place(x=i*120+120, y=180)  # ajusta la posición según sea necesario
                inputdata.configure(border_width=1, border_color='black')
                if not enabled:
                    inputdata.configure(state="disabled")
                self.checkboxes.append(inputdata)

        def get(self):
            checked_checkboxes = []
            for inputdata in self.checkboxes:
                if inputdata.get() == 1:
                    checked_checkboxes.append(inputdata.get("text"))
            return checked_checkboxes

        def enable_checkboxes(self):
            for checkbox in self.checkboxes:
                checkbox.configure(state="normal")
                
        def destroy_checkboxes(self):
             for checkbox in self.checkboxes:
                checkbox.destroy()
            
    # FRAME: ROW 0 - CHECKBOXES AND RESULT FORMAT
    
    self.checkbox_type = Checkbox(self.ventana_segunda, values=['DXF (CAD)', 'Shapefile', 'xlxs (Excel)'], enabled=False)
    self.boton_generate_files = customtkinter.CTkButton(self.ventana_segunda, text='Generate Files', width=510, fg_color='green', text_color='white')
    self.boton_generate_files.place(x= 40, y=220)
    self.boton_generate_files.configure(state= 'disabled')
    

        
        
  
    return