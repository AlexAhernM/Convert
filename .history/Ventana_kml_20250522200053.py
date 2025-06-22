
import customtkinter as ctk

def abrir_ventana_kml(master):
        
    root = ctk.CTkToplevel(master)   
    root.title("Convert KML Files")
    root.geometry('1200x600')
    root.configure(fg_color='white', height= 25)
    
    selectdata_boton = ctk.CTkButton(root, text='Select your KML File', width=200, fg_color='gray7', font=('Arial',16), text_color='white',
                                        command= select_file())
    selectdata_boton.place(x=40, y=40)
                
    selectdata_entry = ctk.CTkEntry(root, width=270)
    selectdata_entry.place(x=270, y=40 )
    
    button_preview = ctk.CTkButton(root, text="Preview", width=510, fg_color='black', text_color='white', font=('Arial',16),
                                                command= lambda: preview(root))
    button_preview.configure(state= 'normal')
    button_preview.place(x=40, y =180)
    
    show_files_frame = ctk.CTkFrame(root, fg_color='ghost white', width=510, height=320)
    show_files_frame.place (x=40, y=220)
     
    root.mainloop   

def select_file():
    # función para seleccionar archivo
    pass

def preview(root):
    from PIL import Image
    imagen_3 = Image.open("D:\\OneDrive\\tuto_vscode\\Convert\\amanecer.png")
    imagen_tk3 = ctk.CTkImage(light_image=imagen_3, dark_image=imagen_3, size=(600,320))
    print ('imagen tk3  creada')
    
    try:                    
        
        label3 = ctk.CTkLabel(root, text='',image=imagen_tk3)
        print ('label  creado')
        label3.image = imagen_tk3  # mantener una referencia a la imagen
        print ('referencia creada')
        label3.place(x=580, y = 40 )
        print ('imagen place')
        
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")


