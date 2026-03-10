from models import db
from models.task import Task


class TaskRepository:

    def get_all(self):
        return Task.query.all()

    def get_by_id(self, id):
        return db.session.get(Task, id)

    def save(self, task):
        db.session.add(task)
        db.session.commit()

    def delete(self, task):
        db.session.delete(task)
        db.session.commit()
