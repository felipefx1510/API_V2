from dtos.user_dto import UserDTO
from models.user import User


class UserMapper:

    @staticmethod
    def to_dto(user):
        return UserDTO(user.id, user.name, user.email)

    @staticmethod
    def to_entity(data):
        return User(name=data["name"], email=data["email"])
