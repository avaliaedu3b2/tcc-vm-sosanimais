import firebase_admin
from firebase_admin import firestore
from app.models.pets import pets

class petsepository:
    def get_all_pets(self) -> list[pets]:
        db = firestore.client()
        docs = db.collection('pets').stream()
        pets = []
        for doc in docs:
            data = doc.to_dict()
            pets.append(pets(id=doc.id,
                                name=data.get('name'),
                                state=data.get('state'),
                                initials=data.get('initials'),
                                country=data.get('country'), 
                                country_initials=data.get('country_initials'),
                                timezone=data.get('timezone'),
                                health_cust=data.get('health_cust'),
                                airport=data.get('airport')))
        return pets

    def get_pets(self, pets_id: str) -> pets:
        db = firestore.client()
        doc = db.collection('pets').document(pets_id).get()
        if doc.exists:
            data = doc.to_dict()
            return pets(id=doc.id, 
                        name=data.get('name'),
                        state=data.get('state'), 
                        initials=data.get('initials'),
                        country=data.get('country'), 
                        country_initials=data.get('country_initials'),
                        timezone=data.get('timezone'),
                        health_cust=data.get('health_cust'),
                        airport=data.get('airport'))
        return None

    def add_pets(self, pets: pets) -> str:
        db = firestore.client()
        doc = db.collection('pets').add({
            'name': pets.name,
            'state': pets.state,
            'initials': pets.initials,
            'country': pets.country, 
            'country_initials': pets.country_initials,
            'timezone': pets.timezone,
            'health_cust': pets.health_cust,
            'airport': pets.airport
        })
        return doc[1].id

    def update_pets(self, pets_id: str, pets: pets) -> bool:
        db = firestore.client()
        db.collection('pets').document(pets_id).update({
            'name': pets.name,
            'state': pets.state,
            'initials': pets.initials,
            'country': pets.country, 
            'country_initials': pets.country_initials,
            'timezone': pets.timezone,
            'health_cust': pets.health_cust,
            'airport': pets.airport
        })
        return True