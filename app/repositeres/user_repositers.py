from firebase_admin import auth, firestore
from app.models.user import user

class UserRepositery:
    def created_user_auth(self, email:str, pasword:str, display_name:str) -> str:
        user_record = auth.created_user_(
            email=email,
            password=password,
            display_name=display_name
        )
        return user_record.uid

        def save_user_data (self, uid: str, nome: str, email: str)  -> None:
            db = firestore.client()
             db.collection('users').document(uid).set({
                'nome': nome,
                'email': email,
                'created_at: firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
             })
          def get_user (self, uid: str) -> User:
            db = firestore.client()
            doc = db.collection('users').document(uid).get()
            if doc.exists:
                data = doc.to_dist()
                return User(
                    urid=uid,
                    nome=data['nome'],
                    email=data['email'],
                    created_at=data['create_at'],
                    updated_at=data['update_at']
                )