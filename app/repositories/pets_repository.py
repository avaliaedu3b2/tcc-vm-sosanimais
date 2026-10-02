from datetime import date, datetime

from firebase_admin import firestore

from app.models.pets import Pets


class PetsRepository:
    COLLECTION = 'pets'

    def get_all_pets(self) -> list[Pets]:
        db = firestore.client()
        docs = db.collection(self.COLLECTION).stream()
        return [self._from_doc(doc.id, doc.to_dict()) for doc in docs]

    def get_pets(self, pets_id: str) -> Pets | None:
        db = firestore.client()
        doc = db.collection(self.COLLECTION).document(pets_id).get()
        if doc.exists:
            return self._from_doc(doc.id, doc.to_dict())
        return None

    def add_pets(self, pet: Pets) -> str:
        db = firestore.client()
        _, ref = db.collection(self.COLLECTION).add(self._to_dict(pet))
        return ref.id

    def update_pets(self, pets_id: str, pet: Pets) -> bool:
        db = firestore.client()
        db.collection(self.COLLECTION).document(pets_id).update(self._to_dict(pet))
        return True

    @staticmethod
    def _from_doc(doc_id: str, data: dict) -> Pets:
        data_registro = data.get('data_registro')
        # O Firestore devolve datetime; o model usa date
        if isinstance(data_registro, datetime):
            data_registro = data_registro.date()
        return Pets(
            id=doc_id,
            nome=data.get('nome'),
            especie=data.get('especie'),
            raca=data.get('raca'),
            idade=data.get('idade'),
            sexo=data.get('sexo'),
            porte=data.get('porte'),
            cor=data.get('cor'),
            peso=data.get('peso'),
            vacinado=data.get('vacinado'),
            castrado=data.get('castrado'),
            microchip=data.get('microchip'),
            condicao_saude=data.get('condicao_saude'),
            status=data.get('status'),
            data_registro=data_registro,
            localizacao=data.get('localizacao'),
            tutor_id=data.get('tutor_id'),
            orgao_id=data.get('orgao_id'),
            foto_url=data.get('foto_url'),
            descricao=data.get('descricao'),
        )

    @staticmethod
    def _to_dict(pet: Pets) -> dict:
        data_registro = pet.data_registro
        # O Firestore não aceita date, só datetime
        if isinstance(data_registro, date) and not isinstance(data_registro, datetime):
            data_registro = datetime(data_registro.year, data_registro.month, data_registro.day)
        return {
            'nome': pet.nome,
            'especie': pet.especie,
            'raca': pet.raca,
            'idade': pet.idade,
            'sexo': pet.sexo,
            'porte': pet.porte,
            'cor': pet.cor,
            'peso': pet.peso,
            'vacinado': pet.vacinado,
            'castrado': pet.castrado,
            'microchip': pet.microchip,
            'condicao_saude': pet.condicao_saude,
            'status': pet.status,
            'data_registro': data_registro,
            'localizacao': pet.localizacao,
            'tutor_id': pet.tutor_id,
            'orgao_id': pet.orgao_id,
            'foto_url': pet.foto_url,
            'descricao': pet.descricao,
        }