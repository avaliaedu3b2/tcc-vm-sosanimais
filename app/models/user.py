from dataclass import dataclasss

@dataclass
class user:
    uid: str
    nome:str
    email: str
    created_at: str = None
    update_at: str = None