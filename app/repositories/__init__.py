from datetime import date

from app.repositories.pets_repository import PetsRepository
from app.models.pets import Pets


class PetsService:
    def __init__(self):
        self.pets_repo = PetsRepository()

    def get_all_pets(self):
        return self.pets_repo.get_all_pets()

    def _build_pets(self, data: dict) -> Pets:
        return Pets(
            nome=data.get('nome'),
            especie=data.get('especie'),
            raca=data.get('raca'),
            idade=int(data.get('idade', 0)),
            sexo=data.get('sexo'),
            porte=data.get('porte'),
            cor=data.get('cor'),
            peso=float(data.get('peso', 0)),
            vacinado=bool(data.get('vacinado', False)),
            castrado=bool(data.get('castrado', False)),
            status=data.get('status', 'disponivel'),
            data_registro=date.today(),
            localizacao=data.get('localizacao'),
            microchip=data.get('microchip'),
            condicao_saude=data.get('condicao_saude'),
            tutor_id=data.get('tutor_id'),
            orgao_id=data.get('orgao_id'),
            foto_url=data.get('foto_url'),
            descricao=data.get('descricao'),
        )

    def add_pets(self, data: dict):
        return self.pets_repo.add_pets(self._build_pets(data))

    def update_pets(self, pets_id: str, data: dict):
        return self.pets_repo.update_pets(pets_id, self._build_pets(data))