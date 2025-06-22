import customtkinter as ctk

class MovingText:
    def __init__(self, master):
        self.master = master
        self.label = ctk.CTkLabel(master, text="", width=200, height=20)
        self.label.pack()
        self.text = "Este texto se mueve horizontalmente"
        self.x = 0
        self.update_text()

    def update_text(self):
        self.label.configure(text=self.text[self.x:] + " " + self.text[:self.x])
        self.x = (self.x + 1) % len(self.text)
        self.master.after(100, self.update_text)

root = ctk.CTk()
app = MovingText(root)
root.mainloop()
