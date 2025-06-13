import { useParams } from "react-router-dom"; // Hook para obtener los parámetros de la URL (ej. medicalFileId)
import React, { useEffect, useState } from "react"; // Importa React y dos hooks: useEffect (efectos secundarios) y useState (estado)
import BackgroundForm from "../components/BackGroundForm"; // Importa el formulario de antecedentes desde componentes

const BackGroundInterview = () => { // Declara el componente funcional BackGroundInterview
  const { medicalFileId } = useParams(); // Extrae el valor de medicalFileId desde la URL (por ejemplo, /entrevista/5)
  const [initialData, setInitialData] = useState(null); // Crea un estado para guardar los datos que se van a cargar

  useEffect(() => { // useEffect se ejecuta cuando el componente se monta o cambia medicalFileId
    const fetchPersonalData = async () => { // Función asíncrona para obtener datos personales desde el backend
      try {
        const response = await fetch( // Realiza la petición GET al backend con el ID de expediente médico
          `${import.meta.env.VITE_BACKEND_URL}/api/personal_data/by_medical_file/${medicalFileId}`, // URL de la API que devuelve datos personales
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`, // Agrega el token de autenticación desde el almacenamiento local
            },
          }
        );
        if (response.ok) { // Si la respuesta fue exitosa (status 200–299)
          const data = await response.json(); // Convierte la respuesta JSON en un objeto JavaScript
          setInitialData(data); // Guarda los datos obtenidos en el estado initialData
        }
      } catch (err) { // Si algo falla durante el fetch (error de red o servidor)
        console.error("Error al obtener datos personales:", err); // Muestra el error en la consola
      }
    };
    if (medicalFileId) fetchPersonalData(); // Llama a la función solo si existe medicalFileId (evita errores)
  }, [medicalFileId]); // El efecto se vuelve a ejecutar si cambia el valor de medicalFileId

  return ( // Lo que se va a mostrar en pantalla
    <div className="container mx-auto p-4"> {/* Contenedor con márgenes automáticos y padding */}
      <h1 className="text-2xl font-bold mb-4">Entrevista</h1> {/* Título principal */}
      <BackgroundForm initialData={initialData} medicalFileId={medicalFileId} /> {/* Renderiza el formulario de antecedentes, pasando los datos obtenidos y el ID */}
    </div>
  );
};

export default BackGroundInterview; // Exporta este componente para que pueda usarse en otras partes de la app