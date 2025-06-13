// COmponente REgister

// Importa React y el hook useState para manejar estados locales
import React, { useState } from "react";
// Importa hooks de React Router para navegación y acceso a parámetros de URL
import { useLocation, useNavigate } from "react-router-dom";

// Define el componente funcional Register
const Register = () => {
  // Hook para redirigir al usuario programáticamente
  const navigate = useNavigate();
  // Hook para acceder a la información de la URL actual
  const location = useLocation();
  // Crea un objeto con los parámetros de la query string de la URL
  const queryParams = new URLSearchParams(location.search);
  // Extrae el valor del parámetro "rol" de la URL, o usa una cadena vacía si no existe
  const roleFromURL = queryParams.get("rol") || "";

  // Define el estado inicial del formulario con todos los campos necesarios
  const [formData, setFormData] = useState({
    first_name: "",         // Primer nombre
    second_name: "",        // Segundo nombre
    first_surname: "",      // Primer apellido
    second_surname: "",     // Segundo apellido
    birth_day: "",          // Fecha de nacimiento
    sex: "",                // Sexo
    role: roleFromURL,      // Rol recibido por URL
    profession: "",         // Profesión (solo si es profesional)
    phone: "",              // Teléfono
    email: "",              // Correo electrónico
    password: ""            // Contraseña
  });

  // Estado para mensajes de error
  const [error, setError] = useState("");
  // Estado para mensaje de éxito
  const [success, setSuccess] = useState("");

  // Maneja los cambios en los inputs del formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    // Actualiza el estado de formData con el nuevo valor
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Maneja el envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault(); // Previene el comportamiento por defecto del formulario
    
    setError("");   // Limpia errores previos
    setSuccess(""); // Limpia mensajes previos

    try {
      // Envía los datos al backend (URL tomada del archivo .env)
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/register`, {
        method: "POST", // Método HTTP POST
        headers: { "Content-Type": "application/json" }, // Indica que se envía JSON
        body: JSON.stringify(formData) // Convierte los datos del formulario en JSON
      });

      // Convierte la respuesta en objeto JS
      const data = await response.json();

      if (!response.ok) {
        // Si la respuesta tiene error, muestra mensaje de error
        setError(data.message || "Error al registrar");
      } else {
        // Si todo sale bien, muestra mensaje de éxito
        setSuccess("Registro exitoso. Redirigiendo al inicio de sesión...");
        // Redirige al login después de 2 segundos
        setTimeout(() => navigate("/login"), 2000);
      }
    } catch (err) {
      // Si ocurre un error de red o servidor
      setError("Ocurrió un error en el servidor.");
    }
  };

  // Estilo personalizado para los inputs (fondo oscuro con texto blanco)
  const inputStyle = {
    backgroundColor: "#495057",
    color: "#fff",
    border: "1px solid #fff"
  };

  // Render del componente
  return (
    <div className="container-fluid min-vh-100 d-flex align-items-center justify-content-center px-3" style={{ backgroundColor: "#800000", color: "#fff" }}>
      <div className="card p-4 w-100" style={{ maxWidth: "900px", backgroundColor: "#343a40", border: "1px solid #fff" }}>
        {/* Título que incluye el rol dinámicamente */}
        <h2 className="text-center text-white mb-4">Registro de {formData.role }</h2>

        {/* Formulario de registro */}
        <form onSubmit={handleSubmit}>
          <div className="row g-3">
            {/* Define la lista de campos del formulario */}
            {[
              { label: "Primer Nombre", name: "first_name", type: "text", required: true },
              { label: "Segundo Nombre", name: "second_name", type: "text"},
              { label: "Primer Apellido", name: "first_surname", type: "text", required: true },
              { label: "Segundo Apellido", name: "second_surname", type: "text" },
              { label: "Fecha de Nacimiento", name: "birth_day", type: "date", required: true },
              { label: "Sexo", name: "sex", type: "select", options: ["masculino", "femenino", "otro"] },
              // Si el rol es profesional, se incluye el campo profesión
              ...(roleFromURL == "profesional" ? [
                { label: "Profesión", name: "profession", type: "text", required: true },
              ]: []),
              { label: "Teléfono", name: "phone", type: "tel" },
              { label: "Correo Electrónico", name: "email", type: "email", required: true },
              { label: "Contraseña", name: "password", type: "password", required: true }
            ].map(field => (
              <div className="col-12 col-md-6 col-lg-4" key={field.name}>
                <label className="form-label text-white">{field.label}</label>
                {field.type === "select" ? (
                  // Si es un campo tipo select (sexo)
                  <select
                    name={field.name}
                    className="form-select"
                    style={inputStyle}
                    value={formData[field.name]}
                    onChange={handleChange}
                  >
                    <option value="">Selecciona</option>
                    {field.options.map(opt => (
                      <option key={opt} value={opt}>{opt}</option>   
                    ))}
                  </select>
                ) : (
                  // Si es un campo tipo input
                  <input
                    type={field.type}
                    name={field.name}
                    className="form-control"
                    style={inputStyle}
                    value={formData[field.name]}
                    onChange={handleChange}
                    readOnly={field.readOnly}
                    required={field.required}
                  />
                )}
              </div>
            ))}
          </div>

          {/* Muestra alertas si hay error o éxito */}
          {error && <div className="alert alert-danger mt-4">{error}</div>}
          {success && <div className="alert alert-success mt-4">{success}</div>}

          {/* Botón de envío */}
          <div className="text-center mt-4">
            <button type="submit" className="btn btn-light btn-lg text-dark w-100">Registrarme</button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Exporta el componente para poder usarlo en otras partes
export default Register;
