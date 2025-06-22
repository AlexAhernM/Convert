
import customtkinter as ctk
from PIL import Image
from Select_file import select_file
from Preview import button_preview

def abrir_ventana_kml(self):
        
    self = ctk.CTkToplevel(self)   
    self.title("Convert KML Files")
    self.geometry('1200x600')
    self.configure(fg_color='ghost white', height= 25)
    self.grab_set()
    
    self.selectdata_boton = ctk.CTkButton(self, text='Select your KML File', width=200, fg_color='gray7', font=('Arial',16), text_color='white',
                                        command= lambda: select_file(self))

    
    self.selectdata_boton.place(x=40, y=40)
                
    self.selectdata_entry = ctk.CTkEntry(self, width=270)
    self.selectdata_entry.place(x=270, y=40 )
    
    self.checkbox_altitude = ctk.CTkCheckBox(self, text='Get Altitude')
    self.checkbox_altitude.configure(state='normal', border_width = 1, border_color = 'black')
    self.checkbox_altitude.place(x=80, y= 100)
    
    
    self.button_preview = ctk.CTkButton(self, text="Preview", width=510, fg_color='black', text_color='white', font=('Arial',16),
                                                command= lambda: button_preview(self))
    self.button_preview.configure(state= 'normal')
    self.button_preview.place(x=40, y =180)
    
    show_files_frame = ctk.CTkFrame(self, fg_color='snow', width=510, height=320)
    show_files_frame.place (x=40, y=350)
     
    



def preview(self):
    
    imagen_3 = Image.open("D:\\OneDrive\\tuto_vscode\\Convert\\amanecer.png")
    imagen_tk3 = ctk.CTkImage(light_image=imagen_3, dark_image=imagen_3, size=(600,320))
    
    try:                    
        
        self.label3 = ctk.CTkLabel(self, text='',image=imagen_tk3)
        self.label3.image = imagen_tk3  # mantener una referencia a la imagen
        self.label3.place(x=580, y = 140 )
        
        
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

