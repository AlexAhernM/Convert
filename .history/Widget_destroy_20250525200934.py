
def widgets_destroy(self):
        for widget in self.label3.winfo_children():
            widget.destroy()
   