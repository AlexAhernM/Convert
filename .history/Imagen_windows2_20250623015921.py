import customtkinter as ctk
from PIL import Image


def ventana_segunda_imagen(self):   
    imagen_3 = Image.open("D:\\OneDrive\\tuto_vscode\\Convert\\amanecer.png")
    imagen_tk3 = ctk.CTkImage(light_image=imagen_3, dark_image=imagen_3, size=(700,400))
    
    try:                    
        
        self.HomeImages = ctk.CTkLabel(self, text='',image=imagen_tk3, width=620,height=500)
        self.HomeImages.image = imagen_tk3  # mantener una referencia a la imagen
        self.HomeImages.place(x=580, y = 100 )
        
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
            
def ventana_tercera_imagen(self):
    imagen_4 = Image.open("D:\\OneDrive\\tuto_vscode\\Convert\\atardecer.png")
    imagen_tk4 = ctk.CTkImage(light_image=imagen_4, dark_image=imagen_4, size=(700,400))
        
    try:                    
            
        self.HomeImages = ctk.CTkLabel(self, text='',image=imagen_tk4, width=620,height=500)
        self.HomeImages.image = imagen_tk4  # mantener una referencia a la imagen
        self.HomeImages.place(x=580, y = 100 )
                    
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")