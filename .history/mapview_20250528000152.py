
import tkinter 
import tkintermapview

root_tk = tkinter.Tk()
root_tk.geometry(f"{1200}x{800}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=90)
map_widget.set_position(41.8902, 12.4922)  # Colosseo, Roma
map_widget.set_zoom(15)

image = tkinter.PhotoImage(file="C:/Users/alex_/Downloads/Circle.png")
marker_1 = map_widget.set_marker(41.8902, 12.4922, text="Colosseo in Rome", image=image)

# Eliminar el marcador actual y crear un nuevo marcador con el nuevo icono
marker_1.delete()
new_image = tkinter.PhotoImage(file="C:/Users/alex_/Downloads/Circle.png")
marker_2 = map_widget.set_marker(41.8902, 12.4922, text="Colosseo in Rome", image=new_image)

map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root_tk.mainloop()
