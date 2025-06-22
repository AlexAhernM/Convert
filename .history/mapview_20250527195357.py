import tkinter 
import tkintermapview

root_tk = tkinter.Tk()
root_tk.geometry(f"{1200}x{800}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.set_address("colosseo, rome, italy")
map_widget.set_zoom(17)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root_tk.mainloop()
