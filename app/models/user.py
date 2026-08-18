from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    uid: str
    nome: str
    email: str
    senha: Optional[str] = None
    telefone: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None