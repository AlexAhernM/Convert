
import customtkinter as ctk


class Rbutton:
    def __init__(self, master, values, x=30, y=80, x_spacing=200, y_spacing=60,
                 orientation='horizontal', label_color='white', use_labels=True):
        self.rbuttons = []
        self.var = ctk.IntVar(value=-1)

        for i, value in enumerate(values):
            pos_x = x + (i if orientation == 'horizontal' else 0) * x_spacing
            pos_y = y + (i if orientation == 'vertical' else 0) * y_spacing

            if use_labels:
                label = ctk.CTkLabel(master, text=value, fg_color=label_color)
                label.place(x=pos_x, y=pos_y)
                rbutton = ctk.CTkRadioButton(master, variable=self.var, value=i, text='')
                rbutton.place(x=pos_x + 40, y=pos_y + 25)
            else:
                rbutton = ctk.CTkRadioButton(master, variable=self.var, value=i, text=value)
                rbutton.place(x=pos_x, y=pos_y)

            self.rbuttons.append(rbutton)

    def get_value(self):
        return self.var.get()

    def set_value(self, index):
        self.var.set(index)

    def set_state(self, state='normal'):
        for rbutton in self.rbuttons:
            rbutton.configure(state=state)
