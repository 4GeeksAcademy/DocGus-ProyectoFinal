// Importa los hooks necesarios desde React

import React, { useEffect, useState } from "react";

import FileForm from "./FileForm"; // Ajusta la ruta si tu FileForm está en otro directorio

// Estado inicial con estructura de los antecedentes médicos
const initialState = {
  patological_background: {                      // Objeto Antecedentes Patologicos
    personal_diseases: "",
    medications: "",
    hospitalizations: "",
    surgeries: "",
    traumatisms: "",
    transfusions: "",
    allergies: "",
    others: "",
  },
  family_background: {                          // Objeto Antecedentes Familiares    
    hypertension: false,
    diabetes: false,
    cancer: false,
    heart_disease: false,
    kidney_disease: false,
    liver_disease: false,
    mental_illness: false,
    congenital_malformations: false,
    others: ""
  },
  non_pathological_background: {                 // Objeto Antecedentes No Patológicos 
    education_level: "",
    economic_activity: "",
    marital_status: "",
    dependents: "",
    occupation: "",
    recent_travels: "",
    social_activities: "",
    exercise: "",
    diet_supplements: "",
    hygiene: "",
    tattoos: false,
    piercings: false,
    hobbies: "",
    tobacco_use: "",
    alcohol_use: "",
    recreational_drugs: "",
    addictions: "",
    others: "",
  },
  gynecological_background: {                   // Objeto Antecedentes Ginecológicos
    menarche_age: "",
    pregnancies: "",
    births: "",
    c_sections: "",
    abortions: "",
    contraceptive_method: "",
    others: "",
  },
  personal_data: {
    sex: "",
    address: "",
  }
};



// Componente principal del formulario. Recibe `initialData` y `medicalFileId` como props
const BackgroundForm = ({ initialData, medicalFileId }) => {
  const [form, setForm] = useState(initialState);

  const handleChange = (e, section) => {
    const { name, value, type, checked } = e.target;
    const val = type === "checkbox" ? checked : value;

    setForm((prevForm) => ({
      ...prevForm,
      [section]: {
        ...prevForm[section],
        [name]: val,
      },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const user = JSON.parse(localStorage.getItem("user"));
    const userId = user?.id;

    const newFormData = {
      ...form,
      medical_file_id: medicalFileId,
      user_id: userId, // 👈 agregado según tu solicitud
    };

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/backgrounds`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(newFormData),
      });

      const data = await response.json();

      if (!response.ok) {
        console.error("Error en antecedentes:", data);
        alert("Error al guardar antecedentes.");
        return;
      }

      const personalDataResponse = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/personal_data`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          ...form.personal_data,
          medical_file_id: medicalFileId,
        }),
      });

      const personalData = await personalDataResponse.json();

      if (!personalDataResponse.ok) {
        console.error("Error en datos personales:", personalData);
        alert("Error al guardar datos personales.");
        return;
      }

      alert("Antecedentes y datos personales guardados correctamente.");
    } catch (err) {
      console.error("Error de conexión:", err);
      alert("Error de conexión con el servidor.");
    }
  };

  useEffect(() => {
    if (initialData) {
      setForm({ ...initialState, ...initialData });
    }
  }, [initialData]);

  console.log(form);                                                              // Para depuración: muestra el estado actual del formulario en consola




  // Formulario principal con clases de Bootstrap
  return (
    <form onSubmit={handleSubmit} className="row p-4 rounded shadow-md max-w-5xl mx-auto" data-bs-theme="dark">
      <h2 className="text-2xl font-bold mb-4">Antecedentes Médicos del Paciente</h2>



      {/* ---------- PERSONAL DATA ---------- */}
      <h4 className="mt-4 mb-2 text-lg font-semibold">Datos Personales</h4>

      <div className="mb-2 col-6">
        <label className="block">Sexo</label>
        <select
          name="sex"
          value={form.personal_data.sex}
          onChange={(e) => handleChange(e, "personal_data")}
          className="form-control"
        >
          <option value="">Selecciona</option>
          <option value="masculino">Masculino</option>
          <option value="femenino">Femenino</option>
          <option value="otro">Otro</option>
        </select>
      </div>

      <div className="mb-2 col-6">
        <label className="block">Dirección</label>
        <textarea
          name="address"
          value={form.personal_data.address}
          onChange={(e) => handleChange(e, "personal_data")}
          className="form-control"
        />
      </div>


      {/* ---------- PATHOLOGICAL BACKGROUND ---------- */}
      <h4 className="mt-4 mb-2 text-lg font-semibold">Antecedentes Patológicos</h4>
      {["personal_diseases", "medications", "hospitalizations", "surgeries", "traumatisms", "transfusions", "allergies", "others"].map((field) => (
        <div key={field} className="mb-2 col-6">
          <label className="block">{field.replace(/_/g, " ").replace("others pathological", "Otros")}</label>
          <textarea name={field} value={form.patological_background[field]} onChange={(e) => handleChange(e, "patological_background")} className="form-control" />
        </div>
      ))}





      {/* ---------- FAMILY BACKGROUND ---------- */}
      <h4 className="mt-4 mb-2 text-lg font-semibold">Antecedentes Familiares</h4>
      {["hypertension", "diabetes", "cancer", "heart_disease", "kidney_disease", "liver_disease", "mental_illness", "congenital_malformations"].map((field) => (
        <div key={field} className="form-check col-6 mb-2">
          <input className="form-check-input" type="checkbox" name={field} checked={form.family_background[field]} onChange={(e) => handleChange(e, "family_background")} />
          <label className="form-check-label">{field.replace(/_/g, " ")}</label>
        </div>
      ))}
      <div className="mb-2 col-6">
        <label className="block">Otros antecedentes familiares</label>
        <textarea name="others" value={form.others} onChange={(e) => handleChange(e, "family_background")} className="form-control" />
      </div>





      {/* ---------- NON-PATHOLOGICAL BACKGROUND ---------- */}
      <h4 className="mt-4 mb-2 text-lg font-semibold">Antecedentes No Patológicos</h4>
      {["education_level", "economic_activity", "marital_status", "dependents", "occupation", "recent_travels", "social_activities", "exercise", "diet_supplements", "hygiene", "hobbies", "tobacco_use", "alcohol_use", "recreational_drugs", "addictions", "others"].map((field) => (
        <div key={field} className="mb-2 col-6">
          <label className="block">{field.replace(/_/g, " ").replace("others nonpath", "Otros")}</label>
          <textarea name={field} value={form.non_pathological_background[field]} onChange={(e) => handleChange(e, "non_pathological_background")} className="form-control" />
        </div>
      ))}
      {["tattoos", "piercings"].map((field) => (
        <div key={field} className="form-check col-6 mb-2">
          <input className="form-check-input" type="checkbox" name={field} checked={form.non_pathological_background[field]} onChange={(e) => handleChange(e, "non_pathological_background")} />
          <label className="form-check-label">{field.charAt(0).toUpperCase() + field.slice(1)}</label>
        </div>
      ))}





      {/* ---------- GYNECOLOGICAL BACKGROUND ---------- */}
      <h4 className="mt-4 mb-2 text-lg font-semibold">Antecedentes Ginecológicos</h4>
      {["menarche_age", "pregnancies", "births", "c_sections", "abortions", "contraceptive_method", "others"].map((field) => (
        <div key={field} className="mb-2 col-6">
          <label className="block">{field.replace(/_/g, " ").replace("others gyneco", "Otros")}</label>
          <input type="text" name={field} value={form.gynecological_background[field]} onChange={(e) => handleChange(e, "gynecological_background")} className="form-control" />
        </div>
      ))}

      <div className="mt-4 col-12">
        <button type="submit" className="btn btn-primary me-2">Guardar</button>
        <button type="button" className="btn btn-secondary" onClick={() => window.history.back()}>Cancelar</button>
      </div>
    </form>
  );
};





// Exporta el componente para poder usarlo en otras partes de la app
export default BackgroundForm;