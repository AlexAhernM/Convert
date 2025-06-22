import customtkinter as ctk
from Select_file import select_file
from Preview import button_preview
from Imagen_windows2 import _imagen

class VentanaSegunda(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
            
  
        self..title("Convert KML Files")
        self..geometry('1300x600')
        self.color_ventana = 'snow'
        self..configure(fg_color= self.color_ventana)
        self..grab_set()
        
        self.abrir_ventana_kml()
        
    def abrir_ventana_kml(self):
    
        self.selectdata_boton = ctk.CTkButton(self., text='Select your KML File', width=200, fg_color='gray7', font=('Arial',16), text_color='white',
                                            command= lambda: select_file(self))

        
        self.selectdata_boton.place(x=40, y=40)
                    
        self.selectdata_entry = ctk.CTkEntry(self., width=270)
        self.selectdata_entry.place(x=270, y=40 )
        
        self.checkbox_altitude = ctk.CTkCheckBox(self., text='Get Altitude', text_color_disabled=self.color_ventana)
        self.checkbox_altitude.configure(state='disabled', border_width = 1, border_color = self.color_ventana, text_color=self.color_ventana)
        self.checkbox_altitude.place(x=140, y= 100)
        
        
        self.button_preview = ctk.CTkButton(self., text="Preview", width=510, fg_color='black', text_color='white', font=('Arial',16),
                                                    command= lambda: button_preview(self))
        self.button_preview.configure(state= 'normal')
        self.button_preview.place(x=40, y =140)
        
        self.show_files_frame = ctk.CTkFrame(self., fg_color=self.color_ventana, width=510, height=320)
        self.show_files_frame.place (x=40, y=260)
        
        _imagen(self)
    
