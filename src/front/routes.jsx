// La función principal es definir las rutas del frontend, 
// qué componentes se deben renderizar cuando el usuario navega a una URL específica.



// Import necessary components and functions from react-router-dom.
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router-dom";
import { Layout } from "./pages/Layout";
import { Home } from "./pages/Home";
import { Single } from "./pages/Single";
import { Demo } from "./pages/Demo";
import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx"
import AdminDashLayout from "./pages/AdminDashLayout.jsx";
import UsersTable from "./pages/UsersTable.jsx";
import StudentDash from "./pages/StudentDash.jsx";
import ProfessionalDash from "./pages/ProfessionalDash.jsx";
import PatientDash from "./pages/PatientDash.jsx";
import BackGroundInterview from "./pages/BackGroundInterview.jsx";

export const router = createBrowserRouter(
  createRoutesFromElements(
// La función CreateRoutesFromElements te permite construir elementos de rutas de forma declarativa.
// Crea tus rutas aquí; si quieres mantener la Navbar y el Footer en todas las vistas, agrega tus nuevas rutas dentro de la Route contenedora.
// Root, en cambio, crea una Route hermana; si tienes dudas, ¡pruébalo!
// Nota: ten en cuenta que errorElement será la página predeterminada cuando no se encuentre una ruta; personaliza esa página para hacer tu proyecto más atractivo.
// Nota: Las rutas hijas del elemento Layout reemplazan el componente Outlet con los elementos contenidos en el atributo "element" de estas rutas hijas.

// Ruta Root: Toda la navegación empezará desde aquí.
    <Route path="/" element={<Layout />} errorElement={<h1>Not found!</h1>} >

      {/* Nested Routes: Define sub-routas dentro del componente base Home. */}
      <Route path="/" element={<Home />} />
      <Route path="/single/:theId" element={<Single />} />  {/* Ruta dinamica para elementos solos */}
      <Route path="/demo" element={<Demo />} />
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      {/* adminDashboard */}
      <Route path="/dashboard" element={<AdminDashLayout/>} >
        <Route path="/dashboard/admin" element={<UsersTable/>} />
        <Route path="/dashboard/student" element={<StudentDash/>} />
        <Route path="/dashboard/student/interview/:medicalFileId" element={<BackGroundInterview/>} />
        <Route path="/dashboard/professional" element={<ProfessionalDash/>} />
        <Route path="/dashboard/patient" element={<PatientDash/>} />
      </Route>
    </Route>
  )
);