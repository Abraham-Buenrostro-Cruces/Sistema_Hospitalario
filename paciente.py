import random
from dataclasses import dataclass, field
from typing import List

@dataclass(order=True)
class Paciente:
    id: int
    prioridad: int = field(default_factory=lambda: random.randint(1, 3))
    estado: str = "waiting"
    sintomas: List[str] = field(default_factory=lambda: random.sample([
        "fiebre", "dolor de cabeza", "dificultad para respirar",
        "dolor abdominal", "mareo", "dolor en el pecho"
    ], k=random.randint(1, 3)))
    diagnostico: str = None
    urgencia: int = None
    tratamiento: str = None

    def __repr__(self):
        return f"Paciente {self.id} (Prioridad {self.prioridad})"