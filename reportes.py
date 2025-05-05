import random
import os
from datetime import datetime

def generar_reporte_pacientes(pacientes):
    # Crear el nombre de archivo con la fecha y hora actual
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"reporte_pacientes_{fecha_hora}.txt"
    
    # Asegurarnos de que el archivo se guarde en el directorio correcto
    ruta_archivo = os.path.join("reportes", nombre_archivo)
    
    # Crear el directorio 'reportes' si no existe
    if not os.path.exists("reportes"):
        os.makedirs("reportes")

    # Abrir el archivo en modo de escritura con codificación UTF-8
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        # Escribir el encabezado del reporte
        archivo.write("📄 Reporte generado: {}\n".format(fecha_hora))
        archivo.write("="*50 + "\n")

        admitidos = 0
        retirados = 0
        # Recorrer cada paciente y escribir su información
        for paciente in pacientes:
            archivo.write(f"👨👩‍🦰 Paciente {paciente.id}\n")
            archivo.write(f"🧪 Síntomas: {', '.join(paciente.sintomas)}\n")
            archivo.write(f"🩻 Diagnóstico: {paciente.diagnostico}\n")
            archivo.write(f"💉 Nivel de urgencia: {paciente.urgencia}\n")  # Cambiado a urgencia
            archivo.write(f"🏨 Estado final: {paciente.estado}\n")
            archivo.write("-"*50 + "\n")
            
            # Contabilizamos los pacientes admitidos y retirados
            if paciente.estado == "admitted":
                admitidos += 1
            else:
                retirados += 1

        # Escribir el reporte final
        archivo.write(f"\n📈 Reporte Final del Hospital\n")
        archivo.write(f"👥 Total de pacientes simulados: {len(pacientes)}\n")
        archivo.write(f"✅ Admitidos: {admitidos}\n")
        archivo.write(f"❌ Se retiraron: {retirados}\n")
        archivo.write("\n")
        
        # Clasificación por niveles de urgencia
        for nivel in range(1, 4):
            admitidos_nivel = sum(1 for p in pacientes if hasattr(p, 'urgencia') and p.urgencia == nivel and p.estado == "admitted")
            retirados_nivel = sum(1 for p in pacientes if hasattr(p, 'urgencia') and p.urgencia == nivel and p.estado == "left")
            archivo.write(f"\n🔢 Prioridad {nivel}:\n")
            archivo.write(f"   ✅ Admitidos: {admitidos_nivel}\n")
            archivo.write(f"   ❌ Retirados: {retirados_nivel}\n")

    print(f"Reporte guardado en {ruta_archivo}")