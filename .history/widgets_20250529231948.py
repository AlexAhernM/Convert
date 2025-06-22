import customtkinter as ctk
from PIL import Image
from Ventana_kml import VentanaSegunda
from Ventana_coord import VentanaTercera

class VentanaPrincipal:
    def __init__(self):
        self.root = ctk.CTk()
        
        self.root.title("Geo Convert Program by Ambylog")
        self.root.after(0, lambda: self.root.state('zoomed'))
        self.root.state('zoomed')
        self.root.configure(fg_color='white')
    
        self.root.boton_inic1 = ctk.CTkButton(self.root, text='Convert your KML/KMZ files into..\n CAD, Shapefile or Excel', font=('Arial',36),
                                text_color='white',width=520, height=140, fg_color='navy', 	hover_color='midnight blue',
                                command= lambda: VentanaSegunda(self),  corner_radius=20)
        
        self.root.boton_inic1.configure(cursor='hand2')                              
        self.root.boton_inic1.place(x=30, y=200) 
        
        self.root.boton_inic2 = ctk.CTkButton(self.root, text='Convert coordinates (in Excel)..\n into KML, CAD or Shapefile', font=('Arial',36),
                                text_color='white', width=520, height=140, fg_color='navy',  hover_color='midnight blue',
                                command= lambda: VentanaTercera(self) ,corner_radius=20)
        
        self.root.boton_inic2.configure(cursor='hand2' )                              
        self.root.boton_inic2.place(x=30, y=400) 
        
        imagen1 = Image.open("D:\\OneDrive\\tuto_vscode\\Convert\\mundo.png")
        imagen_tk1 = ctk.CTkImage(light_image=imagen1, dark_image=imagen1, size=(760,360))
        
        label1 = ctk.CTkLabel(self.root,image=imagen_tk1, text="")
        label1.image = imagen_tk1  # mantener una referencia a la imagen
        label1.place(x=700, y=180)
        
        imagen2 = Image.open("D:\\OneDrive\\tuto_vscode\\Conversion\\AMBYLOG.png")
        imagen_tk2 = ctk.CTkImage(light_image=imagen2, dark_image=imagen2, size=(240,100))

        label2 = ctk.CTkLabel(self.root, image=imagen_tk2, text="")
        label2.image = imagen_tk2  # mantener una referencia a la imagen
        label2.place(x=30, y=20)
   
    def run(self):
        self.root.mainloop()     

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.run()