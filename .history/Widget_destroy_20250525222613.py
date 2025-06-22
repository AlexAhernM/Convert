
def widgets_destroy(self):
    if self.label3.winfo_exists():
        for widget in self.label3.winfo_children():
            widget.destroy()
    