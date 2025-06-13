# Permite que los administradores vean, editen, creen y eliminen registros directamente desde el navegador 
# en todas las tablas clave del proyecto, como usuarios, expedientes médicos y antecedentes clínicos.
 
 
   
import os                                                       # Importa el módulo `os` para acceder a variables de entorno
from flask_admin import Admin                                   # Importa la clase `Admin` de Flask-Admin para crear una interfaz de administración
from flask_admin.contrib.sqla import ModelView                  # Importa `ModelView` para crear vistas de modelos SQLAlchemy en la interfaz de administración
from flask_admin import expose                                  # Importa `expose` para definir rutas personalizadas en las vistas de administración 
from .models import (                                           # Importa los modelos necesarios desde el módulo `models`          
    db,
    User,
    MedicalFile,
    PersonalData,
    PatientData,
    StudentData,
    ProfessionalData,
    PathologicalBackground,
    FamilyBackground,
    GynecologicalBackground,
    NonPathologicalBackground
)

class UserView(ModelView):                                                                  # Define una vista personalizada para el modelo `User`  
    column_list = [
        "id", "email", "role", "status",
        "first_name", "second_name", "first_surname", "second_surname", 
        "birth_day",  "password", "phone", 
    ]

class MedicalFileView(ModelView):                                                           # Define una vista personalizada para el modelo `MedicalFile`
    column_list = [
        "id", "status", "created_at", "created_by", "user_id",
        "creator", "user",
        "gynecological_background", "non_pathological_background",
        "family_background", "pathological_background", "personal_data"
    ]

class PatientDataView(ModelView):                                                           # Define una vista personalizada para el modelo `PatientData`
    column_list = [
        "id", "user_id", "medical_file_id"
    ]

class PersonalDataView(ModelView):                                                          # Define una vista personalizada para el modelo `PersonalData`
    column_list = [
        "id", "user_id", "sex", "address"
    ]

class StudentDataView(ModelView):                                                           # Define una vista personalizada para el modelo `StudentData`
    column_list = [
        "id", "user_id", "academic_grade"
    ]

class ProfessionalDataView(ModelView):                                                      # Define una vista personalizada para el modelo `ProfessionalData`
    column_list = [
        "id", "user_id", "profession"
    ]

class PathologicalBackgroundView(ModelView):                                                # Define una vista personalizada para el modelo `PathologicalBackground`
    column_list = [
        "id", "user_id", "medical_file_id",
        "personal_diseases", "medications", "hospitalizations",
        "surgeries", "traumatisms", "transfusions",
        "allergies", "others"
    ]

class FamilyBackgroundView(ModelView):                                                      # Define una vista personalizada para el modelo `FamilyBackground`
    column_list = [
        "id", "user_id", "medical_file_id",
        "hypertension", "diabetes", "cancer",
        "heart_disease", "kidney_disease", "liver_disease",
        "mental_illness", "congenital_malformations"
    ]

class GynecologicalBackgroundView(ModelView):                                               # Define una vista personalizada para el modelo `GynecologicalBackground`
    column_list = [
        "id", "user_id", "medical_file_id",
        "menarche_age", "pregnancies", "births",
        "c_sections", "abortions", "contraceptive_method"
    ]

class NonPathologicalBackgroundView(ModelView):                                             # Define una vista personalizada para el modelo `NonPathologicalBackground`
    column_list = [
        "id", "user_id", "medical_file_id",
        "education_level", "economic_activity", "marital_status",
        "dependents", "occupation", "recent_travels",
        "social_activities", "exercise", "diet_supplements",
        "hygiene", "tattoos", "piercings", "hobbies",
        "tobacco_use", "alcohol_use", "recreational_drugs",
        "addictions", "other"
    ]

def setup_admin(app):                                                                       # Define una función para configurar el panel de administración
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')                          # Configura la clave secreta de la aplicación Flask
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'                                           # Configura el tema del panel de administración
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')                     # Crea una instancia de `Admin` con la aplicación Flask, nombre y modo de plantilla 

    # Agregar las vistas personalizadas al admin
    admin.add_view(UserView(User, db.session))
    admin.add_view(MedicalFileView(MedicalFile, db.session))
    admin.add_view(PersonalDataView(PersonalData, db.session))
    admin.add_view(PatientDataView(PatientData, db.session))
    admin.add_view(StudentDataView(StudentData, db.session))
    admin.add_view(ProfessionalDataView(ProfessionalData, db.session))
    admin.add_view(PathologicalBackgroundView(PathologicalBackground, db.session))
    admin.add_view(FamilyBackgroundView(FamilyBackground, db.session))
    admin.add_view(GynecologicalBackgroundView(GynecologicalBackground, db.session))
    admin.add_view(NonPathologicalBackgroundView(NonPathologicalBackground, db.session))

    