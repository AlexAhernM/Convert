import customtkinter as ctk
from PIL import Image
from Select_file import select_file
from Preview import button_preview

class VentanaSegunda:
    def __init__(self, root):
            
        self.ventana_segunda = ctk.CTkToplevel(root.root)   
        self.ventana_segunda.title("Convert KML Files")
        self.ventana_segunda.geometry('1300x600')
        self.ventana_segunda.configure(fg_color='ghost white')
        self.ventana_segunda.grab_set()
        
        self.abrir_ventana_kml()
        
    def abrir_ventana_kml(self):
    
        self.selectdata_boton = ctk.CTkButton(self.ventana_segunda, text='Select your KML File', width=200, fg_color='gray7', font=('Arial',16), text_color='white',
                                            command= lambda: select_file(self))

        
        self.selectdata_boton.place(x=40, y=40)
                    
        self.selectdata_entry = ctk.CTkEntry(self.ventana_segunda, width=270)
        self.selectdata_entry.place(x=270, y=40 )
        
        self.checkbox_altitude = ctk.CTkCheckBox(self.ventana_segunda, text='Get Altitude')
        self.checkbox_altitude.configure(state='normal', border_width = 1, border_color = 'black')
        self.checkbox_altitude.place(x=140, y= 100)
        
        
        self.button_preview = ctk.CTkButton(self.ventana_segunda, text="Preview", width=510, fg_color='black', text_color='white', font=('Arial',16),
                                                    command= lambda: button_preview(self))
        self.button_preview.configure(state= 'normal')
        self.button_preview.place(x=40, y =140)
        
        self.show_files_frame = ctk.CTkFrame(self.ventana_segunda, fg_color='blue', width=510, height=440)
        self.show_files_frame.place (x=40, y=180)
        
        
        imagen_3 = Image.open("D:\\OneDrive\\tuto_vscode\\Convert\\amanecer.png")
        imagen_tk3 = ctk.CTkImage(light_image=imagen_3, dark_image=imagen_3, size=(700,400))
        
        try:                    
            
            self.label3 = ctk.CTkLabel(self.ventana_segunda, text='',image=imagen_tk3, width=620,height=500)
            self.label3.image = imagen_tk3  # mantener una referencia a la imagen
            self.label3.place(x=580, y = 100 )
            
            
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
