from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, Date, DateTime, ForeignKey, Enum, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum

# Inicializa la base de datos
db = SQLAlchemy()

# ENUMS personalizados
class UserRole(enum.Enum):
    admin = "admin"
    medico = "medico"
    paciente = "paciente"

class SexType(enum.Enum):
    masculino = "masculino"
    femenino = "femenino"
    otro = "otro"

# MODELOS
class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    names: Mapped[str] = mapped_column(String(30), nullable=False)
    first_surname: Mapped[str] = mapped_column(String(30), nullable=False)
    second_surname: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    birth_day: Mapped[datetime] = mapped_column(Date, nullable=False)
    profession: Mapped[str] = mapped_column(String(20))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    sex: Mapped[SexType] = mapped_column(Enum(SexType))
    phone: Mapped[str] = mapped_column(String(20))

    def serialize(self):
        return {
            "id": self.id,
            "names": self.names,
            "first_surname": self.first_surname,
            "email": self.email,
            "birth_day": self.birth_day.isoformat(),
            "role": self.role.value,
        }

class MedicalFile(db.Model):
    __tablename__ = "medical_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])

    def serialize(self):
        return {
            "id": self.id,
            "file_number": self.file_number,
            "user_id": self.user_id,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }

class PersonalData(db.Model):
    __tablename__ = "personal_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey("medical_files.id"), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    paternal_surname: Mapped[str] = mapped_column(String(30), nullable=False)
    maternal_surname: Mapped[str] = mapped_column(String(30))
    sex: Mapped[SexType] = mapped_column(Enum(SexType))
    birth_day: Mapped[datetime] = mapped_column(Date)
    age: Mapped[int] = mapped_column(Integer)
    address: Mapped[str] = mapped_column(Text)
    phone: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(30))

class PathologicalBackground(db.Model):
    __tablename__ = "pathological_background"

    id: Mapped[int] = mapped_column(primary_key=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey("medical_files.id"), nullable=False)
    personal_diseases: Mapped[str] = mapped_column(Text)
    medications: Mapped[str] = mapped_column(Text)
    hospitalizations: Mapped[str] = mapped_column(Text)
    surgeries: Mapped[str] = mapped_column(Text)
    traumas: Mapped[str] = mapped_column(Text)
    transfusions: Mapped[str] = mapped_column(Text)
    allergies: Mapped[str] = mapped_column(Text)
    others: Mapped[str] = mapped_column(Text)

class FamilyBackground(db.Model):
    __tablename__ = "family_background"

    id: Mapped[int] = mapped_column(primary_key=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey("medical_files.id"), nullable=False)
    hypertension: Mapped[bool] = mapped_column(Boolean, default=False)
    diabetes: Mapped[bool] = mapped_column(Boolean, default=False)
    cancer: Mapped[bool] = mapped_column(Boolean, default=False)
    heart_disease: Mapped[bool] = mapped_column(Boolean, default=False)
    kidney_disease: Mapped[bool] = mapped_column(Boolean, default=False)
    liver_disease: Mapped[bool] = mapped_column(Boolean, default=False)
    mental_illness: Mapped[bool] = mapped_column(Boolean, default=False)
    congenital_malformations: Mapped[bool] = mapped_column(Boolean, default=False)

class GynecologicalBackground(db.Model):
    __tablename__ = "gynecological_background"

    id: Mapped[int] = mapped_column(primary_key=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey("medical_files.id"), nullable=False)
    menarche_age: Mapped[int] = mapped_column(Integer)
    pregnancies: Mapped[int] = mapped_column(Integer)
    births: Mapped[int] = mapped_column(Integer)
    c_sections: Mapped[int] = mapped_column(Integer)
    abortions: Mapped[int] = mapped_column(Integer)
    contraceptive_method: Mapped[str] = mapped_column(Text)

class NonPathologicalBackground(db.Model):
    __tablename__ = "non_pathological_background"

    id: Mapped[int] = mapped_column(primary_key=True)
    medical_file_id: Mapped[int] = mapped_column(ForeignKey("medical_files.id"), nullable=False)
    economic_activity: Mapped[str] = mapped_column(Text)
    marital_status: Mapped[str] = mapped_column(String(30))
    dependents: Mapped[str] = mapped_column(Text)
    education_level: Mapped[str] = mapped_column(String(50))
    occupation: Mapped[str] = mapped_column(String(50))
    recent_travels: Mapped[str] = mapped_column(Text)
    social_activities: Mapped[str] = mapped_column(Text)
    exercise: Mapped[str] = mapped_column(Text)
    diet_supplements: Mapped[str] = mapped_column(Text)
    hygiene: Mapped[str] = mapped_column(Text)
    tattoos: Mapped[bool] = mapped_column(Boolean, default=False)
    piercings: Mapped[bool] = mapped_column(Boolean, default=False)
    hobbies: Mapped[str] = mapped_column(Text)
    tobacco_use: Mapped[str] = mapped_column(Text)
    alcohol_use: Mapped[str] = mapped_column(Text)
    recreational_drugs: Mapped[str] = mapped_column(Text)
    addictions: Mapped[str] = mapped_column(Text)
    other: Mapped[str] = mapped_column(Text)
