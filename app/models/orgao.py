from dataclasses import dataclass
from typing import Optional


@dataclass
class Orgao:
    uid: str
    nome_orgao: str
    email: str
    cnpj: str
    status: str  # "pendente" | "aprovado" | "rejeitado"
    created_at: Optional[object] = None
    updated_at: Optional[object] = None