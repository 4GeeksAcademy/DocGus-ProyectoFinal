from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import db, User, MedicalFile, PersonalData, PathologicalBackground, FamilyBackground, GynecologicalBackground, NonPathologicalBackground, SexType
from api.utils import APIException
from datetime import datetime, timezone, timedelta
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

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

# Endpoint para crear un expediente médico
# Crea un expediente medico y asigna el usuario actual como creador, 
# y el usuario que lo supervisa si es un profesional
# el endpoint recibe el id del paciente
# recibe por body la informacion del paciente que generara un registro en cada una de las tablas vinculadas: PersonalData, PathologicalBackground, FamilyBackground, GynecologicalBackground (en el caso de los pacientes femenino), NonPathologicalBackground)
@api.route("/medical-file", methods=["POST"])
@jwt_required()
def create_medical_file():
    """
    body example:
    {
        "user_id": 1,
        "created_by": 2,
        "personal_data": {
            "full_name": "Juan Perez",
            "paternal_surname": "Perez",
            "maternal_surname": "Gomez","sex": "masculino",
            "birth_date": "1990-01-01",
            "address": "Calle Falsa 123",
            "phone": "123456789"
        },
        "pathological": {  
            "personal_diseases": "Ninguna",
            "medications": "Ninguno",
            "hospitalizations": "Ninguna",
            "surgeries": "Ninguna",
            "traumatisms": "Ninguno",
            "transfusions": "Ninguna",
            "allergies": "Ninguna",
            "others": "Ninguno"
        },
        "family": {
            "hypertension": false,
            "diabetes": false,
            "cancer": false,
            "heart_disease": false,
            "kidney_disease": false,
            "liver_disease": false,
            "mental_illness": false,
            "congenital_malformations": false,
            "others": "Ninguno"
        },
        "non_pathological": {
            "education_level": "Secundaria",
            "economic_activity": "Estudiante",
            "marital_status": "Soltero",
            "dependents": 0,
            "occupation": "Estudiante",
            "recent_travels": "Ninguno",
            "social_activities": "Ninguna",
            "exercise": "Ninguno",
            "diet_supplements": "Ninguno",
            "hygiene": "Buena",
            "tattoos": false,
            "piercings": false,
            "hobbies": "Leer",
            "tobacco_use": false,
            "alcohol_use": false,
            "recreational_drugs": false,
            "addictions": "Ninguna",
            "otherS": "Ninguno"
        },
        "gynecological": {
            "menarche_age": 12,
            "pregnancies": 0,
            "births": 0,
            "c_sections": 0,
            "abortions": 0,
            "contraceptive_method": "Ninguno",
            "others": "Ninguno"
        }           
    }
    """
    data = request.get_json()

    # 1. Crear el expediente médico
    medical_file = MedicalFile(
        user_id=data["user_id"],
        supervised_by=data["supervised_by"],
        supervised_at=datetime.now(timezone.utc),
        created_by=data["created_by"],
        created_at=datetime.now(timezone.utc),
        confirmed_at=datetime.now(timezone.utc),
        status="revision"
    )
    db.session.add(medical_file)
    db.session.flush()  # Para obtener el ID antes de commit

    # 2. Crear los datos personales
    personal_data = PersonalData(
        user_id=data["user_id"],
        medical_file_id=medical_file.id,
        full_name=data["personal_data"]["full_name"],
        paternal_surname=data["personal_data"]["paternal_surname"],
        maternal_surname=data["personal_data"].get("maternal_surname"),
        sex=data["personal_data"]["sex"],
        birth_date=data["personal_data"]["birth_date"],
        address=data["personal_data"]["address"],
        phone=data["personal_data"]["phone"]
    )
    db.session.add(personal_data)

    # 3. Crear antecedentes patológicos
    pathological = PathologicalBackground(
        user_id=data["user_id"],
        medical_file_id=medical_file.id,
        personal_diseases=data["pathological"]["personal_diseases"],
        medications=data["pathological"]["medications"],
        hospitalizations=data["pathological"]["hospitalizations"],
        surgeries=data["pathological"]["surgeries"],
        traumatisms=data["pathological"]["traumatisms"],
        transfusions=data["pathological"]["transfusions"],
        allergies=data["pathological"]["allergies"],
        others=data["pathological"]["others"]
    )
    db.session.add(pathological)

    # 4. Crear antecedentes familiares
    family = FamilyBackground(
        user_id=data["user_id"],
        medical_file_id=medical_file.id,
        hypertension=data["family"]["hypertension"],
        diabetes=data["family"]["diabetes"],
        cancer=data["family"]["cancer"],
        heart_disease=data["family"]["heart_disease"],
        kidney_disease=data["family"]["kidney_disease"],
        liver_disease=data["family"]["liver_disease"],
        mental_illness=data["family"]["mental_illness"],
        congenital_malformations=data["family"]["congenital_malformations"],
        others=data["family"]["others"]
    )
    db.session.add(family)

    # 5. Crear antecedentes no patológicos
    non_pathological = NonPathologicalBackground(
        user_id=data["user_id"],
        medical_file_id=medical_file.id,
        education_level=data["non_pathological"]["education_level"],
        economic_activity=data["non_pathological"]["economic_activity"],
        marital_status=data["non_pathological"]["marital_status"],
        dependents=data["non_pathological"]["dependents"],
        occupation=data["non_pathological"]["occupation"],
        recent_travels=data["non_pathological"]["recent_travels"],
        social_activities=data["non_pathological"]["social_activities"],
        exercise=data["non_pathological"]["exercise"],
        diet_supplements=data["non_pathological"]["diet_supplements"],
        hygiene=data["non_pathological"]["hygiene"],
        tattoos=data["non_pathological"]["tattoos"],
        piercings=data["non_pathological"]["piercings"],
        hobbies=data["non_pathological"]["hobbies"],
        tobacco_use=data["non_pathological"]["tobacco_use"],
        alcohol_use=data["non_pathological"]["alcohol_use"],
        recreational_drugs=data["non_pathological"]["recreational_drugs"],
        addictions=data["non_pathological"]["addictions"],
        otherS=data["non_pathological"]["otherS"]
    )
    db.session.add(non_pathological)

    # 6. Si es femenino, crear antecedentes ginecológicos
    if data["personal_data"]["sex"] == SexType.femenino.value:
        gyneco = GynecologicalBackground(
            user_id=data["user_id"],
            medical_file_id=medical_file.id,
            menarche_age=data["gynecological"]["menarche_age"],
            pregnancies=data["gynecological"]["pregnancies"],
            births=data["gynecological"]["births"],
            c_sections=data["gynecological"]["c_sections"],
            abortions=data["gynecological"]["abortions"],
            contraceptive_method=data["gynecological"]["contraceptive_method"],
            others=data["gynecological"]["others"]
        )
        db.session.add(gyneco)

    db.session.commit()
    return jsonify({"msg": "Expediente médico creado", "medical_file_id": medical_file.id}), 201


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

