import customtkinter

def convert_cor(self):
    class Rbutton:
        def __init__(self, master, values, enabled=True):
            self.rbuttons = []
            self.labels = []
            self.var = customtkinter.IntVar()

            for i, value in enumerate(values):
                frame = customtkinter.CTkFrame(master)
                frame.place(x=(i+1)*150+50, y=100)

                label = customtkinter.CTkLabel(frame, text=value)
                label.pack()

                inputdata = customtkinter.CTkRadioButton(frame, variable=self.var, value=i)
                inputdata.pack()

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