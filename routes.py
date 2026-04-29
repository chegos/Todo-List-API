from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Todo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint("main", __name__)
bcrypt = Bcrypt()

@main.route("/register", methods=["POST"])
def register():
    data = request.json

    # Verifica se já existe usuário com esse email
    existing_user = User.query.filter_by(email=data["email"]).first()

    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))

    return jsonify({"token": token})


@main.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):
        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401

@main.route("/todos", methods=["POST"])
@jwt_required()
def create_todo():
    user_id = int(get_jwt_identity())
    data = request.json

    todo = Todo(
        title=data["title"],
        description=data["description"],
        user_id=user_id
    )

    db.session.add(todo)
    db.session.commit()

    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "description": todo.description
    })

@main.route("/todos", methods=["GET"])
@jwt_required()
def get_todos():
    user_id = int(get_jwt_identity())

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    todos = Todo.query.filter_by(user_id=user_id).paginate(page=page, per_page=limit)

    data = []

    for todo in todos.items:
        data.append({
            "id": todo.id,
            "title": todo.title,
            "description": todo.description
        })

    return jsonify({
        "data": data,
        "page": page,
        "limit": limit,
        "total": todos.total
    })

@main.route("/todos/<int:id>", methods=["PUT"])
@jwt_required()
def update_todo(id):
    user_id = int(get_jwt_identity())

    todo = Todo.query.get_or_404(id)

    if todo.user_id != user_id:
        return jsonify({"message": "Forbidden"}), 403

    data = request.json

    todo.title = data["title"]
    todo.description = data["description"]

    db.session.commit()

    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "description": todo.description
    })

@main.route("/todos/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_todo(id):
    user_id = int(get_jwt_identity())

    todo = Todo.query.get_or_404(id)

    if todo.user_id != user_id:
        return jsonify({"message": "Forbidden"}), 403

    db.session.delete(todo)
    db.session.commit()

    return "", 204
