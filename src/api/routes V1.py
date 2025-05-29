from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from api.models import db, User, MedicalFile, Interview
from api.utils import APIException
from datetime import datetime

api = Blueprint('api', __name__)

# REGISTRO


@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        raise APIException(
            "El cuerpo de la solicitud debe ser JSON", status_code=400)

    required_fields = ["names", "first_surname",
                       "email", "password", "birth_day", "role"]
    for field in required_fields:
        if field not in data:
            raise APIException(
                f"Falta el campo requerido: {field}", status_code=400)

    if User.query.filter_by(email=data["email"]).first():
        raise APIException("El correo ya está registrado", status_code=400)

    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        names=data["names"],
        first_surname=data["first_surname"],
        second_surname=data.get("second_surname"),
        email=data["email"],
        password=hashed_password,
        birth_day=data["birth_day"],
        profession=data.get("profession"),
        role=data["role"],
        sex=data.get("sex"),
        phone=data.get("phone")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario registrado exitosamente"}), 201

# LOGIN
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        raise APIException("Credenciales inválidas", status_code=401)

    access_token = create_access_token(
        identity=user.id, expires_delta=timedelta(hours=1))
    return jsonify({"token": access_token, "user": user.serialize()}), 200

# RUTA PROTEGIDA


@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"msg": "Acceso autorizado", "user": user.serialize()}), 200

# Enpoint para visualizar expedientes segun el rol


@api.route('/medical_files', methods=['GET'])
@jwt_required()
def get_medical_files():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        raise APIException("Usuario no encontrado", status_code=404)

    files = {}

    if user.role == "administrador":
        all_files = MedicalFile.query.all()
        files["all_files"] = [file.serialize() for file in all_files]
        return jsonify(files), 200

    own_file = MedicalFile.query.filter_by(user_id=user.id).first()
    files["own_file"] = own_file.serialize() if own_file else None

    if user.role in ["estudiante", "profesional"]:
        created_files = MedicalFile.query.filter_by(created_by=user.id).all()
        files["created_files"] = [file.serialize() for file in created_files]

    if user.role == "profesional":
        supervised_files = MedicalFile.query.filter_by(
            supervised_by=user.id).all()
        files["supervised_files"] = [file.serialize()
                                     for file in supervised_files]

    return jsonify(files), 200










# endpoint interview
@api.route('/interview', methods=['POST'])
@jwt_required()
def create_interview():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    try:
        interview = Interview(
            medical_file_id=data.get('medical_file_id'),
            # Puede ser un dict en JSON
            questions_answers=data.get('questions_answers'),
            created_by=current_user_id,
            created_at=datetime.utcnow()
        )

        db.session.add(interview)
        db.session.commit()

        return jsonify({"msg": "Entrevista creada exitosamente", "id": interview.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al crear entrevista", "error": str(e)}), 500







@api.route('/interviews', methods=['GET'])
@jwt_required()
def get_all_interviews():
    interviews = Interview.query.all()
    result = [i.serialize() for i in interviews]
    return jsonify(result), 200



@api.route('/interview/<int:id>', methods=['GET'])
@jwt_required()
def get_interview(id):
    interview = Interview.query.get(id)
    if not interview:
        return jsonify({"msg": "Entrevista no encontrada"}), 404
    return jsonify(interview.serialize()), 200




@api.route('/interview/<int:id>/confirm', methods=['PUT'])
@jwt_required()
def confirm_interview(id):
    current_user_id = get_jwt_identity()
    interview = Interview.query.get(id)

    if not interview:
        return jsonify({"msg": "Entrevista no encontrada"}), 404

    interview.confirmed_by = current_user_id
    interview.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({"msg": "Entrevista confirmada"}), 200





@api.route('/interview/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_interview(id):
    interview = Interview.query.get(id)

    if not interview:
        return jsonify({"msg": "Entrevista no encontrada"}), 404

    db.session.delete(interview)
    db.session.commit()
    return jsonify({"msg": "Entrevista eliminada"}), 200

