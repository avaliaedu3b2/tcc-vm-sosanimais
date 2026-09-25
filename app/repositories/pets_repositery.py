import firebase_admin
from firebase_admin import firestore
from app.models.pets import pets


class CityRepository:
     def get_all_pets(self) -> list[pets]:
        db = firestore.client()
        docs = db.collectiom('')