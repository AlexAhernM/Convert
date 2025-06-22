import customtkinter
from Convert_file import convert_file, widgets_destroy
import requests
from PIL import Image
from io import BytesIO

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Geo Convert Program by Ambylog")
        self.after(0, lambda:app.state('zoomed'))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
                
        # FRAME: ROW 0 - SELECT FILE
        self.selectfile_frame = customtkinter.CTkFrame(self)
        #self.selectfile_frame.place(x=10, y=10)
        self.selectfile_frame.grid(row=0, column = 0, padx=10, pady=10, sticky='ew')
        self.selectfile_frame.grid_propagate(False)
        
        # FRAME: ROW 0 - INTERMEDIO RADIOBUTTOMS - TIPO DE FORMATO A TRANSFORMAR
        self.intermedio_frame = customtkinter.CTkFrame(self)
        #self.intermedio_frame.place(x= 560, y=10)
        self.intermedio_frame.grid(row=0, column = 1, padx=10, pady=10)
        self.intermedio_frame.grid_propagate(False)
        
        self.tipo_geo = customtkinter.StringVar()
        self.rbuttomkml = customtkinter.CTkRadioButton(self.intermedio_frame, text=" From KML", variable=self.tipo_geo, value="KML",
                                                       command=self.habilitar_boton)
        self.rbuttomkml.grid(row=0, column=0, padx=10, pady=(20,10),  sticky='w')
        
        self.rbuttomcord = customtkinter.CTkRadioButton(self.intermedio_frame, text="From Coords", variable=self.tipo_geo, value="Coordenadas",
                                                        command=self.habilitar_boton)
        self.rbuttomcord.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        self.convert_file = customtkinter.CTkButton(self.intermedio_frame, text='Convert File', command=lambda: convert_file(self))
        self.convert_file.grid(row=2, column=0, padx=(65,0), pady=(44,0), sticky='w')
        self.convert_file.configure(state='disabled')
        self.habilitar()
        # FRAME: ROW 0 -  CHECKBOXS Y MESSAGES
        
        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.place(x=900,y=10)
        #self.checkbox_frame.grid(row=0, column=3, padx =10, pady=10, sticky = 'ew' )
        
        # FRAME: ROW 2 - MAP PREVIEW
        # Creación del frame de vista previa
        self.preview_frame = customtkinter.CTkFrame(self,  fg_color='white')
        self.preview_frame.grid(row=2, column=0, padx=10, pady=5, columnspan=4, sticky='nsew')
        self.preview_frame.grid_columnconfigure(0, weight=1)
        
        self.show_image_in_preview() 
        #self.show_image_in_labels()

    def deseleccionar(self):
        self.rbuttomkml.configure(state='disabled')
        self.rbuttomcord.configure(state='disabled') 
        self.tipo_geo.set("")
        
    def habilitar (self):
        self.rbuttomkml.configure(state='normal')
        self.rbuttomcord.configure(state='normal') 
        
    def habilitar_boton(self):
        if self.tipo_geo.get() == "KML":
            self.convert_file.configure(state='normal')
        elif self.tipo_geo.get() == "Coordenadas":
            self.convert_file.configure(state='normal')  # o cualquier otra lógica que desees aplicar
        else:
            self.convert_file.configure(state='disabled')

    def show_image_in_preview(self):

        images_config = [
            {"url": "https://raw.githubusercontent.com/AlexAhernM/Converter/master/earth1.png", "size": (1440, 530)},
            {"url": "https://raw.githubusercontent.com/AlexAhernM/Converter/master/Atardecer_anf.png", "size": (300, 180)},
            {"url": "https://raw.githubusercontent.com/AlexAhernM/Converter/master/amanecer.png", "size": (300, 180)}
        ]
        
         # Descargar las imágenes y crear CTkImage
        self.preview_images = []
        for config in images_config:
            response = requests.get(config["url"])
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                preview_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=config["size"])
                self.preview_images.append(preview_image)
            else:
                print(f"Error al descargar la imagen: {response.status_code}")
                
        # Crear y mostrar el CTkLabel (si no existe)
        
        self.preview_label1 = customtkinter.CTkLabel(self.preview_frame, text="", image=self.preview_images[0])
        self.preview_label1.pack(expand = True, fill ='both')
        
    def show_image_in_labels(self):
        self.preview_label2 = customtkinter.CTkLabel(self.selectfile_frame, text="", image=self.preview_images[1])
        self.preview_label2.grid(row=0, column=0, padx=120, pady=2, sticky='nsew')
        
        self.preview_label3 = customtkinter.CTkLabel(self.checkbox_frame, text="", image=self.preview_images[2])
        self.preview_label3.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
                                                        
    
app = App()
app.mainloop()