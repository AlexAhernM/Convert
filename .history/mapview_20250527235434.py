import tkinter 
import tkintermapview

root_tk = tkinter.Tk()
root_tk.geometry(f"{1200}x{800}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=90)
map_widget.set_position(41.8902, 12.4922, marker=True)  # Colosseo, Roma
map_widget.set_zoom(15)
#marker_1 = map_widget.set_marker(41.8902, 12.4922)
image = tkinter.PhotoImage(file="C:/Users/alex_/Downloads/Circle.png")
marker_1 = map_widget.set_marker(41.8902, 12.4922, text="Colosseo in Rome", image="C:/Users/alex_/Downloads/Circle.png")
print(marker_1.position, marker_1.text)  # get position and text
#marker_1.change_icon("C:/Users/alex_/Downloads/Circle.png")

marker_1.set_text("Colosseo in Rome")  # set new text
# marker_1.set_position(48.860381, 2.338594)  # change position
# marker_1.delete()
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root_tk.mainloop()
