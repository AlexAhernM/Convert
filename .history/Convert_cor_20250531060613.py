import customtkinter

def convert_cor(self):
    class Rbutton:
        def __init__(self, master, values):
            self.rbuttons = []
            self.labels = []
            self.var = customtkinter.IntVar()
            

            for i, value in enumerate(values):
                label = customtkinter.CTkLabel(master, text=value, fg_color='red')
                Rbutton = customtkinter.CTkRadioButton(master, variable=self.var, value=i, text='')
                y=80
                x=30
                if i==0 :
                    label.place(x=x, y=y)  # ajusta la posición y para que quede más arriba
                    Rbutton.place(x=x+40, y=y+25)
                if i==1:
                    label.place(x=x+150, y=y)  # ajusta la posición y para que quede más arr
                    Rbutton.place(x= x+210, y=y+25)
                if i==2:
                    label.place(x=x+350, y=y)  # ajusta la posición y para que quede más arr
                    Rbutton.place(x=x+400, y=y+25)
                if i==3:
                    label.place(x=65, y=y+60)  # ajusta la posición y para que quede más arr
                    Rbutton.place(x=x+40, y=y+85)
                
                  # ajusta la posición x para que quede centrado debajo del label
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
    
    
         
    self.zona_var = customtkinter.StringVar(value="1")
    values = [str(i) for i in range(1, 61)]
    self.checkbox_zona = customtkinter.CTkComboBox(self.ventana_tercera, values=values, variable=self.zona_var)
    self.checkbox_zona.place(x=180, y=165)

    self.hemi_var = customtkinter.StringVar(value="Norte")
    self.label_hemi = customtkinter.CTkLabel(self.ventana_tercera, text='Hemisferio')
    self.label_hemi.place(x=430, y=140)                                       
    self.checkbox_hemi = customtkinter.CTkComboBox(self.ventana_tercera, values=["Norte", "Sur"], variable=self.hemi_var)
    self.checkbox_hemi.place(x=380, y= 165)