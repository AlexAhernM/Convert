import customtkinter as ctk
from Select_cor import select_cor
#from Preview import preview_kml
from Select_cor import convert_cor
from Imagen_windows2 import ventana_tercera_imagen

class VentanaTercera(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)  
        self.title("Convert Coord to KML, CAD or Shapefile")
        self.geometry('1300x600')
        self.color_ventana = 'red'
        self.configure(fg_color= self.color_ventana)
        self.grab_set()
        
        self.abrir_ventana_cor()
        
    def abrir_ventana_cor(self):
    
        self.selectcor_boton = ctk.CTkButton(self, text='Select your Excel File', width=200, fg_color='gray7', font=('Arial',16), text_color='white',
                                            command= lambda: select_cor(self))

        
        self.selectcor_boton.place(x=40, y=40)
                    
        self.selectcor_entry = ctk.CTkEntry(self, width=270)
        self.selectcor_entry.place(x=270, y=40 )
        
               
        self.boton_cor_preview = ctk.CTkButton(self, text="Preview", width=510, fg_color='black', text_color='white', font=('Arial',16),
                                                    command= lambda: preview_xlx(self))
        self.boton_cor_preview.configure(state= 'normal')
        self.boton_cor_preview.place(x=40, y =210)
        
        convert_cor(self)
        
        self.show_cor_frame = ctk.CTkFrame(self, fg_color=self.color_ventana, width=510, height=320)
        self.show_cor_frame.place (x=40, y=250)
        
        ventana_tercera_imagen(self)
    
