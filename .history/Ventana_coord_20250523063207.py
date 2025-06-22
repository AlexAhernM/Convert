

import customtkinter as ctk
from PIL import Image

def abrir_ventana_cor(self):

    self = ctk.CTkToplevel(self)
    self.title("Convert Coordinates Files (Excel)")
    self.geometry('1200x600')
    self.configure(fg_color='white smoke', height= 25)
    self.grab_set()
    
    selectdata_boton = ctk.CTkButton(self, text='Select your Excel File', width=200, fg_color='green', font=('Arial',16), text_color='white', 
                                        command= select_file())
    selectdata_boton.place(x=40, y=40)
                
    selectdata_entry = ctk.CTkEntry(self, width=270)
    selectdata_entry.place(x=270, y=40 )
    
    button_preview = ctk.CTkButton(self, text="Preview", width=510, fg_color='black', text_color='white', font=('Arial',16),
                                                command= lambda: preview(self))
    button_preview.configure(state= 'normal')
    button_preview.place(x=40, y =180)   
    
    
    
def select_file(s):
    # función para seleccionar archivo
    pass

def preview(root):
       
    imagen_4= Image.open("D:\\OneDrive\\tuto_vscode\\Conversion\\Atardecer_anf.png")
    imagen_4 = imagen_4.resize((400, 200)) 
    imagen_tk4 = ctk.CTkImage(light_image=imagen_4, dark_image=imagen_4, size=(400,200))
    
    try:                    
        label4 = ctk.CTkLabel(root, text='', image= imagen_tk4)
        label4.image = imagen_tk4  # mantener una referencia a la imagen
        label4.place(x=580, y = 40 )
        
            
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
    
        
