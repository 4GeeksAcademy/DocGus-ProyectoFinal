# -------------------- INICIALIZACIÓN DE LA BASE DE DATOS --------------------


# Se importan todos los módulos necesarios y se crea la instancia principal de la base de datos.
from flask_sqlalchemy import SQLAlchemy                                                                     # Importa la extensión de SQLAlchemy para usarla con Flask
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Enum, Text, func                     # Importa tipos y funciones necesarios para definir columnas y relaciones en la base de datos
from sqlalchemy.orm import Mapped, mapped_column, relationship                                              # Importa utilidades para mapear columnas y relaciones en los modelos
from datetime import datetime                                                                               # Importa clase para trabajar con fechas y horas
from datetime import date                                                                                   # Importa clase para trabajar con fechas      
import enum                                                                                                 # Importa módulo para crear enumeraciones (valores limitados)

db = SQLAlchemy()                                                                                           # Crea una instancia de SQLAlchemy para usarla en la app Flask










# # -------------------- ENUMS PERSONALIZADOS --------------------
# # RESUMEN: Representa a los usuarios del sistema. Puede ser un administrador, profesional o paciente. (Estudiante????)
# # RESUMEN: Se crean dos enumeraciones para asegurar que ciertos campos solo tengan valores válidos: rol de usuario y sexo.
class UserRole(str, enum.Enum):             # Define roles posibles de usuario
    administrador = "administrador"         # Usuario administrador
    profesional = "profesional"             # Usuario profesional de la salud
    paciente = "paciente"                   # Usuario paciente       
    estudiante = "estudiante"               # Usuario estudiante  


class FileStatus(str, enum.Enum):           # Define los estados posibles de un expediente médico
    PROGRESS = "PROGRESS"                   # El expediente está en progreso (llenándose)
    REVIEW = "REVIEW"                       # El expediente está en revisión por el profesional
    APPROVED = "APPROVED"                   # El expediente fue aprobado por el profesional
    CONFIRMED = "CONFIRMED"                 # El expediente fue confirmado por el paciente


class UserStatus(str, enum.Enum):           # Define los estados posibles de validación del usuario
    preaprobado = "preaprobado"             # Usuario registrado, pendiente de aprobación
    aprobado = "aprobado"                   # Usuario aprobado y activo
    inactivo = "inactivo"                   # Usuario inactivo o suspendido

# Define los tipos posibles de sexo biologico y variedades anatomicas las custiones de identidad de genero son propias del area psicologica de este expediente
class SexType(str, enum.Enum):  
    femenino = "femenino"                   # Sexo femenino
    masculino = "masculino"                 # Sexo masculino
    otro = "otro"                           # Hermafroditismo u otros

# Define los niveles académicos posibles para profesionales
class AcademicGrade(str, enum.Enum):        
    tecnico = "tecnico"                     # Nivel técnico (carrera técnica o equivalente)
    profesionista = "profesionista"         # Profesional titulado (licenciatura o superior)

# -------------------- MODELO: User --------------------
# Definicion y Descripcion
# RESUMEN: Modelo que representa a los usuarios del sistema. Puede contener la info de Id email y Rol


class User(db.Model):  # Modelo principal para todos los tipos de usuarios del sistema
    __tablename__ = "users"  # Nombre de la tabla en la base de datos

    id: Mapped[int] = mapped_column(primary_key=True)                               # Identificador único del usuario (clave primaria)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)            # Primer nombre del usuario
    second_name: Mapped[str] = mapped_column(String(100), nullable=True)            # Segundo nombre del usuario (opcional)
    first_surname: Mapped[str] = mapped_column(String(100), nullable=False)         # Primer apellido del usuario
    second_surname: Mapped[str] = mapped_column(String(100), nullable=True)         # Segundo apellido del usuario (opcional)
    birth_day: Mapped[date] = mapped_column(nullable=False)                         # Fecha de nacimiento del usuario
    phone: Mapped[str] = mapped_column(String(20), nullable=True)                   # Número de teléfono (opcional)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)     # Correo electrónico único
    password: Mapped[str] = mapped_column(String(200), nullable=False)              # Contraseña cifrada del usuario
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)          # Rol del usuario (enum)
    status: Mapped[UserStatus] = mapped_column(                                     # Estado del usuario (enum)
        Enum(UserStatus), nullable=False, default=UserStatus.preaprobado            # Valor por defecto: preaprobado
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
            "id": self.id,                                                                  # ID del usuario
            "email": self.email,                                                            # Correo electrónico
            "role": self.role.value,                                                        # Rol del usuario (como string)
            "status": self.status.value,                                                    # Estado del usuario (como string)
            "first_name": self.first_name,                                                  # Primer nombre
            "second_name": self.second_name,                                                # Segundo nombre
            "first_surname": self.first_surname,                                            # Primer apellido
            "second_surname": self.second_surname,                                          # Segundo apellido
            "birth_day": self.birth_day.isoformat(),                                        # Fecha de nacimiento en formato ISO
            "phone": self.phone,                                                            # Teléfono
            "medical_file": self.medical_file.serialize() if self.medical_file else None    # Expediente médico serializado
        }

    def __repr__(self):                                                                     # Representación legible del objeto para debugging
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
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # ID del profesional que supervisa la revisión
    supervised_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    supervised_at: Mapped[datetime] = mapped_column(DateTime)

    # Nuevo: ID del profesional que aprueba
    approved_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
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
    supervisor: Mapped["User"] = relationship("User", foreign_keys=[supervised_by])
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
        
        # Método para representar el expediente como una cadena
        # Retorna una cadena con el ID del expediente y el ID del paciente asociado
        # Agregar quien autoriza que se quede en base de datos la entrevista o expediente


# -------------------- MODELO: PersonalData --------------------
# RESUMEN: Contiene los datos personales de un usuario. Está relacionado con su expediente y su cuenta de usuario.
class PersonalData(db.Model):
    __tablename__ = "personal_data"
    id: Mapped[int] = mapped_column(primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id"), nullable=False, unique=True)                               # Relación 1:1 con usuario
    sex: Mapped[SexType] = mapped_column(Enum(SexType))                         # Sexo (enum)
    address: Mapped[str] = mapped_column(Text)                                  # Dirección

    # Relación con el modelo User
    user: Mapped["User"] = relationship("User", back_populates="personal_data", uselist=False)

    def serialize(self):
        return {
            **self.user.serialize(),                                            # Incluye la serialización del usuario
            "id": self.id,
            "sex": self.sex.value if hasattr(self.sex, "value") else self.sex,
            "address": self.address,
        }

class PatientData(db.Model):
    __tablename__ = "patient_data"
    id: Mapped[int] = mapped_column(primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id"), nullable=False, unique=True)                               # Relación 1:1 con usuario
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=True)                                     # Expediente asociado
    
    
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
    id: Mapped[int] = mapped_column(primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id"), nullable=False, unique=True)                               # Relación 1:1 con usuario
    academic_grade: Mapped[AcademicGrade] = mapped_column(Enum(AcademicGrade), nullable=False)


    # Relación con el modelo User
    user: Mapped["User"] = relationship("User", back_populates="student_data", uselist=False)       

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
    user: Mapped["User"] = relationship("User", back_populates="professional_data", uselist=False)      

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
    id: Mapped[int] = mapped_column(primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=False)                                    # Relación con expediente

    # Futuro uso de la api irian la lista de codigos de enfermededes            
    personal_diseases: Mapped[str] = mapped_column(db.Text, nullable=True)      # Enfermedades personales
    medications: Mapped[str] = mapped_column(Text)                              # Medicamentos
    hospitalizations: Mapped[str] = mapped_column(Text)                         # Hospitalizaciones
    surgeries: Mapped[str] = mapped_column(Text)                                # Cirugías
    traumatisms: Mapped[str] = mapped_column(Text)                              # Traumatismos
    transfusions: Mapped[str] = mapped_column(Text)                             # Transfusiones
    allergies: Mapped[str] = mapped_column(Text)                                # Alergias
    others: Mapped[str] = mapped_column(Text)                                   # Otros antecedentes

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="pathological_background")


# -------------------- MODELO: FamilyBackground --------------------
# RESUMEN: Contiene antecedentes familiares del paciente relacionados con enfermedades hereditarias.
class FamilyBackground(db.Model):
    __tablename__ = "family_background"
    id: Mapped[int] = mapped_column(primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=False)                                    # Relación con expediente

    hypertension: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # Hipertensión hereditaria
    diabetes: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # Diabetes hereditaria
    cancer: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # Cáncer familiar
    heart_disease: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # Enfermedad del corazón
    kidney_disease: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # Enfermedad renal
    liver_disease: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # Enfermedad hepática
    mental_illness: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # Trastornos mentales
    congenital_malformations: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # Malformaciones congénitas
    others: Mapped[str] = mapped_column(Text)

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="family_background")


# -------------------- MODELO: GynecologicalBackground --------------------
# RESUMEN: Guarda antecedentes ginecológicos para pacientes mujeres, incluyendo embarazos, partos y métodos de planificación.
class GynecologicalBackground(db.Model):
    __tablename__ = "gynecological_background"
    id: Mapped[int] = mapped_column(primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=False)                                    # Relación con expediente

    menarche_age: Mapped[int] = mapped_column(
        Integer)                                                                # Edad de la primera menstruación
    pregnancies: Mapped[int] = mapped_column(Integer)                           # Número de embarazos
    births: Mapped[int] = mapped_column(Integer)                                # Número de partos
    c_sections: Mapped[int] = mapped_column(Integer)                            # Cesáreas
    abortions: Mapped[int] = mapped_column(Integer)                             # Abortos
    contraceptive_method: Mapped[str] = mapped_column(
        Text)                                                                   # Método anticonceptivo usado
    others: Mapped[str] = mapped_column(Text)

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="gynecological_background")


# -------------------- MODELO: NonPathologicalBackground --------------------
# RESUMEN: Guarda información sobre el estilo de vida del paciente, incluyendo ocupación, hábitos y factores de riesgo no médicos
class NonPathologicalBackground(db.Model):
    __tablename__ = "non_pathological_background"
    id: Mapped[int] = mapped_column(primary_key=True)                           # ID único
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey(
        "medical_files.id"), nullable=False)                                    # Relación con expediente

    education_level: Mapped[str] = mapped_column(String(50))                    # Nivel educativo
    economic_activity: Mapped[str] = mapped_column(Text)                        # Actividad económica
    marital_status: Mapped[str] = mapped_column(String(30))                     # Estado civil
    dependents: Mapped[str] = mapped_column(Text)                               # Dependientes económicos
    occupation: Mapped[str] = mapped_column(String(50))                         # Ocupación

    recent_travels: Mapped[str] = mapped_column(Text)                           # Viajes recientes
    social_activities: Mapped[str] = mapped_column(
        Text)                                                                   # Actividades sociales
    exercise: Mapped[str] = mapped_column(Text)                                 # Ejercicio físico
    diet_supplements: Mapped[str] = mapped_column(
        Text)                                                                   # Suplementos alimenticios
    hygiene: Mapped[str] = mapped_column(Text)                                  # Hábitos de higiene
    tattoos: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # ¿Tiene tatuajes?
    piercings: Mapped[bool] = mapped_column(
        Boolean, default=False)                                                 # ¿Tiene piercings?
    hobbies: Mapped[str] = mapped_column(Text)                                  # Pasatiempos
    tobacco_use: Mapped[str] = mapped_column(Text)                              # Consumo de tabaco
    alcohol_use: Mapped[str] = mapped_column(Text)                              # Consumo de alcohol
    recreational_drugs: Mapped[str] = mapped_column(Text)                       # Drogas recreativas
    addictions: Mapped[str] = mapped_column(Text)                               # Adicciones
    otherS: Mapped[str] = mapped_column(Text)                                   # Otro tipo de antecedentes

    medical_file: Mapped["MedicalFile"] = relationship(
        "MedicalFile", back_populates="non_pathological_background")


