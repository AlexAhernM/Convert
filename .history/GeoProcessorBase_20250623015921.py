from abc import ABC, abstractmethod

class GeoProcessorBase(ABC):
    def __init__(self, parent):
        self.parent = parent
        self.mapa_tkinter = None
        self.HomeImages = None

    @abstractmethod
    def procesar_archivo(self):
        """Procesa el archivo geoespacial. Debe ser implementado por cada subclase."""
        pass

    @abstractmethod
    def update_preview(self, *args, **kwargs):
        """Actualiza la vista previa del mapa. Debe ser implementado por cada subclase."""
        pass

    @abstractmethod
    def confirmar_localizacion(self, *args, **kwargs):
        """Confirma la localización con el usuario. Debe ser implementado por cada subclase."""
        pass
