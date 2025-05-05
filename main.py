from hospital import Hospital
from paciente import Paciente
from configuracion import NUM_PACIENTES  # Importar la configuración
def iniciar_simulacion():
    # Crear pacientes
    pacientes = [Paciente(i) for i in range(1, NUM_PACIENTES + 1)]  # Crear pacientes dinámicamente según la configuración
    hospital = Hospital()

    # Procesar los pacientes en el hospital
    hospital.procesar_pacientes(pacientes)

    # Generar el reporte
    hospital.generar_reporte(pacientes)

if __name__ == "__main__":
    iniciar_simulacion()
