
import customtkinter as ctk
from customtkinter import filedialog

def select_cor(self):
    self.mapa_tkinter = None
    self.selectcor_boton.configure(state='normal')
    self.grab_set()
    ruta_archivo_excel = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivo XLSX", "*.xlsx")])
    self.selectcor_entry.delete(0, ctk.END)
    self.selectcor_entry.insert(ctk.END, ruta_archivo_excel)
    convert_cor(self)
    return ruta_archivo_excel

def convert_cor(self):
    class Rbutton:
        def __init__(self, master, values):
            self.rbuttons = []
            self.labels = []
            self.var = ctk.IntVar()
            

            for i, value in enumerate(values):
                label = ctk.CTkLabel(master, text=value, fg_color='red')
                Rbutton = ctk.CTkRadioButton(master, variable=self.var, value=i, text='')
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
    self.rbutton_type = Rbutton(self, values)
    
    self.zona_var = ctk.IntVar(value=1)
    
    self.slider = ctk.CTkSlider(self, from_=1, to=60, variable=self.zona_var, number_of_steps=59)
    self.slider.place(x=150, y=165)
    
    self.label_valor = ctk.CTkLabel(self, text = 'Zona Geografica')
    self.label_valor.place(x=190, y=140)
    
    self.label_valor = ctk.CTkLabel(self, textvariable = self.zona_var)
    self.label_valor.place(x=243, y=178)
    

    self.hemi_var = ctk.StringVar
    
    self.label_hemi = ctk.CTkLabel(self, text='Hemisferio')
    self.label_hemi.place(x=430, y=140)   
                                        
    self.checkbox_hemi = ctk.CTkComboBox(self, values=["-","Norte", "Sur"], variable=self.hemi_var)
    self.checkbox_hemi.place(x=380, y= 165)