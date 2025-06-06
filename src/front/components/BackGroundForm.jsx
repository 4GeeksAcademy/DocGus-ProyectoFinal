import React, { useEffect, useState } from "react";


const initialState = {
  patological_background: {
    personal_diseases: "",
    medications: "",
    hospitalizations: "",
    surgeries: "",
    traumatisms: "",
    transfusions: "",
    allergies: "",
    others_pathological: "",
  },
  family_background: {
    hypertension: false,
    diabetes: false,
    cancer: false,
    heart_disease: false,
    kidney_disease: false,
    liver_disease: false,
    mental_illness: false,
    congenital_malformations: false,
    others_family: ""
  },
  non_pathological_background: {
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
    others_nonpath: "",
  },
  gynecological_background: {
    menarche_age: "",
    pregnancies: "",
    births: "",
    c_sections: "",
    abortions: "",
    contraceptive_method: "",
    others_gyneco: "",
  }
};

const BackgroundForm = ({initialData, medicalFileId }) => {
  const [form, setForm] = useState(initialState);

  const handleChange = (e, obj) => {
    const { name, value, type, checked } = e.target;
    const val = type === "checkbox" ? checked : value;
    setForm({ ...form, [obj]: { ...form[obj], [name]: value } });
  };

  const handleSubmit = async (e) => {
    const newFormData= { ...form, medical_file_id: medicalFileId };
  e.preventDefault();

  try {
    const response = await fetch(`${process.env.BACKEND_URL}/api/medical_background/${medicalFileId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`, // Si usas JWT
      },
      body: JSON.stringify(newFormData),
    });

    const data = await response.json();

    if (response.ok) {
      alert("Antecedentes guardados correctamente.");
    } else {
      console.error(data);
      alert("Error al guardar antecedentes.");
    }
  } catch (err) {
    console.error(err);
    alert("Error de conexión con el servidor.");
  }
};


  useEffect(() => {
    if (initialData) {
      setForm({ ...initialState, ...initialData });
    }
  }, [initialData]);
console.log(form)
  return (
    <form onSubmit={handleSubmit} className="row p-4 rounded shadow-md max-w-5xl mx-auto" data-bs-theme="dark">
      <h2 className="text-2xl font-bold mb-4">Antecedentes Médicos del Paciente</h2>

      {/* ---------- PATHOLOGICAL BACKGROUND ---------- */}
      <h4 className="mt-4 mb-2 text-lg font-semibold">Antecedentes Patológicos</h4>
      {["personal_diseases", "medications", "hospitalizations", "surgeries", "traumatisms", "transfusions", "allergies", "others_pathological"].map((field) => (
        <div key={field} className="mb-2 col-6">
          <label className="block">{field.replace(/_/g, " ").replace("others pathological", "Otros")}</label>
          <textarea name={field} value={form.patological_background[field]} onChange={(e)=> handleChange(e, "patological_background")} className="form-control" />
        </div>
      ))}

      {/* ---------- FAMILY BACKGROUND ---------- */}
      <h4 className="mt-4 mb-2 text-lg font-semibold">Antecedentes Familiares</h4>
      {["hypertension", "diabetes", "cancer", "heart_disease", "kidney_disease", "liver_disease", "mental_illness", "congenital_malformations"].map((field) => (
        <div key={field} className="form-check col-6 mb-2">
          <input className="form-check-input" type="checkbox" name={field} checked={form.family_background[field]} onChange={(e)=> handleChange(e, " family_background")} />
          <label className="form-check-label">{field.replace(/_/g, " ")}</label>
        </div>
      ))}
      <div className="mb-2 col-6">
        <label className="block">Otros antecedentes familiares</label>
        <textarea name="others_family" value={form.others_family} onChange={(e)=> handleChange(e, " family_background")} className="form-control" />
      </div>

      {/* ---------- NON-PATHOLOGICAL BACKGROUND ---------- */}
      <h4 className="mt-4 mb-2 text-lg font-semibold">Antecedentes No Patológicos</h4>
      {["education_level", "economic_activity", "marital_status", "dependents", "occupation", "recent_travels", "social_activities", "exercise", "diet_supplements", "hygiene", "hobbies", "tobacco_use", "alcohol_use", "recreational_drugs", "addictions", "others_nonpath"].map((field) => (
        <div key={field} className="mb-2 col-6">
          <label className="block">{field.replace(/_/g, " ").replace("others nonpath", "Otros")}</label>
          <textarea name={field} value={form.non_pathological_background[field]} onChange={(e)=> handleChange(e, "non_patological_background")} className="form-control" />
        </div>
      ))}
      {["tattoos", "piercings"].map((field) => (
        <div key={field} className="form-check col-6 mb-2">
          <input className="form-check-input" type="checkbox" name={field} checked={form.non_pathological_background[field]} onChange={(e)=> handleChange(e, "non_patological_background")} />
          <label className="form-check-label">{field.charAt(0).toUpperCase() + field.slice(1)}</label>
        </div>
      ))}

      {/* ---------- GYNECOLOGICAL BACKGROUND ---------- */}
      <h4 className="mt-4 mb-2 text-lg font-semibold">Antecedentes Ginecológicos</h4>
      {["menarche_age", "pregnancies", "births", "c_sections", "abortions", "contraceptive_method", "others_gyneco"].map((field) => (
        <div key={field} className="mb-2 col-6">
          <label className="block">{field.replace(/_/g, " ").replace("others gyneco", "Otros")}</label>
          <input type="text" name={field} value={form.gynecological_background[field]} onChange={(e)=> handleChange(e, "gynecological_background")} className="form-control" />
        </div>
      ))}

      <div className="mt-4 col-12">
        <button type="submit" className="btn btn-primary me-2">Guardar</button>
        <button type="button" className="btn btn-secondary" onClick={() => window.history.back()}>Cancelar</button>
      </div>
    </form>
  );
};

export default BackgroundForm;