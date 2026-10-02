from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Pets:
    nome: str
    especie: str
    raca: str
    idade: int
    sexo: str
    porte: str
    cor: str
    peso: float
    vacinado: bool
    castrado: bool
    status: str
    data_registro: date
    localizacao: str
    id: Optional[str] = None
    microchip: Optional[str] = None
    condicao_saude: Optional[str] = None
    tutor_id: Optional[str] = None
    orgao_id: Optional[str] = None
    foto_url: Optional[str] = None
    descricao: Optional[str] = None