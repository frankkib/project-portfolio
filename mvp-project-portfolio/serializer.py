class HouseSerializer:
    @staticmethod
    def serialize(house):
        return {
            'id': house.id,
            'location': house.location,
            'price': house.price,
            'description': house.description,
            'created_at': house.created_at,
            'is_available': house.is_available,
            'photo_filename': house.photo_filename
        }
    @staticmethod
    def serialize_many(houses):
        return [HouseSerializer.serialize(house) for house in houses]
class UserSerializer:
        @staticmethod
        def serialize(user):
            return {
                'id': user.id,
                'username': user.name,
                'email': user.email,
                'password': user.password
            }
        @staticmethod
        def serialize_many(users):
            return [UserSerializer.serialize(user) for user in users]