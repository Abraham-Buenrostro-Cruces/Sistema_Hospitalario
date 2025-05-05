import random
import concurrent.futures
import asyncio
from paciente import Paciente
import time

def diagnostico_ia(paciente: Paciente) -> dict:
    """Proceso intensivo que se ejecuta en paralelo"""
    print(f"🏥💡 Diagnóstico IA para el paciente {paciente.id} en progreso...")
    
    # Simulación de procesamiento pesado
    time.sleep(random.uniform(0.5, 2.0))
    
    sintomas = paciente.sintomas
    diagnostico = "Revisión general"
    urgencia = 3

    if "dificultad para respirar" in sintomas and "dolor en el pecho" in sintomas:
        diagnostico = "Posible ataque cardíaco"
        urgencia = 1
    elif "fiebre" in sintomas and "dolor de cabeza" in sintomas:
        diagnostico = "Infección viral"
        urgencia = 2
    elif "dolor abdominal" in sintomas:
        diagnostico = "Problema digestivo"
        urgencia = 2

    return {
        "diagnostico": diagnostico,
        "urgencia": urgencia,
        "tratamiento": generar_tratamiento(diagnostico)  # Quitamos self.
    }

def generar_tratamiento(diagnostico: str) -> str:
    """Mock de modelo IA para tratamiento"""
    tratamientos = {
        "Posible ataque cardíaco": "ECG y enzimas cardíacas",
        "Infección viral": "Reposo y antipiréticos",
        "Problema digestivo": "Endoscopia y dieta blanda"
    }
    return tratamientos.get(diagnostico, "Observación")

async def procesar_diagnosticos(pacientes: list, max_workers: int = 4):
    """Procesa diagnósticos en paralelo"""
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, diagnostico_ia, paciente)
            for paciente in pacientes
        ]
        return await asyncio.gather(*futures)