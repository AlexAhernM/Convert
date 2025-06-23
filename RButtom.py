class Rbutton:
    def __init__(self, master, values, x=30, y=80, x_spacing=200, y_spacing=60):
        self.rbuttons = []
        self.labels = []
        self.var = ctk.IntVar(value=-1)

        for i, value in enumerate(values):
            label = ctk.CTkLabel(master, text=value, fg_color='red')
            label.place(x=x + (i % 2) * x_spacing, y=y + (i // 2) * y_spacing)

            rbutton = ctk.CTkRadioButton(master, variable=self.var, value=i, text='')
            rbutton.place(x=x + (i % 2) * x_spacing + 40, y=y + (i // 2) * y_spacing + 25)

            self.rbuttons.append(rbutton)
            self.labels.append(label)

    def get_value(self):
        return self.var.get()

    def set_value(self, index):
        self.var.set(index)
