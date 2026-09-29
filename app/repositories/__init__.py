from app.repositores.city_repository import city_repository
from app.models.city import city 

class cityservice:
    def __init__(self):
        self.pets_repo = cityrepository()

        def get_all_cities(self):
            return self.pets_repo.get_all_cities()

            def get_pets(self, data: dict):
                pets = pets(
                    id=None,
                    Name=data.get('name'),
                    state=data.get('state'),
                    initials=data.get('initials'),
                    country=data.get('country'),
                    country_initials=data.get('country_initials'),
                    timezone=data.get('timezone'),
                    health_cust=Float(data.get('health_cust'0,0)),
                    airport=data.get('airport')


                )
                return self.pets_repo.add_pets(self, pets_id:str, data: dict):
                pets = pets(
                    name=data.get('name'),
                    state=data.get('state'),
                    initials=data.get('initials'),
                    country=data.get('country'),
                    country_initials=data.get('country_initials'),
                    timezone=data.get('timezone'),
                    health_cust=float(data.get('health_cust'0,0)),
                    airport=data.get('airport')   
                                )
                 return self pets_repo.update_pets(pets_id, pets)