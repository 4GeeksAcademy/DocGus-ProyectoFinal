import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const Register = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const roleFromURL = queryParams.get("rol") || "";


  const [formData, setFormData] = useState({
    first_name: "",
    second_name: "",
    first_surname: "",
    second_surname: "",
    birth_day: "",
    sex: "",
    role: roleFromURL,
    profession: "",
    phone: "",
    email: "",
    password: ""
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
   
    setError("");
    setSuccess("");

    try {
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "Error al registrar");
      } else {
        setSuccess("Registro exitoso. Redirigiendo al inicio de sesión...");
        setTimeout(() => navigate("/login"), 2000);
      }
    } catch (err) {
      setError("Ocurrió un error en el servidor.");
    }
  };

  const inputStyle = {
    backgroundColor: "#495057",
    color: "#fff",
    border: "1px solid #fff"
  };

  return (
    <div className="container-fluid min-vh-100 d-flex align-items-center justify-content-center px-3" style={{ backgroundColor: "#800000", color: "#fff" }}>
      <div className="card p-4 w-100" style={{ maxWidth: "900px", backgroundColor: "#343a40", border: "1px solid #fff" }}>
        <h2 className="text-center text-white mb-4">Registro de {formData.role }</h2>

        <form onSubmit={handleSubmit}>
          <div className="row g-3">
            {[
              { label: "Primer Nombre", name: "first_name", type: "text", required: true },
              { label: "Segundo Nombre", name: "second_name", type: "text"},
              { label: "Primer Apellido", name: "first_surname", type: "text", required: true },
              { label: "Segundo Apellido", name: "second_surname", type: "text" },
              { label: "Fecha de Nacimiento", name: "birth_day", type: "date", required: true },
              { label: "Sexo", name: "sex", type: "select", options: ["masculino", "femenino", "otro"] },
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

          {error && <div className="alert alert-danger mt-4">{error}</div>}
          {success && <div className="alert alert-success mt-4">{success}</div>}

          <div className="text-center mt-4">
            <button type="submit" className="btn btn-light btn-lg text-dark w-100">Registrarme</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
