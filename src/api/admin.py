  
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import (
    db,
    User,
    MedicalFile,
    PersonalData,
    PathologicalBackground,
    FamilyBackground,
    GynecologicalBackground,
    NonPathologicalBackground
)

class UserView(ModelView):
    column_list = [
        "id", "email", "role", "status",
        "medical_file", "student_medical_files"
    ]

class MedicalFileView(ModelView):
    column_list = [
        "id", "status", "created_at", "created_by", "user_id",
        "creator", "user",
        "gynecological_background", "non_pathological_background",
        "family_background", "pathological_background", "personal_data"
    ]

class PersonalDataView(ModelView):
    column_list = [
        "id", "user_id", "medical_file_id",
        "full_name", "paternal_surname", "maternal_surname",
        "sex", "birth_date", "address", "phone"
    ]

class PathologicalBackgroundView(ModelView):
    column_list = [
        "id", "user_id", "medical_file_id",
        "personal_diseases", "medications", "hospitalizations",
        "surgeries", "traumatisms", "transfusions",
        "allergies", "others"
    ]

class FamilyBackgroundView(ModelView):
    column_list = [
        "id", "user_id", "medical_file_id",
        "hypertension", "diabetes", "cancer",
        "heart_disease", "kidney_disease", "liver_disease",
        "mental_illness", "congenital_malformations"
    ]

class GynecologicalBackgroundView(ModelView):
    column_list = [
        "id", "user_id", "medical_file_id",
        "menarche_age", "pregnancies", "births",
        "c_sections", "abortions", "contraceptive_method"
    ]

class NonPathologicalBackgroundView(ModelView):
    column_list = [
        "id", "user_id", "medical_file_id",
        "education_level", "economic_activity", "marital_status",
        "dependents", "occupation", "recent_travels",
        "social_activities", "exercise", "diet_supplements",
        "hygiene", "tattoos", "piercings", "hobbies",
        "tobacco_use", "alcohol_use", "recreational_drugs",
        "addictions", "other"
    ]

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Agregar las vistas personalizadas al admin
    admin.add_view(UserView(User, db.session))
    admin.add_view(MedicalFileView(MedicalFile, db.session))
    admin.add_view(PersonalDataView(PersonalData, db.session))
    admin.add_view(PathologicalBackgroundView(PathologicalBackground, db.session))
    admin.add_view(FamilyBackgroundView(FamilyBackground, db.session))
    admin.add_view(GynecologicalBackgroundView(GynecologicalBackground, db.session))
    admin.add_view(NonPathologicalBackgroundView(NonPathologicalBackground, db.session))

    