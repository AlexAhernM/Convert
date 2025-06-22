import customtkinter as ctk
from PIL import Image
from Select_file import select_file
from Preview import button_preview
from Imagen_windows2 import ventana_segunda_imagen

class VentanaSegunda:
    def __init__(self, root):
            
        self.ventana_segunda = ctk.CTkToplevel(root.root)   
        self.ventana_segunda.title("Convert KML Files")
        self.ventana_segunda.geometry('1300x600')
        self.color_ventana = 'white'
        self.ventana_segunda.configure(fg_color= self.color_ventana)
        self.ventana_segunda.grab_set()
        
        self.abrir_ventana_kml()
        
    def abrir_ventana_kml(self):
    
        self.selectdata_boton = ctk.CTkButton(self.ventana_segunda, text='Select your KML File', width=200, fg_color='gray7', font=('Arial',16), text_color='white',
                                            command= lambda: select_file(self))

        
        self.selectdata_boton.place(x=40, y=40)
                    
        self.selectdata_entry = ctk.CTkEntry(self.ventana_segunda, width=270)
        self.selectdata_entry.place(x=270, y=40 )
        
        self.checkbox_altitude = ctk.CTkCheckBox(self.ventana_segunda, text='Get Altitude', text_color_disabled=self.color_ventana)
        self.checkbox_altitude.configure(state='disabled', border_width = 1, border_color = self.color_ventana, text_color=self.color_ventana)
        self.checkbox_altitude.place(x=140, y= 100)
        
        
        self.button_preview = ctk.CTkButton(self.ventana_segunda, text="Preview", width=510, fg_color='black', text_color='white', font=('Arial',16),
                                                    command= lambda: button_preview(self))
        self.button_preview.configure(state= 'normal')
        self.button_preview.place(x=40, y =140)
        
        self.show_files_frame = ctk.CTkFrame(self.ventana_segunda, fg_color=self.color_ventana, width=510, height=320)
        self.show_files_frame.place (x=40, y=260)
        
        ventana_segunda_imagen(self)
    
