
def widgets_destroy(self):
    for frame in [self.selectfile_frame, self.preview_frame,  self.checkbox_frame]:
        for widget in frame.winfo_children():
            widget.destroy()
    self.habilitar()