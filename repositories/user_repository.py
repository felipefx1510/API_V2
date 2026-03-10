from models import db
from models.user import User


class UserRepository:

    def get_all(self):
        return User.query.all()

    def get_by_id(self, id):
        return db.session.get(User, id)

    def save(self, user):
        db.session.add(user)
        db.session.commit()

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
