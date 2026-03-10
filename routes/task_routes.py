from flask import Blueprint, jsonify, request
from mappers.task_mapper import TaskMapper
from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository

task_bp = Blueprint("tasks", __name__)
task_repo = TaskRepository()
user_repo = UserRepository()


@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = task_repo.get_all()
    return jsonify([TaskMapper.to_dto(t).to_dict() for t in tasks])


@task_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data or "user_id" not in data:
        return jsonify({"error": "Campos 'title' e 'user_id' são obrigatórios"}), 400

    user = user_repo.get_by_id(data["user_id"])
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    task = TaskMapper.to_entity(data)
    task_repo.save(task)
    return jsonify(TaskMapper.to_dto(task).to_dict()), 201


@task_bp.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = task_repo.get_by_id(id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    return jsonify(TaskMapper.to_dto(task).to_dict())


@task_bp.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = task_repo.get_by_id(id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição inválido"}), 400

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)

    task_repo.save(task)
    return jsonify(TaskMapper.to_dto(task).to_dict())


@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = task_repo.get_by_id(id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    task_repo.delete(task)
    return "", 204
