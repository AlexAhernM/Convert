import customtkinter

def convert_cor(self):
    class Rbutton:
        def __init__(self, master, values):
            self.rbuttons = []
            self.labels = []
            self.var = customtkinter.IntVar()
            

            for i, value in enumerate(values):
                label = customtkinter.CTkLabel(master, text=value, fg_color='red')
                label.place(x=(i+1)*80+40, y=80)  # ajusta la posición y para que quede más arriba
                
                Rbutton = customtkinter.CTkRadioButton(master, variable=self.var, value=i)
                Rbutton.place(x=(i+1)*100+10, y=110)  # ajusta la posición x para que quede centrado debajo del label
            self.var.set(-1)  # Deseleccionar los radiobuttons


        def enable_rbuttons(self):
            for rbutton in self.rbuttons:
                rbutton.configure(state="normal")
                
        def destroy_rbuttons(self):
             for rbutton in self.rbuttons:
                rbutton.destroy()
             for label in self.labels:
                label.destroy()
            
    # FRAME: ROW 0 - CHECKBOXES AND RESULT FORMAT
    
    values = ['Grados decimales', 'Grados, minutos, segundos', 'Grados, minutos decimales', 'UTM']
    self.rbutton_type = Rbutton(self.ventana_tercera, values)