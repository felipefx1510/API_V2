from dtos.task_dto import TaskDTO
from models.task import Task


class TaskMapper:

    @staticmethod
    def to_dto(task):
        return TaskDTO(task.id, task.title, task.description, task.completed)

    @staticmethod
    def to_entity(data):
        return Task(
            title=data["title"],
            description=data.get("description", ""),
            completed=False,
            user_id=data["user_id"],
        )
