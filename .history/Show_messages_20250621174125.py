import customtkinter as ctk
import os
import re
from Widget_destroy import widgets_destroy
from tkinter import messagebox

class ShowMessages:
    def __init__(self, parent):
        self.parent = parent

    def show_messages(self, messages):
        msg_dxf, msg_shp, msg_xlx, msg_pdf = messages
        color_texto = 'black'
        font_texto = ('Arial', 12)

        ruta_dxf = self._extract_path(msg_dxf, r'C:\\.*\\.dxf')
        ruta_shp = self._extract_path(msg_shp, r'C:\\.*\\.shp')
        ruta_xlx = self._extract_path(msg_xlx, r'C:\\.*\\.xlsx')
        ruta_pdf = self._extract_path(msg_pdf, r'C:\\.*\\.pdf')

        self._setup_ui()

        x = 20
        y = 10

        if msg_dxf:
            self._create_file_display(x, y, 'CAD file has been generated in the following path : ', msg_dxf, ruta_dxf)
            y += 60

        if msg_shp:
            self._create_file_display(x, y, 'Shapefile has been generated in the following path : ', msg_shp, ruta_shp)
            y += 60

        if msg_xlx:
            self._create_file_display(x, y, 'Excel file has been generated in the following path : ', msg_xlx, ruta_xlx)
            y += 60

        if msg_pdf:
            self._create_file_display(x, y, 'PDF file has been generated in the following path : ', msg_pdf, ruta_pdf)
            y += 60

    def show_single_file(self, file_path, file_type):
        self._setup_ui()
        x = 20
        y = 10
        label_text = f'{file_type} file has been generated in the following path : '
        self._create_file_display(x, y, label_text, file_path, file_path)

    def _extract_path(self, message, pattern):
        match = re.search(pattern, message)
        return match.group() if match else None

    def _setup_ui(self):
        self.parent.label_mappreview.configure(text='Vision Preliminar Area Geografica Procesada')
        self.parent.boton_limpiar = ctk.CTkButton(self.parent, text="CLEAN", command=lambda: widgets_destroy(self.parent),
                                                  fg_color='black', text_color='white', width=150, height=25, corner_radius=6)
        self.parent.boton_limpiar.place(x=40, y=520)

        self.parent.boton_cerrar = ctk.CTkButton(self.parent, text="CLOSE", command=self.parent.destroy,
                                                 fg_color='black', text_color='white', width=150, height=25, corner_radius=6)
        self.parent.boton_cerrar.place(x=300, y=520)

    def _create_file_display(self, x, y, label_text, button_text, file_path):
        label = ctk.CTkLabel(self.parent.show_files_frame, text=label_text)
        button = ctk.CTkButton(self.parent.show_files_frame, text=button_text, text_color='black', fg_color="transparent",
                               hover_color=self.parent.show_files_frame.cget("fg_color"), border_width=0, font=('Arial', 12))

        if file_path:
            label.place(x=x, y=y)
            button.configure(command=lambda ruta=file_path: self._abrir_archivo(ruta))
            button.place(x=x, y=y+20)

    def _abrir_archivo(self, ruta):
        try:
            os.startfile(ruta)
        except OSError:
            messagebox.showerror("Error", f"No se pudo abrir el archivo {ruta}. Asegúrate de que haya una aplicación asociada.")
