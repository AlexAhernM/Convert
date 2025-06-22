

    
import customtkinter as ctk
from widgets import imagen_tk3

class App1(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        self.title("Convert KML Files")
        self.geometry('1200x600')
        self.configure(fg_color='white', height= 25)
        self.selectdata_boton = ctk.CTkButton(self, text='Select your KML File', width=200, fg_color='gray7', font=('Arial',16), text_color='white',
                                            command= self.select_file())
        self.selectdata_boton.place(x=40, y=40)
                    
        self.selectdata_entry = ctk.CTkEntry(self, width=270)
        self.selectdata_entry.place(x=270, y=40 )
        
        self.button_preview = ctk.CTkButton(self, text="Preview", width=510, fg_color='black', text_color='white', font=('Arial',16),
                                                    command= self.preview())
        self.button_preview.configure(state= 'normal')
        self.button_preview.place(x=40, y =180)
        
        self.show_files_frame = ctk.CTkFrame(self, fg_color='ghost white', width=510, height=320)
        self.show_files_frame.place (x=40, y=220)
        
        try:                    
            
            self.label3 = ctk.CTkLabel(self, text='',image=imagen_tk3)
            print ('label  creado')
            self.label3.image = imagen_tk3  # mantener una referencia a la imagen
            print ('referencia creada')
            self.label3.place(x=580, y = 40 )
            print ('imagen place')
                
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")

    def select_file(self):
        # función para seleccionar archivo
        pass

    def preview(self):
        # función para preview
        pass

app = App1()
app.mainloop()