// Importa el hook `useParams` de React Router, que permite acceder a los parámetros de la URL.
import { useParams } from "react-router-dom";



// Importa el componente `BackgroundForm` desde el directorio de componentes.
import BackgroundForm from "../components/BackGroundForm";



// Define un componente funcional llamado `BackGroundInterview`
const BackGroundInterview = () => {
    const {medicalFileId} = useParams();  // Extrae el parámetro `medicalFileId` desde la URL usando `useParams`.



// Retorna el JSX que se renderiza en pantalla.
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">ProfesionalDash</h1>
      <p>This is the Profesional file page.</p>
      <BackgroundForm initialData={null} medicalFileId={medicalFileId} />
    </div>
  );
}



// Exporta el componente para que pueda ser utilizado en otras partes de la app.
export default BackGroundInterview;