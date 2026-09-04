from dataclasses import dataclass
from datatime import Optional


@dataclass
class User:
    uid: str
    nome: str
    email: str
    senha: Optional[str] = None
    telefone: Optional[str] = None
    created_at: datatime = field(default_factory=datatime.utcnow) 