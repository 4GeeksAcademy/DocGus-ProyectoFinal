# -------------------- INICIALIZACIÓN DE LA BASE DE DATOS --------------------


# Se importan todos los módulos necesarios y se crea la instancia principal de la base de datos.
# Importa la extensión de SQLAlchemy para usarla con Flask
from flask_sqlalchemy import SQLAlchemy
# Importa tipos y funciones necesarios para definir columnas y relaciones en la base de datos
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Enum, Text, func
# Importa utilidades para mapear columnas y relaciones en los modelos
from sqlalchemy.orm import Mapped, mapped_column, relationship
# Importa clase para trabajar con fechas y horas
from datetime import datetime
# Importa clase para trabajar con fechas
from datetime import date
# Importa módulo para crear enumeraciones (valores limitados)
import enum

# Crea una instancia de SQLAlchemy para usarla en la app Flask
db = SQLAlchemy()


# # -------------------- ENUMS PERSONALIZADOS --------------------
# # RESUMEN: Representa a los usuarios del sistema. Puede ser un administrador, profesional o paciente. (Estudiante????)
# # RESUMEN: Se crean dos enumeraciones para asegurar que ciertos campos solo tengan valores válidos: rol de usuario y sexo.
class UserRole(str, enum.Enum):             # Define roles posibles de usuario
    administrador = "administrador"         # Usuario administrador
    profesional = "profesional"             # Usuario profesional de la salud
    paciente = "paciente"                   # Usuario paciente
    estudiante = "estudiante"               # Usuario estudiante


# Define los estados posibles de un expediente médico
class FileStatus(str, enum.Enum):
    # El expediente está en progreso (llenándose)
    PROGRESS = "PROGRESS"
    # El expediente está en revisión por el profesional
    REVIEW = "REVIEW"
    # El expediente fue aprobado por el profesional
    APPROVED = "APPROVED"
    # El expediente fue confirmado por el paciente
    CONFIRMED = "CONFIRMED"


# Define los estados posibles de validación del usuario
class UserStatus(str, enum.Enum):
    # Usuario registrado, pendiente de aprobación
    preaprobado = "preaprobado"
    aprobado = "aprobado"                   # Usuario aprobado y activo
    inactivo = "inactivo"                   # Usuario inactivo o suspendido


class SexType(str, enum.Enum):              # Define los tipos posibles de sexo biologico y variedades anatomicas las cuestiones de identidad de genero son propias del area psicologica de este expediente
    femenino = "femenino"                   # Sexo femenino
    masculino = "masculino"                 # Sexo masculino
    otro = "otro"                           # Hermafroditismo u otros


# Define los niveles académicos posibles para profesionales
class AcademicGrade(str, enum.Enum):
    # Nivel técnico (carrera técnica o equivalente)
    tecnico = "tecnico"
    # Profesional titulado (licenciatura o superior)
    profesionista = "profesionista"


# -------------------- MODELO: User --------------------
# Definicion y Descripcion
# RESUMEN: Modelo que representa a los usuarios del sistema. Puede contener la info de Id email y Rol


class User(db.Model):  # Modelo principal para todos los tipos de usuarios del sistema
    __tablename__ = "users"  # Nombre de la tabla en la base de datos

    # Identificador único del usuario (clave primaria)
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(
        String(100), nullable=False)            # Primer nombre del usuario
    # Segundo nombre del usuario (opcional)
    second_name: Mapped[str] = mapped_column(String(100), nullable=True)
    first_surname: Mapped[str] = mapped_column(
        String(100), nullable=False)         # Primer apellido del usuario
    # Segundo apellido del usuario (opcional)
    second_surname: Mapped[str] = mapped_column(String(100), nullable=True)
    # Fecha de nacimiento del usuario
    birth_day: Mapped[date] = mapped_column(nullable=False)
    # Número de teléfono (opcional)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False)     # Correo electrónico único
    # Contraseña cifrada del usuario
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False)          # Rol del usuario (enum)
    status: Mapped[UserStatus] = mapped_column(                                     # Estado del usuario (enum)
        # Valor por defecto: preaprobado
        Enum(UserStatus), nullable=False, default=UserStatus.preaprobado
    )

    # Relación uno a uno con los datos personales (PersonalData)
    personal_data: Mapped["PersonalData"] = relationship(
        "PersonalData", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    # Relación uno a uno con los datos de estudiante (StudentData)
    student_data: Mapped["StudentData"] = relationship(
        "StudentData", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    # Relación uno a uno con los datos profesionales (ProfessionalData)
    professional_data: Mapped["ProfessionalData"] = relationship(
        "ProfessionalData", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    # Relación uno a uno con el expediente médico del usuario (si es paciente)
    medical_file: Mapped["MedicalFile"] = relationship(
        back_populates="user", foreign_keys="[MedicalFile.user_id]", uselist=False, cascade="all, delete-orphan"
    )

    # Relación uno a muchos: expedientes médicos creados por este usuario (si es estudiante)
    student_medical_files: Mapped[list["MedicalFile"]] = relationship(
        back_populates="creator", foreign_keys="[MedicalFile.created_by]", cascade="all, delete-orphan"
    )

    # Relación uno a muchos: expedientes médicos supervisados por este usuario (si es profesional)
    supervised_medical_files: Mapped[list["MedicalFile"]] = relationship(
        back_populates="supervisor", foreign_keys="[MedicalFile.supervised_by]", cascade="all, delete-orphan"
    )

    def serialize(self):  # Método para representar el usuario como un diccionario (para APIs o JSON)
        return {
            # ID del usuario
            "id": self.id,
            # Correo electrónico
            "email": self.email,
            # Rol del usuario (como string)
            "role": self.role.value,
            # Estado del usuario (como string)
            "status": self.status.value,
            # Primer nombre
            "first_name": self.first_name,
            # Segundo nombre
            "second_name": self.second_name,
            # Primer apellido
            "first_surname": self.first_surname,
            # Segundo apellido
            "second_surname": self.second_surname,
            # Fecha de nacimiento en formato ISO
            "birth_day": self.birth_day.isoformat(),
            # Teléfono
            "phone": self.phone,
            # Expediente médico serializado
            "medical_file": self.medical_file.serialize_medical_data() if self.medical_file else None
        }

    # Representación legible del objeto para debugging
    def __repr__(self):
        return f"<User {self.id} - {self.email} .>"


# -------------------- MODELO: MedicalFile --------------------
# RESUMEN: Representa un expediente médico que puede ser creado por un profesional para un paciente.
# Definición de la clase MedicalFile que hereda de db.Model (SQLAlchemy)
class MedicalFile(db.Model):
    __tablename__ = "medical_files"

    # Clave primaria del expediente
    id: Mapped[int] = mapped_column(primary_key=True)

    # ID del paciente relacionado (puede ser nulo al inicio)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    # ID del estudiante que crea el expediente
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # ID del profesional que supervisa la revisión
    supervised_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True)
    supervised_at: Mapped[datetime] = mapped_column(DateTime)

    # Nuevo: ID del profesional que aprueba
    approved_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Fecha en la que el paciente confirma su expediente
    confirmed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Estado del expediente clínico
    status: Mapped["FileStatus"] = mapped_column(
        Enum(FileStatus), nullable=True, default=None
    )

    # Relaciones con el modelo User
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    supervisor: Mapped["User"] = relationship(
        "User", foreign_keys=[supervised_by])
    approver: Mapped["User"] = relationship("User", foreign_keys=[approved_by])

    # Relaciones 1:1 con los datos clínicos
    patient_data: Mapped["PatientData"] = relationship(
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan"
    )
    pathological_background: Mapped["PathologicalBackground"] = relationship(
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan"
    )
    family_background: Mapped["FamilyBackground"] = relationship(
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan"
    )
    non_pathological_background: Mapped["NonPathologicalBackground"] = relationship(
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan"
    )
    gynecological_background: Mapped["GynecologicalBackground"] = relationship(
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "supervised_by": self.supervised_by,
            "supervised_at": self.supervised_at.isoformat() if self.supervised_at else None,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "status": self.status.value
        }

        # Representa el expediente como un diccionario para serialización
    def serialize_medical_data(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "supervised_by": self.supervised_by,
            "supervised_at": self.supervised_at.isoformat() if self.supervised_at else None,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "status": self.status.value,
            "patient_data": self.patient_data.serialize() if self.patient_data else None,
            "pathological_background": self.pathological_background.serialize() if self.pathological_background else None,
            "family_background": self.family_background.serialize() if self.family_background else None,
            "non_pathological_background": self.non_pathological_background.serialize() if self.non_pathological_background else None,
            "gynecological_background": self.gynecological_background.serialize() if self.gynecological_background else None
        }

        # Método para representar el expediente como una cadena
        # Retorna una cadena con el ID del expediente y el ID del paciente asociado
        # Agregar quien autoriza que se quede en base de datos la entrevista o expediente


# -------------------- MODELO: PersonalData --------------------
# RESUMEN: Contiene los datos personales de un usuario. Está relacionado con su expediente y su cuenta de usuario.
class PersonalData(db.Model):
    __tablename__ = "personal_data"
    id: Mapped[int] = mapped_column(
        primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(ForeignKey(
        # Relación 1:1 con usuario
        "users.id"), nullable=False, unique=True)
    sex: Mapped[SexType] = mapped_column(
        Enum(SexType))                         # Sexo (enum)
    address: Mapped[str] = mapped_column(
        Text)                                  # Dirección

    # Relación con el modelo User
    user: Mapped["User"] = relationship(
        "User", back_populates="personal_data", uselist=False)

    def serialize(self):
        return {
            # Incluye la serialización del usuario
            **self.user.serialize(),
            "id": self.id,
            "sex": self.sex.value if hasattr(self.sex, "value") else self.sex,
            "address": self.address,
            "user": {
                "first_name": self.user.first_name,
                "second_name": self.user.second_name,
                "first_surname": self.first_surname,
                "second_surname": self.user.second_surname,
                "birth_day": self.user.birth_day.isoformat(),
                "phone": self.user.phone,
                "email": self.user.email,
                "role": self.user.role.value
            }
        }

class PatientData(db.Model):
    __tablename__ = "patient_data"
    id: Mapped[int] = mapped_column(
        primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(ForeignKey(
        # Relación 1:1 con usuario
        "users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        # Expediente asociado
        "medical_files.id"), nullable=True)


    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="patient_data")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "medical_file_id": self.medical_file_id
        }

class StudentData(db.Model):
    __tablename__ = "student_data"
    id: Mapped[int] = mapped_column(
        primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(ForeignKey(
        # Relación 1:1 con usuario
        "users.id"), nullable=False, unique=True)
    academic_grade: Mapped[AcademicGrade] = mapped_column(
        Enum(AcademicGrade), nullable=False)


    # Relación con el modelo User
    user: Mapped["User"] = relationship(
        "User", back_populates="student_data", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "academic_grade": self.academic_grade.value
        }

class ProfessionalData(db.Model):
    __tablename__ = "professional_data"
    id: Mapped[int] = mapped_column(primary_key=True)  # ID único
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id"), nullable=False, unique=True)  # Relación 1:1 con usuario
    profession: Mapped[str] = mapped_column(String(70))

    # Relación con el modelo User
    user: Mapped["User"] = relationship(
        "User", back_populates="professional_data", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "profession": self.profession
        }










# -------------------- MODELO: PathologicalBackground --------------------
# RESUMEN: Almacena antecedentes patológicos personales del paciente, como enfermedades, cirugías y alergias.
class PathologicalBackground(db.Model):
    __tablename__ = "pathological_background"
    id: Mapped[int] = mapped_column(
        primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        # Relación con expediente
        "medical_files.id"), nullable=False)

    # Futuro uso de la api irian la lista de codigos de enfermededes
    personal_diseases: Mapped[str] = mapped_column(
        db.Text, nullable=True)      # Enfermedades personales
    medications: Mapped[str] = mapped_column(
        Text)                              # Medicamentos
    hospitalizations: Mapped[str] = mapped_column(
        Text)                         # Hospitalizaciones
    surgeries: Mapped[str] = mapped_column(
        Text)                                # Cirugías
    traumatisms: Mapped[str] = mapped_column(
        Text)                              # Traumatismos
    transfusions: Mapped[str] = mapped_column(
        Text)                             # Transfusiones
    allergies: Mapped[str] = mapped_column(
        Text)                                # Alergias
    # Otros antecedentes
    others: Mapped[str] = mapped_column(Text)

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="pathological_background")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "medical_file_id": self.medical_file_id,
            "personal_diseases": self.personal_diseases,
            "medications": self.medications,
            "hospitalizations": self.hospitalizations,
            "surgeries": self.surgeries,
            "traumatisms": self.traumatisms,
            "transfusions": self.transfusions,
            "allergies": self.allergies,
            "others": self.others
        }










# -------------------- MODELO: FamilyBackground --------------------
# RESUMEN: Contiene antecedentes familiares del paciente relacionados con enfermedades hereditarias.
class FamilyBackground(db.Model):
    __tablename__ = "family_background"
    id: Mapped[int] = mapped_column(
        primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        # Relación con expediente
        "medical_files.id"), nullable=False)

    hypertension: Mapped[bool] = mapped_column(
        # Hipertensión hereditaria
        Boolean, default=False)
    diabetes: Mapped[bool] = mapped_column(
        # Diabetes hereditaria
        Boolean, default=False)
    cancer: Mapped[bool] = mapped_column(
        # Cáncer familiar
        Boolean, default=False)
    heart_disease: Mapped[bool] = mapped_column(
        # Enfermedad del corazón
        Boolean, default=False)
    kidney_disease: Mapped[bool] = mapped_column(
        # Enfermedad renal
        Boolean, default=False)
    liver_disease: Mapped[bool] = mapped_column(
        # Enfermedad hepática
        Boolean, default=False)
    mental_illness: Mapped[bool] = mapped_column(
        # Trastornos mentales
        Boolean, default=False)
    congenital_malformations: Mapped[bool] = mapped_column(
        # Malformaciones congénitas
        Boolean, default=False)
    others: Mapped[str] = mapped_column(Text)

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="family_background")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "medical_file_id": self.medical_file_id,
            "hypertension": self.hypertension,
            "diabetes": self.diabetes,
            "cancer": self.cancer,
            "heart_disease": self.heart_disease,
            "kidney_disease": self.kidney_disease,
            "liver_disease": self.liver_disease,
            "mental_illness": self.mental_illness,
            "congenital_malformations": self.congenital_malformations,
            "others": self.others
        }










# -------------------- MODELO: GynecologicalBackground --------------------
# RESUMEN: Guarda antecedentes ginecológicos para pacientes mujeres, incluyendo embarazos, partos y métodos de planificación.
class GynecologicalBackground(db.Model):
    __tablename__ = "gynecological_background"
    id: Mapped[int] = mapped_column(
        primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        # Relación con expediente
        "medical_files.id"), nullable=False)

    menarche_age: Mapped[int] = mapped_column(
        # Edad de la primera menstruación
        Integer)
    pregnancies: Mapped[int] = mapped_column(
        Integer)                           # Número de embarazos
    # Número de partos
    births: Mapped[int] = mapped_column(Integer)
    c_sections: Mapped[int] = mapped_column(
        Integer)                            # Cesáreas
    abortions: Mapped[int] = mapped_column(
        Integer)                             # Abortos
    contraceptive_method: Mapped[str] = mapped_column(
        # Método anticonceptivo usado
        Text)
    others: Mapped[str] = mapped_column(Text)

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="gynecological_background")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "medical_file_id": self.medical_file_id,
            "menarche_age": self.menarche_age,
            "pregnancies": self.pregnancies,
            "births": self.births,
            "c_sections": self.c_sections,
            "abortions": self.abortions,
            "contraceptive_method": self.contraceptive_method,
            "others": self.others
        }










# -------------------- MODELO: NonPathologicalBackground --------------------
# RESUMEN: Guarda información sobre el estilo de vida del paciente, incluyendo ocupación, hábitos y factores de riesgo no médicos
class NonPathologicalBackground(db.Model):
    __tablename__ = "non_pathological_background"
    id: Mapped[int] = mapped_column(
        primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        # Relación con expediente
        "medical_files.id"), nullable=False)

    education_level: Mapped[str] = mapped_column(
        String(50))                    # Nivel educativo
    economic_activity: Mapped[str] = mapped_column(
        Text)                        # Actividad económica
    marital_status: Mapped[str] = mapped_column(
        String(30))                     # Estado civil
    # Dependientes económicos
    dependents: Mapped[str] = mapped_column(Text)
    occupation: Mapped[str] = mapped_column(
        String(50))                         # Ocupación

    recent_travels: Mapped[str] = mapped_column(
        Text)                           # Viajes recientes
    social_activities: Mapped[str] = mapped_column(
        # Actividades sociales
        Text)
    exercise: Mapped[str] = mapped_column(
        Text)                                 # Ejercicio físico
    diet_supplements: Mapped[str] = mapped_column(
        # Suplementos alimenticios
        Text)
    # Hábitos de higiene
    hygiene: Mapped[str] = mapped_column(Text)
    tattoos: Mapped[bool] = mapped_column(
        # ¿Tiene tatuajes?
        Boolean, default=False)
    piercings: Mapped[bool] = mapped_column(
        # ¿Tiene piercings?
        Boolean, default=False)
    hobbies: Mapped[str] = mapped_column(
        Text)                                  # Pasatiempos
    tobacco_use: Mapped[str] = mapped_column(
        Text)                              # Consumo de tabaco
    alcohol_use: Mapped[str] = mapped_column(
        Text)                              # Consumo de alcohol
    recreational_drugs: Mapped[str] = mapped_column(
        Text)                       # Drogas recreativas
    addictions: Mapped[str] = mapped_column(
        Text)                               # Adicciones
    # Otro tipo de antecedentes
    others: Mapped[str] = mapped_column(Text)

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="non_pathological_background")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "medical_file_id": self.medical_file_id,
            "education_level": self.education_level,
            "economic_activity": self.economic_activity,
            "marital_status": self.marital_status,
            "dependents": self.dependents,
            "occupation": self.occupation,
            "recent_travels": self.recent_travels,
            "social_activities": self.social_activities,
            "exercise": self.exercise,
            "diet_supplements": self.diet_supplements,
            "hygiene": self.hygiene,
            "tattoos": self.tattoos,
            "piercings": self.piercings,
            "hobbies": self.hobbies,
            "tobacco_use": self.tobacco_use,
            "alcohol_use": self.alcohol_use,
            "recreational_drugs": self.recreational_drugs,
            "addictions": self.addictions,
            "others": self.others
        }
