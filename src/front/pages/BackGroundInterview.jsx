import { useParams } from "react-router-dom";
import BackgroundForm from "../components/BackGroundForm";

const BackGroundInterview = () => {
    const {medicalFileId} = useParams();
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">ProfesionalDash</h1>
      <p>This is the Profesional file page.</p>
      <BackgroundForm initialData={null} medicalFileId={medicalFileId} />
    </div>
  );
}
export default BackGroundInterview;