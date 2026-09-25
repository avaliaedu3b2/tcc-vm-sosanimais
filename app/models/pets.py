from dataclass import dataclass

@dataclass
class Pets:
    str
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
    microchip: Optional[str]
    condicao_saude: Optional[str]
    status: str
    data_registro: date
    localizacao: str
    tutor_id: Optional[str]
    orgao_id: Optional[str]
    foto_url: Optional[str]
    descricao: Optional[str]