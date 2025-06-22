import customtkinter

def convert_cor(self):
    class Rbutton:
        def __init__(self, master, values, enabled=True):
            self.rbuttons = []
            self.var = customtkinter.IntVar()

            for i, value in enumerate(values):
                inputdata = customtkinter.CTkRadioButton(master, text=value, variable=self.var, value=i)
                inputdata.place(x=i*150+50, y=100)
                #inputdata.configure(border_width=1, border_color='black')
                if not enabled:
                    inputdata.configure(state="disabled")
                self.rbuttons.append(inputdata)


        def enable_rbuttons(self):
            for rbutton in self.rbuttons:
                rbutton.configure(state="normal")
                
        def destroy_rbuttons(self):
             for rbutton in self.rbuttons:
                rbutton.destroy()
            
    # FRAME: ROW 0 - CHECKBOXES AND RESULT FORMAT
    
    self.rbutton_type = Rbutton(self.ventana_tercera, values=['Grados Decimales', 'Grados, minutos, segundos', 'Grados, minutos decimales', 'UTM'], enabled=False)
    self.boton_generate_cor = customtkinter.CTkButton(self.ventana_segunda, text='Generate Files', width=510, fg_color='green', text_color='white')
    self.boton_generate_cor.place(x= 40, y=220)
    self.boton_generate_cor.configure(state= 'disabled')