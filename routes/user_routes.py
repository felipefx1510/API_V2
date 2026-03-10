from flask import Blueprint, jsonify, request
from mappers.user_mapper import UserMapper
from repositories.user_repository import UserRepository

user_bp = Blueprint("users", __name__)
user_repo = UserRepository()


@user_bp.route("/users", methods=["GET"])
def get_users():
    users = user_repo.get_all()
    return jsonify([UserMapper.to_dto(u).to_dict() for u in users])


@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Campos 'name' e 'email' são obrigatórios"}), 400

    user = UserMapper.to_entity(data)
    user_repo.save(user)
    return jsonify(UserMapper.to_dto(user).to_dict()), 201


@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = user_repo.get_by_id(id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(UserMapper.to_dto(user).to_dict())
