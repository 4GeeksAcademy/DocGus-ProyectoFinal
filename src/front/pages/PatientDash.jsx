import React, { useEffect, useState } from "react";
import FileForm from "../components/FileForm";

// Función auxiliar para decodificar el JWT y obtener el user_id
function getUserIdFromToken() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.sub || payload.user_id || payload.id; // Ajusta según cómo guardes el id en el JWT
  } catch {
    return null;
  }
}

const PatientDash = () => {
  const [personalData, setPersonalData] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
   
    fetch(import.meta.env.VITE_BACKEND_URL+`/api/personal_data`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) setError(data.error);
        else setPersonalData(data);
      })
      .catch(() => setError("No se pudieron cargar los datos personales."));
  }, []);

  if (error) return <div className="text-red-600">{error}</div>;
  if (!personalData) return <div>Cargando datos personales...</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Mis datos personales</h1>
      <FileForm initialData={personalData} readOnly={true} />
    </div>
  );
};

export default PatientDash;