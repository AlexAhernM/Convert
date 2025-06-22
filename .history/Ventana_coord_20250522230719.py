

import customtkinter as ctk
from PIL import Image

def abrir_ventana_cor(master):

    root = ctk.CTkToplevel(master)
    root.title("Convert KML Files")
    root.geometry('1200x600')
    root.configure(fg_color='white', height= 25)
    root.grab_set()
    
    selectdata_boton = ctk.CTkButton(root, text='Select your KML File', width=200, fg_color='gray7', font=('Arial',16), text_color='white',
                                        command= select_file())
    selectdata_boton.place(x=40, y=40)
                
    selectdata_entry = ctk.CTkEntry(root, width=270)
    selectdata_entry.place(x=270, y=40 )
    
    button_preview = ctk.CTkButton(root, text="Preview", width=510, fg_color='black', text_color='white', font=('Arial',16),
                                                command= lambda: preview(root))
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
    
        
