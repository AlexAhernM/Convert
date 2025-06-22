import customtkinter

def convert_cor(self):
    class Rbutton:
        def __init__(self, master, values, enabled=True):
            self.rbuttons = []
            self.labels = []
            self.var = customtkinter.IntVar()

            for i, value in enumerate(values):
                label = customtkinter.CTkLabel(self.ventana_tercera,  text=value)
                label.place(x=(i+1)*150+50, y=100)
                
                inputdata = customtkinter.CTkRadioButton(self.ventana_tercera,  variable=self.var, value=i)
                inputdata.place(x=(i+1)*150+50, y=120)

                if not enabled:
                    inputdata.configure(state="disabled")
                self.rbuttons.append(inputdata)
                self.labels.append(label)
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