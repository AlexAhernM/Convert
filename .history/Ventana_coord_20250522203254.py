

import customtkinter as ctk
from PIL import Image

def abrir_ventana_cor(master):

    root = ctk.CTkToplevel(master)
    root.title("Convert KML Files")
    root.geometry('1200x600')
    root.configure(fg_color='white', height= 25)
    root.grab_set()
       
        
    imagen_4= Image.open("D:\\OneDrive\\tuto_vscode\\Conversion\\Atardecer_anf.png")
    imagen_4 = imagen_4.resize((400, 200)) 
    imagen_tk4 = ctk.CTkImage(light_image=imagen_4, dark_image=imagen_4, size=(400,200))
    print ('imagen tk4 creada')
    try:                    
        label4 = ctk.CTkLabel(root, text='', image= imagen_tk4)
        print('label creado')
        label4.image = imagen_tk4  # mantener una referencia a la imagen
        print ('label imagen creado')
        label4.place(x=530, y = 180 )
        print ('imagen place')
            
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
    
        
