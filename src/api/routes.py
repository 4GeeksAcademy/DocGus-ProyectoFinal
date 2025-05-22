from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from api.models import db, User, MedicalFile  # Asegúrate de importar estos modelos
from api.utils import APIException
from flask_cors import CORS


api = Blueprint('api', __name__)
CORS(api)

# REGISTRO
@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ["names", "first_surname", "email", "password", "birth_day", "role"]
    for field in required_fields:
        if field not in data:
            raise APIException(f"Falta el campo requerido: {field}", status_code=400)

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

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    return jsonify({"token": access_token, "user": user.serialize()}), 200

# RUTA PROTEGIDA
@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"msg": "Acceso autorizado", "user": user.serialize()}), 200


# ENDPOINT PARA VER EXPEDIENTES MÉDICOS SEGÚN ROL
@api.route('/medical_files', methods=['GET'])
@jwt_required()
def get_medical_files():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        raise APIException("Usuario no encontrado", status_code=404)
    
    files={}

    # PACIENTE estudiante y profesional: su expediente
    own_file = MedicalFile.query.filter_by(user_id=user.id).first()
    files["own_file"]=own_file.serialize()

    # ESTUDIANTE: expedientes que él mismo creó
    if user.role == "estudiante" or user.rol=="profesional":
        created_files = MedicalFile.query.filter_by(created_by=user.id).all()
        files["created_files"]=[file.serialize() for file in created_files]

    # PROFESIONAL: los propios y los de estudiantes autorizados
    if user.role == "profesional":
        # suprvisados
        supervised_files = MedicalFile.query.filter_by(supervised_by=user.id).all()
        files["supervised_files"]=[file.serialize() for file in supervised_files]



    return jsonify(files), 200