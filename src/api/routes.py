# Archivo donde guardas todas las direcciones web (rutas) de tu app, y qué función debe activarse en cada una.
# Una ruta comienza en el decorador y termina en la funcion y su respuesta



# Importa las herramientas JWT para manejar autenticación
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import db, User, MedicalFile, FileStatus, PersonalData, PatientData, PathologicalBackground, FamilyBackground, GynecologicalBackground, NonPathologicalBackground, SexType
from api.utils import APIException
from datetime import datetime, timezone, timedelta
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)






# 01 EPT para registrar un nuevo usuario
@api.route('/register', methods=['POST'])                                                                           # Define la ruta /register para el endpoint, que solo acepta método POST. Es el punto de entrada para registrar nuevos usuarios.
def register():                                                                                                     # Define la función que maneja la lógica del registro de un nuevo usuario.
    data = request.get_json()                                                                                       # Obtiene el contenido JSON enviado desde el frontend.
    if not data:
        raise APIException("El cuerpo de la solicitud debe ser JSON", status_code=400)                              # Verifica que se haya enviado un JSON válido. Si no, lanza un error 400.

    required_fields = ["first_name", "first_surname", "email", "password", "birth_day", "role", "phone"]            # Lista y Verifica que todos los campos obligatorios estén presentes
    for field in required_fields:                                                                                   # Recorre (itera) la lista de campos requeridos y lanza un error si alguno falta.    
        if field not in data:
            raise APIException(f"Falta el campo requerido: {field}", status_code=400)

    if User.query.filter_by(email=data["email"]).first():                                                           # Verifica si ya existe un usuario con ese email
        raise APIException("El correo ya está registrado", status_code=400)                                         # Si sí, lanza error.

    hashed_password = generate_password_hash(data["password"])                                                      # Usa werkzeug para hashear (encriptar) la contraseña antes de guardarla.


    new_user = User(                                                                                                # Crea una instancia de User con los datos del formulario. second_name y second_surname son opcionales.
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

    db.session.add(new_user)                                                                                        #  Agrega el nuevo usuario a la sesión y confirma el registro en la base de datos.
    db.session.commit()

    # Verifica si el rol del usuario es "paciente". Soporta tanto string como Enum.                                 # Si el usuario es paciente, crear expediente y datos personales
    if new_user.role == "paciente" or (hasattr(new_user.role, "value") and new_user.role.value == "paciente"):      # Devuelve una respuesta con el nuevo usuario creado

                                                                                                                    # Si es paciente, crea un registro en la tabla PersonalData vinculado al user_id.              
        personal_data = PersonalData(
            user_id=new_user.id,
            sex=data.get("sex", None),
            address="",                                                                                             # Campo opcional, puedes pedirlo luego
                )
                                                                                                                    # Guarda los datos personales del paciente en la base de datos. 
        db.session.add(personal_data)
        db.session.commit()

                                                                                                                    # Devuelve un mensaje de éxito junto con los datos del usuario recién registrado. Código 201 = creado exitosamente. 
    return jsonify({
        "msg": "Usuario registrado exitosamente",
        "user": new_user.serialize()
    }), 201









# 02 EPT para RUTA PROTEGIDA
@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({"msg": "Acceso autorizado", "user": user.serialize()}), 200










# 03 EPT para LOGIN y generar JWT
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        raise APIException("Credenciales inválidas", status_code=401)
                                                                                                # Asegúrate de que identity sea string
    access_token = create_access_token(                                                         # Genera un token JWT con exp de 1 hora

        identity=str(user.id), expires_delta=timedelta(hours=1))

    return jsonify({"token": access_token, "user": user.serialize()}), 200











# 04 EPT para obtener datos personales de un usuario por su user_id. (usuario autenticado)
@api.route('/personal_data', methods=['GET'])
@jwt_required()                                                                                 # Requiere autenticación JWT.
def get_personal_data():
    user_id = int(get_jwt_identity())                                                                                             
    personal_data = PersonalData.query.filter_by(user_id=user_id).first()
    if not personal_data:
        return jsonify({"error": "Datos personales no encontrados"}), 404                       # Devuelve un JSON con los datos personales almacenados en la tabla PersonalData.
    return jsonify(personal_data.serialize()), 200
 



# EPT para obtener un usuario por su ID
@api.route("/user/<int:user_id>", methods=['GET'])
@jwt_required()
def get_user_for_id(user_id):
    user=User.query.get(user_id)
    if user is None : 
        return jsonify("Not Found"), 404
    else:
        return jsonify(user.serialize()),200




# 05 EPT para obtener información de todos los usuarios (solo para administradores)
@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or current_user.role.value != "administrador":
        raise APIException("Acceso no autorizado", status_code=403)

    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200









 
# 06 EPT para que un estudiante tome control de un expediente vacío
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
    file.created_by = current_user_id                                                       # Estudiante que toma el expediente para modificarlo
    db.session.commit()

    return jsonify({"msg": "Expediente asignado al estudiante"}), 200












# 07 Endpoint para obtener archivos médicos vacíos (solo para estudiantes
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








# 11 Endpoint para estudiantes: obtiene la lista de pacientes que aún no tienen expediente médico asignado.
@api.route('/student/patients', methods=['GET'])
@jwt_required()
def get_student_patients():
    current_user_id = get_jwt_identity()                                                        # Requiere autenticación y valida que el usuario sea un estudiante.
    current_user = User.query.get(current_user_id)

    if not current_user or current_user.role.value != "estudiante":
        raise APIException("Acceso no autorizado", status_code=403)

    users = User.query.filter_by(role="paciente", medical_file=None).all()
    return jsonify([user.serialize() for user in users]), 200










# 08 Endpoint para crear un expediente médico y asigna el usuario estudiante (actual) como creador,
# el endpoint recibe el id del paciente
# recibe por body la informacion del paciente que generara un registro en cada una de las tablas vinculadas
@api.route('/medical_file', methods=['POST'])
@jwt_required()
def create_medical_file():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        raise APIException("Usuario no encontrado", status_code=404)
    
    if user.role != "estudiante":
        raise APIException("Solo los estudiantes pueden crear expedientes médicos", status_code=403)

    data = request.get_json()
    if not data or "patient_id" not in data:
        raise APIException("El ID del paciente es requerido", status_code=400)

    patient_id = data["patient_id"]
    patient = User.query.get(patient_id)
    if not patient or patient.role != "paciente":
        raise APIException("Paciente no encontrado o no válido", status_code=404)

    # Verificar si el paciente ya tiene un expediente médico
    existing_file = MedicalFile.query.filter_by(user_id=patient.id).first()
    if existing_file:
        raise APIException("El paciente ya tiene un expediente médico", status_code=400)

    new_file = MedicalFile(
        user_id=patient.id,
        created_by=current_user_id,
        status=FileStatus.EMPTY
    )
    
    db.session.add(new_file)
    db.session.commit()

    return jsonify({"msg": "Expediente médico creado exitosamente", "file": new_file.serialize()}), 201







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










# 09 Cambiar estado de un expediente médico
@api.route('/medical_file/<int:file_id>/status', methods=['PUT'])
@jwt_required()
def change_medical_file_status(file_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        raise APIException("Usuario no encontrado", status_code=404)

    file = MedicalFile.query.get(file_id)
    if not file:
        raise APIException("Expediente médico no encontrado", status_code=404)

    new_status = request.json.get("status")
    if not new_status:
        raise APIException("El estado es requerido", status_code=400)
    if user.role == "paciente":
        # Solo los profesionales pueden cambiar el estado a REVISADO
        if new_status != ["REVIEW", "APPROVED"]:
            raise APIException("Solo los pacientes pueden cambiar el estado a REVISADO", status_code=403)
        file.status = FileStatus.REVIEW
    elif user.role == "profesional":
        # Los profesionales pueden cambiar el estado a REVISADO o FINALIZADO
        new_status = request.json.get("status")
        if new_status not in ["REVIEW"]:
            raise APIException("Estado inválido para profesionales", status_code=400)
        file.status = FileStatus[new_status]
        file.supervised_by = current_user_id
        file.supervised_at = datetime.now(timezone.utc)
        if new_status == "APPROVED":
            file.approved_by = current_user_id
            file.approved_at = datetime.now(timezone.utc)
    else:
        raise APIException("Acceso no autorizado para cambiar el estado del expediente", status_code=403)
    db.session.commit()
    return jsonify({"msg": "Estado del expediente médico actualizado exitosamente"}), 200









# 10 Enpoint para visualizar expedientes segun el rol
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




















# 12 Endpoint para profesionales: obtiene la lista de pacientes que tienen un expediente médico en status REVIEW.
@api.route('/professional/patients', methods=['GET'])
@jwt_required()
def get_professional_patients():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or current_user.role.value != "profesional":
        raise APIException("Acceso no autorizado", status_code=403)

    users = (
    User.query
    .join(MedicalFile, MedicalFile.user_id == User.id)
    .filter(
        User.role == "paciente",
        MedicalFile.status == "REVIEW"
    )
    .all()
)
    return jsonify([user.serialize() for user in users]), 200










# 13 Endpoint para eliminar un usuario (solo administradores)
@api.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200
   











@api.route('/personal-data', methods=['POST'])
def create_personal_data():
    data = request.get_json()

    user_id = data.get("user_id")
    sex = data.get("sex")
    address = data.get("address")

    if not user_id or not sex or not address:
        return jsonify({"error": "Faltan campos obligatorios: user_id, sex o address"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Verificar si ya existe personal_data
    if user.personal_data:
        return jsonify({"error": "Ya existen datos personales para este usuario"}), 400

    try:
        personal_data = PersonalData(
            user_id=user_id,
            sex=SexType(sex),  # Convierte string a Enum
            address=address
        )

        db.session.add(personal_data)
        db.session.commit()

        return jsonify(personal_data.serialize()), 201

    except ValueError as e:
        return jsonify({"error": f"Valor inválido para 'sex': {sex}. Opciones válidas: {[s.value for s in SexType]}"}), 400












# crear un endpoint para traer los datos del user similar a personal PatientData instanciar clase usuario
