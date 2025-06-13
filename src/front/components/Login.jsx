import React, { useState } from "react";                  // Importa React y el hook useState para manejar estados locales
import { useNavigate } from "react-router-dom";           // Importa el hook useNavigate para redirección programática entre rutas

const Login = () => {                                     // Define el componente funcional Login
  const navigate = useNavigate();                         // Inicializa la función de navegación

  const [formData, setFormData] = useState({              // Estado para guardar los datos del formulario
    email: "",                                            // Campo email, inicialmente vacío
    password: ""                                          // Campo password, inicialmente vacío
  });

  const [error, setError] = useState("");                 // Estado para mostrar mensajes de error
  const [success, setSuccess] = useState("");             // Estado para mostrar mensaje de éxito

  const handleChange = (e) => {                           // Función que se ejecuta al cambiar un input del formulario
    const { name, value } = e.target;                     // Extrae el nombre y valor del input que disparó el evento
    setFormData(prev => ({ ...prev, [name]: value }));    // Actualiza el estado formData manteniendo los demás campos
  };

  const handleSubmit = async (e) => {                     // Función que se ejecuta al enviar el formulario
    e.preventDefault();                                   // Previene la recarga de la página
    setError("");                                         // Limpia errores anteriores
    setSuccess("");                                       // Limpia mensajes de éxito anteriores

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/login`, {
        method: "POST",                                   // Método POST para enviar credenciales
        headers: { "Content-Type": "application/json" },  // Indica que se envían datos en formato JSON
        body: JSON.stringify(formData)                    // Convierte formData en una cadena JSON
      });

      const data = await response.json();                 // Parsea la respuesta como JSON

      if (!response.ok) {                                 // Si la respuesta no fue exitosa
        setError(data.message || "Error al iniciar sesión");  // Muestra mensaje de error
      } else {                                            // Si la respuesta fue exitosa
        localStorage.setItem("token", data.token);        // Guarda el token en el almacenamiento local
        localStorage.setItem("user", JSON.stringify(data.user)); // Guarda el usuario como string
        console.log("Usuario:", data.user);               // Muestra en consola el usuario autenticado
        setSuccess("Inicio de sesión exitoso. Redirigiendo..."); // Muestra mensaje de éxito

        setTimeout(() => {                                // Espera 2 segundos antes de redirigir
          if (data.user.role === "administrador") {
            navigate("/dashboard/admin");                 // Redirige al dashboard del administrador
          }
          else if (data.user.role === "estudiante") {
            navigate("/dashboard/student");               // Redirige al dashboard del estudiante
          } 
          else if (data.user.role === "paciente") {
            navigate("/dashboard/patient");               // Redirige al dashboard del paciente
          } 
          else if (data.user.role === "profesional") {
            navigate("/dashboard/professional");          // Redirige al dashboard del profesional
          } 
          else {
            navigate("/");                                // Redirige al inicio si no hay coincidencia
          }
        }, 2000);
      }
    } catch (err) {
      setError("Ocurrió un error al conectar con el servidor."); // Muestra error si falla la petición
    }
  };

  return (
    <div className="container-fluid min-vh-100 d-flex align-items-center justify-content-center"
         style={{ backgroundColor: "#800000", color: "#fff" }}>   {/* Contenedor de fondo completo con estilo */}
      <div className="card p-4 w-100"
           style={{ maxWidth: "500px", backgroundColor: "#343a40", border: "1px solid #fff" }}> {/* Tarjeta centrada */}
        <h2 className="text-center text-white mb-4">Iniciar Sesión</h2> {/* Título del formulario */}

        <form onSubmit={handleSubmit}>                    {/* Manejador de envío del formulario */}
          <div className="mb-3">
            <label className="form-label text-white">Correo Electrónico</label>
            <input
              type="email"                                // Input tipo email
              name="email"                                // Nombre del campo
              className="form-control"                    // Clase de Bootstrap
              style={{ backgroundColor: "#495057", color: "#fff", border: "1px solid #fff" }}
              value={formData.email}                      // Valor controlado desde el estado
              onChange={handleChange}                     // Actualiza el estado al escribir
              required                                     // Campo obligatorio
            />
          </div>
          <div className="mb-3">
            <label className="form-label text-white">Contraseña</label>
            <input
              type="password"                             // Input tipo password
              name="password"                             // Nombre del campo
              className="form-control"
              style={{ backgroundColor: "#495057", color: "#fff", border: "1px solid #fff" }}
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          {error && <div className="alert alert-danger mt-3">{error}</div>}       {/* Muestra error si existe */}
          {success && <div className="alert alert-success mt-3">{success}</div>}  {/* Muestra éxito si existe */}

          <div className="text-center mt-4">
            <button type="submit" className="btn btn-light btn-lg text-dark w-100">Entrar</button> {/* Botón de envío */}
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login; // Exporta el componente para su uso
