import asyncio
from typing import Optional
from paciente import Paciente

class Doctores:
    def __init__(self, total_doctores: int):
        self.total_doctores = total_doctores
        self.doctores_disponibles = total_doctores
        self.semaphore = asyncio.Semaphore(total_doctores)  # Usar asyncio.Semaphore
        self.asignaciones = {}

    async def asignar_recurso(self, paciente: Paciente) -> bool:
        """Asigna doctor con semáforo"""
        if await self.semaphore.acquire():
            self.doctores_disponibles -= 1
            self.asignaciones[paciente.id] = paciente
            print(f"🩺 Doctor asignado al paciente {paciente.id}")
            return True
        return False

    async def liberar_recurso(self, paciente_id: int):
        """Libera doctor"""
        if paciente_id in self.asignaciones:
            self.doctores_disponibles += 1
            del self.asignaciones[paciente_id]
            self.semaphore.release()
            print(f"✅👨‍⚕️ Doctor liberado por paciente {paciente_id}")

    def estado(self) -> dict:
        return {
            "total": self.total_doctores,
            "disponibles": self.doctores_disponibles,
            "ocupados": self.total_doctores - self.doctores_disponibles
        }