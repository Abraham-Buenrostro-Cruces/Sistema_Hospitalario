import asyncio
from typing import List
from paciente import Paciente
from recursos.camas import Camas
from recursos.doctores import Doctores
from diagnostico import procesar_diagnosticos
from configuracion import NUM_CAMAS, NUM_DOCTORES
import random

class Hospital:
    def __init__(self):
        self.camas = Camas(NUM_CAMAS)
        self.doctores = Doctores(NUM_DOCTORES)
        self.monitor_task = None

    async def admitir_paciente(self, paciente: Paciente) -> bool:
        """Proceso de admisión asíncrono"""
        cama_asignada = await self.camas.asignar_recurso(paciente)
        doctor_asignado = await self.doctores.asignar_recurso(paciente)
        
        if not cama_asignada or not doctor_asignado:
            print(f"❌ No hay recursos para paciente {paciente.id}")
            if cama_asignada:
                await self.camas.liberar_recurso(paciente.id)
            if doctor_asignado:
                await self.doctores.liberar_recurso(paciente.id)
            return False
        
        paciente.estado = "admitted"
        print(f"✅ Paciente {paciente.id} admitido")
        return True

    async def procesar_paciente(self, paciente: Paciente):
        """Flujo completo para un paciente"""
        try:
            if await self.admitir_paciente(paciente):
                # Procesamiento paralelo del diagnóstico
                resultados = await procesar_diagnosticos([paciente])
                resultado = resultados[0]  # Como solo procesamos un paciente
                
                paciente.diagnostico = resultado['diagnostico']
                paciente.urgencia = resultado['urgencia']
                paciente.tratamiento = resultado['tratamiento']
                
                # Simular tiempo de tratamiento
                await asyncio.sleep(random.uniform(1, 3))
                
                await self.camas.liberar_recurso(paciente.id)
                await self.doctores.liberar_recurso(paciente.id)
        except Exception as e:
            print(f"Error procesando paciente {paciente.id}: {str(e)}")
            # Asegurarse de liberar recursos en caso de error
            await self.camas.liberar_recurso(paciente.id)
            await self.doctores.liberar_recurso(paciente.id)

    async def monitorear_recursos(self):
        """Tarea asíncrona de monitoreo"""
        while True:
            print(f"\n📊 Monitor: Camas {self.camas.estado()} | Doctores {self.doctores.estado()}")
            await asyncio.sleep(5)

    async def procesar_pacientes(self, pacientes: List[Paciente]):
        """Procesamiento concurrente de pacientes"""
        # Ordenar por prioridad
        pacientes.sort(key=lambda x: x.prioridad)
        
        # Iniciar monitoreo
        self.monitor_task = asyncio.create_task(self.monitorear_recursos())
        
        # Procesar concurrentemente
        await asyncio.gather(*[self.procesar_paciente(p) for p in pacientes])
        
        # Detener monitoreo
        self.monitor_task.cancel()