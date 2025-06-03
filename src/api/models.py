
# -------------------- INICIALIZACIÓN DE LA BASE DE DATOS --------------------


# RESUMEN: Se importan todos los módulos necesarios y se crea la instancia principal de la base de datos.
# Importa la extensión de SQLAlchemy para usarla con Flask
from flask_sqlalchemy import SQLAlchemy
# Importa tipos y funciones necesarios para definir columnas y relaciones en la base de datos
from sqlalchemy import String, Integer, Boolean, Date, DateTime, Column, ForeignKey, Enum, Text, func
# Importa utilidades para mapear columnas y relaciones en los modelos
from sqlalchemy.orm import Mapped, mapped_column, relationship
# Importa clase para trabajar con fechas y horas
from datetime import datetime
from datetime import date
# Importa módulo para crear enumeraciones (valores limitados)
import enum
# Crea una instancia de SQLAlchemy para usarla en la app Flask
db = SQLAlchemy()


# # -------------------- ENUMS PERSONALIZADOS --------------------
# # RESUMEN: Representa a los usuarios del sistema. Puede ser un administrador, profesional o paciente. (Estudiante????)
# # RESUMEN: Se crean dos enumeraciones para asegurar que ciertos campos solo tengan valores válidos: rol de usuario y sexo.
class UserRole(str, enum.Enum):  # Define roles posibles de usuario
    admin = "administrador"  # Usuario administrador
    profesional = "profesional"  # Usuario profesional de la salud
    paciente = "paciente"  # Usuario paciente
    # Usuario estudiante                 ## Define los tipos posibles de sexo biologico y alguna variedad anatomica o psicologica
    estudiante = "estudiante"


class FileStatus(str, enum.Enum):
    autorizado = "autorizado"
    rechazado = "rechazado"
    revision = "revision"
    confirmado = "confirmado"


class UserStatus(str, enum.Enum):
    pre_aprobado = "preaprobado"
    aprobado = "aprobado"
    inactivo = "inactivo"


class SexType(str, enum.Enum):
    femenino = "femenino"  # Sexo femenino
    masculino = "masculino"  # Sexo masculino
    otro = "otro"


# -------------------- MODELO: User --------------------
# Definicion y Descripcion
# RESUMEN: Modelo que representa a los usuarios del sistema. Puede contener la info de Id email y Rol


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    names: Mapped[str] = mapped_column(String(100), nullable=False)
    first_surname: Mapped[str] = mapped_column(String(100), nullable=False)
    second_surname: Mapped[str] = mapped_column(String(100), nullable=True)
    birth_day: Mapped[date] = mapped_column(nullable=False)
    profession: Mapped[str] = mapped_column(String(100), nullable=True)
    sex: Mapped[SexType] = mapped_column(Enum(SexType), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)

    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus), nullable=False, default=UserStatus.pre_aprobado)

    medical_file: Mapped["MedicalFile"] = relationship(
        back_populates="user", foreign_keys="[MedicalFile.user_id]", uselist=False, cascade="all, delete-orphan"
    )
    student_medical_files: Mapped[list["MedicalFile"]] = relationship(
        back_populates="creator", foreign_keys="[MedicalFile.created_by]", cascade="all, delete-orphan"
    )
    supervised_medical_files: Mapped[list["MedicalFile"]] = relationship(
        back_populates="supervisor", foreign_keys="[MedicalFile.supervised_by]", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.value,
            "status": self.status.value,
            "names": self.names,
            "first_surname": self.first_surname,
            "second_surname": self.second_surname,
            "birth_day": self.birth_day.isoformat(),
            "profession": self.profession,
            "medical_file": self.medical_file.serialize() if self.medical_file else None
        }

    def __repr__(self):
        return f"<User {self.id} - {self.email} .>"


# -------------------- MODELO: MedicalFile --------------------
# RESUMEN: Representa un expediente médico que puede ser creado por un profesional para un paciente.
# Definición de la clase MedicalFile que hereda de db.Model (SQLAlchemy)
class MedicalFile(db.Model):
    __tablename__ = "medical_files"  # Nombre que tendrá la tabla en la base de datos

    # Clave primaria del expediente ( del user), tipo entero
    id: Mapped[int] = mapped_column(primary_key=True)
    # ID del paciente relacionado (puede ser nulo)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    # ID del profesional que crea el expediente (obligatorio)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    # Fecha y hora de creación automática del expediente
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    supervised_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    # Fecha y hora de creación automática del expediente
    supervised_at: Mapped[datetime] = mapped_column(DateTime)
    confirmed_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped["FileStatus"] = mapped_column(
        Enum(FileStatus), nullable=False, default=FileStatus.revision.value)

    # Relación con el modelo User para acceder al paciente
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    # Revisar posteriormente relacion delicada     ## Relación con el modelo User para acceder al creador
    supervisor: Mapped["User"] = relationship(
        "User", foreign_keys=[supervised_by])

    personal_data: Mapped["PersonalData"] = relationship(
        # Relación uno a uno con el modelo PersonalData
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan")
    pathological_background: Mapped["PathologicalBackground"] = relationship(
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan")
    family_background: Mapped["FamilyBackground"] = relationship(
        # Relación uno a uno con el modelo PersonalData
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan")
    non_pathological_background: Mapped["NonPathologicalBackground"] = relationship(
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan")
    gynecological_background: Mapped["GynecologicalBackground"] = relationship(
        back_populates="medical_file", uselist=False, cascade="all, delete-orphan")

    def serialize(self):  # Método para convertir el expediente a un diccionario (útil para API/JSON)
        return {  # Retorna
            "id": self.id,  # El ID del expediente
            "user_id": self.user_id,  # El ID del paciente
            "created_by": self.created_by,  # El ID del profesional que lo creó
            "created_at": self.created_at.isoformat(),
            "supervised_by": self.supervised_by,
            # La fecha en formato legible ISO 8601
            "supervised_at": self.supervised_at.isoformat()
        }
        # Método para representar el expediente como una cadena
        # Retorna una cadena con el ID del expediente y el ID del paciente asociado
# Agregar quien autoriza que se quede en base de datos la entrevista o expediente


# -------------------- MODELO: PersonalData --------------------
# RESUMEN: Contiene los datos personales de un usuario. Está relacionado con su expediente y su cuenta de usuario.
class PersonalData(db.Model):
    __tablename__ = "personal_data"
    id: Mapped[int] = mapped_column(primary_key=True)  # ID único
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id"), nullable=False, unique=True)  # Relación 1:1 con usuario
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=True)  # Expediente asociado

    full_name: Mapped[str] = mapped_column(
        String(50), nullable=False)  # Nombre completo
    paternal_surname: Mapped[str] = mapped_column(
        String(30), nullable=False)  # Apellido paterno
    maternal_surname: Mapped[str] = mapped_column(
        String(30), nullable=True)  # Apellido materno (opcional)
    sex: Mapped[SexType] = mapped_column(Enum(SexType))  # Sexo (enum)
    birth_date: Mapped[datetime.date] = mapped_column(
        Date())  # Fecha de nacimiento
    address: Mapped[str] = mapped_column(Text)  # Dirección
    phone: Mapped[str] = mapped_column(String(30))  # Teléfono

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="personal_data")


# -------------------- MODELO: PathologicalBackground --------------------
# RESUMEN: Almacena antecedentes patológicos personales del paciente, como enfermedades, cirugías y alergias.
class PathologicalBackground(db.Model):
    __tablename__ = "pathological_background"
    id: Mapped[int] = mapped_column(primary_key=True)  # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=False)  # Relación con expediente

    # Futuro uso de la api irian la lista de codigos de enfermededes                                                                        ## Enfermedades personales
    personal_diseases: Mapped[str] = mapped_column(db.Text, nullable=True)
    medications: Mapped[str] = mapped_column(Text)  # Medicamentos
    hospitalizations: Mapped[str] = mapped_column(Text)  # Hospitalizaciones
    surgeries: Mapped[str] = mapped_column(Text)  # Cirugías
    traumatisms: Mapped[str] = mapped_column(Text)  # Traumatismos
    transfusions: Mapped[str] = mapped_column(Text)  # Transfusiones
    allergies: Mapped[str] = mapped_column(Text)  # Alergias
    others: Mapped[str] = mapped_column(Text)  # Otros antecedentes

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="pathological_background")


# -------------------- MODELO: FamilyBackground --------------------
# RESUMEN: Contiene antecedentes familiares del paciente relacionados con enfermedades hereditarias.
class FamilyBackground(db.Model):
    __tablename__ = "family_background"
    id: Mapped[int] = mapped_column(primary_key=True)  # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=False)  # Relación con expediente

    hypertension: Mapped[bool] = mapped_column(
        Boolean, default=False)  # Hipertensión hereditaria
    diabetes: Mapped[bool] = mapped_column(
        Boolean, default=False)  # Diabetes hereditaria
    cancer: Mapped[bool] = mapped_column(
        Boolean, default=False)  # Cáncer familiar
    heart_disease: Mapped[bool] = mapped_column(
        Boolean, default=False)  # Enfermedad del corazón
    kidney_disease: Mapped[bool] = mapped_column(
        Boolean, default=False)  # Enfermedad renal
    liver_disease: Mapped[bool] = mapped_column(
        Boolean, default=False)  # Enfermedad hepática
    mental_illness: Mapped[bool] = mapped_column(
        Boolean, default=False)  # Trastornos mentales
    congenital_malformations: Mapped[bool] = mapped_column(
        Boolean, default=False)  # Malformaciones congénitas
    others: Mapped[str] = mapped_column(Text)

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="family_background")


# -------------------- MODELO: GynecologicalBackground --------------------
# RESUMEN: Guarda antecedentes ginecológicos para pacientes mujeres, incluyendo embarazos, partos y métodos de planificación.
class GynecologicalBackground(db.Model):
    __tablename__ = "gynecological_background"
    id: Mapped[int] = mapped_column(primary_key=True)  # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=False)  # Relación con expediente

    menarche_age: Mapped[int] = mapped_column(
        Integer)  # Edad de la primera menstruación
    pregnancies: Mapped[int] = mapped_column(Integer)  # Número de embarazos
    births: Mapped[int] = mapped_column(Integer)  # Número de partos
    c_sections: Mapped[int] = mapped_column(Integer)  # Cesáreas
    abortions: Mapped[int] = mapped_column(Integer)  # Abortos
    contraceptive_method: Mapped[str] = mapped_column(
        Text)  # Método anticonceptivo usado
    others: Mapped[str] = mapped_column(Text)

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="gynecological_background")


# -------------------- MODELO: NonPathologicalBackground --------------------
# RESUMEN: Guarda información sobre el estilo de vida del paciente, incluyendo ocupación, hábitos y factores de riesgo no médicos
class NonPathologicalBackground(db.Model):
    __tablename__ = "non_pathological_background"
    id: Mapped[int] = mapped_column(primary_key=True)  # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=False)  # Relación con expediente

    education_level: Mapped[str] = mapped_column(String(50))  # Nivel educativo
    economic_activity: Mapped[str] = mapped_column(Text)  # Actividad económica
    marital_status: Mapped[str] = mapped_column(String(30))  # Estado civil
    dependents: Mapped[str] = mapped_column(Text)  # Dependientes económicos
    occupation: Mapped[str] = mapped_column(String(50))  # Ocupación

    recent_travels: Mapped[str] = mapped_column(Text)  # Viajes recientes
    social_activities: Mapped[str] = mapped_column(
        Text)  # Actividades sociales
    exercise: Mapped[str] = mapped_column(Text)  # Ejercicio físico
    diet_supplements: Mapped[str] = mapped_column(
        Text)  # Suplementos alimenticios
    hygiene: Mapped[str] = mapped_column(Text)  # Hábitos de higiene
    tattoos: Mapped[bool] = mapped_column(
        Boolean, default=False)  # ¿Tiene tatuajes?
    piercings: Mapped[bool] = mapped_column(
        Boolean, default=False)  # ¿Tiene piercings?
    hobbies: Mapped[str] = mapped_column(Text)  # Pasatiempos
    tobacco_use: Mapped[str] = mapped_column(Text)  # Consumo de tabaco
    alcohol_use: Mapped[str] = mapped_column(Text)  # Consumo de alcohol
    recreational_drugs: Mapped[str] = mapped_column(Text)  # Drogas recreativas
    addictions: Mapped[str] = mapped_column(Text)  # Adicciones
    otherS: Mapped[str] = mapped_column(Text)  # Otro tipo de antecedentes

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="non_pathological_background")


