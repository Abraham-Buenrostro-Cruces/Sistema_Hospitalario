import asyncio
from typing import Optional
from paciente import Paciente

class Camas:
    def __init__(self, total_camitas: int):
        self.total_camitas = total_camitas
        self.camitas_disponibles = total_camitas
        self.lock = asyncio.Lock()  # Usar asyncio.Lock en lugar de threading.Lock
        self.asignaciones = {}

    async def asignar_recurso(self, paciente: Paciente) -> bool:
        """Asigna cama de forma asíncrona con control de concurrencia"""
        async with self.lock:
            if self.camitas_disponibles > 0:
                self.camitas_disponibles -= 1
                self.asignaciones[paciente.id] = paciente
                print(f"🛏️ Cama asignada al paciente {paciente.id}")
                return True
            return False

    async def liberar_recurso(self, paciente_id: int):
        """Libera cama de forma asíncrona"""
        async with self.lock:
            if paciente_id in self.asignaciones:
                self.camitas_disponibles += 1
                del self.asignaciones[paciente_id]
                print(f"✅🛏️ Cama liberada por paciente {paciente_id}")

    def estado(self) -> dict:
        """Devuelve estado actual de las camas"""
        return {
            "total": self.total_camitas,
            "disponibles": self.camitas_disponibles,
            "ocupadas": self.total_camitas - self.camitas_disponibles
        }