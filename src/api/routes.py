# Importa las herramientas JWT para manejar autenticación
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import db, User, MedicalFile, FileStatus, PersonalData, PatientData, PathologicalBackground, FamilyBackground, GynecologicalBackground, NonPathologicalBackground, SexType
from api.utils import APIException
from datetime import datetime, timezone, timedelta
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        raise APIException("El cuerpo de la solicitud debe ser JSON", status_code=400)

    required_fields = ["first_name", "first_surname", "email", "password", "birth_day", "role", "phone"]
    for field in required_fields:
        if field not in data:
            raise APIException(f"Falta el campo requerido: {field}", status_code=400)

    if User.query.filter_by(email=data["email"]).first():
        raise APIException("El correo ya está registrado", status_code=400)

    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        first_name=data.get("first_name", None),
        second_name=data.get("second_name", None),
        first_surname=data.get("first_surname", None),
        second_surname=data.get("second_surname"),
        email=data.get("email", None),
        password=hashed_password,
        birth_day=data.get("birth_day", None),
        role=data.get("role", None),
        phone=data.get("phone", None)
    )

    db.session.add(new_user)
    db.session.commit()

    # Si el usuario es paciente, crear expediente y datos personales
    if new_user.role == "paciente" or (hasattr(new_user.role, "value") and new_user.role.value == "paciente"):
        # 2. Crear datos personales asociados
        personal_data = PersonalData(
            user_id=new_user.id,
            sex=data.get("sex", None),
            address="",  # Campo opcional, puedes pedirlo luego
                ) 
        db.session.add(personal_data)
        db.session.commit()


    return jsonify({
        "msg": "Usuario registrado exitosamente",
        "user": new_user.serialize()
    }), 201




# Endpoint para obtener los datos personales de un usuario por su user_id.
# Requiere autenticación JWT.
# Devuelve un JSON con los datos personales almacenados en la tabla PersonalData.
@api.route('/personal_data', methods=['GET'])
@jwt_required()
def get_personal_data():
    user_id = int(get_jwt_identity())
    """
    Devuelve los datos personales asociados a un usuario.
    """
    personal_data = PersonalData.query.filter_by(user_id=user_id).first()
    if not personal_data:
        return jsonify({"error": "Datos personales no encontrados"}), 404
    return jsonify(personal_data.serialize()), 200
 

#Este endpoint es solo para que un estudiante tome un expediente vacío
@api.route('/student/files/<int:file_id>/take', methods=['POST'])
@jwt_required()
def take_file(file_id):
    current_user_id = get_jwt_identity()

    file = MedicalFile.query.get(file_id)

    if not file:
        return jsonify({"error": "Expediente no encontrado"}), 404

    if file.status != FileStatus.EMPTY:
        return jsonify({"error": "Expediente no disponible"}), 400

    file.status = FileStatus.PROGRESS
    file.created_by = current_user_id  # El estudiante que lo toma
    db.session.commit()

    return jsonify({"msg": "Expediente asignado al estudiante"}), 200

# LOGIN
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        raise APIException("Credenciales inválidas", status_code=401)

    # ✅ Asegúrate de que identity sea string
    access_token = create_access_token(
        identity=str(user.id), expires_delta=timedelta(hours=1))

    return jsonify({"token": access_token, "user": user.serialize()}), 200


# Endpoint para obtener información de todos los usuarios (solo para administradores)
@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or current_user.role.value != "administrador":
        raise APIException("Acceso no autorizado", status_code=403)

    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# Endpoint para estudiantes: obtiene la lista de pacientes que aún no tienen expediente médico asignado.
# Se usa en el flujo de selección de pacientes disponibles antes de iniciar un nuevo expediente.
# Requiere autenticación y valida que el usuario sea un estudiante.
@api.route('/student/patients', methods=['GET'])
@jwt_required()
def get_student_patients():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or current_user.role.value != "estudiante":
        raise APIException("Acceso no autorizado", status_code=403)

    users = User.query.filter_by(role="paciente", medical_file=None).all()
    return jsonify([user.serialize() for user in users]), 200


# RUTA PROTEGIDA
@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"msg": "Acceso autorizado", "user": user.serialize()}), 200

# Endpoint para obtener archivos médicos vacíos (solo para estudiantes

@api.route('/student/files', methods=['GET'])
def get_files_by_status():
    status = request.args.get('status', 'EMPTY')
    # Convertir el string a Enum para evitar errores de tipo
    try:
        status_enum = FileStatus[status]
    except KeyError:
        return jsonify({"error": "Status inválido"}), 400
    files = MedicalFile.query.filter_by(status=status_enum).all()
    return jsonify([file.serialize() for file in files]), 200

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

# Endpoint para crear un expediente médico
# Crea un expediente medico y asigna el usuario actual como creador,
# y el usuario que lo supervisa si es un profesional
# el endpoint recibe el id del paciente
# recibe por body la informacion del paciente que generara un registro en cada una de las tablas vinculadas: PersonalData, PathologicalBackground, FamilyBackground, GynecologicalBackground (en el caso de los pacientes femenino), NonPathologicalBackground)


# Endpoint para eliminar un usuario (solo administradores)
@api.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200
   

@api.route('/backgrounds', methods=['POST'])
def save_backgrounds():
    data = request.get_json()

    medical_file_id = data.get("medical_file_id")
    if not medical_file_id:
        return jsonify({"error": "Medical file ID is required"}), 400

    medical_file = MedicalFile.query.get(medical_file_id)
    if not medical_file:
        return jsonify({"error": "Medical file not found"}), 404

    # 1. Pathological
    pathological_data = data.get("patological_background", {})
    pathological = PathologicalBackground(user_id=medical_file.user_id, medical_file_id=medical_file_id, **pathological_data)
    db.session.add(pathological)

    # 2. Family
    family_data = data.get("family_background", {})
    family = FamilyBackground(user_id=medical_file.user_id, medical_file_id=medical_file_id, **family_data)
    db.session.add(family)

    # 3. Non-Pathological
    nonpath_data = data.get("non_pathological_background", {})
    nonpath = NonPathologicalBackground(user_id=medical_file.user_id, medical_file_id=medical_file_id, **nonpath_data)
    db.session.add(nonpath)

    # 4. Gynecological
    gyneco_data = data.get("gynecological_background", {})
    gyneco = GynecologicalBackground(user_id=medical_file.user_id, medical_file_id=medical_file_id, **gyneco_data)
    db.session.add(gyneco)

    db.session.commit()

    return jsonify({"msg": "Antecedentes guardados exitosamente"}), 201
