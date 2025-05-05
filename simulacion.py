import asyncio
import random
from hospital import Hospital
from paciente import Paciente
from configuracion import NUM_PACIENTES, TIEMPO_ENTRE_LLEGADAS
from reportes import generar_reporte_pacientes

async def simular_urgencias():
    hospital = Hospital()
    pacientes = [Paciente(i) for i in range(1, NUM_PACIENTES + 1)]
    
    # Simular llegada escalonada de pacientes
    tasks = []
    for paciente in pacientes:
        tasks.append(hospital.procesar_paciente(paciente))
        await asyncio.sleep(TIEMPO_ENTRE_LLEGADAS * random.uniform(0.5, 1.5))
    
    await asyncio.gather(*tasks)
    generar_reporte_pacientes(pacientes)

if __name__ == "__main__":
    asyncio.run(simular_urgencias())