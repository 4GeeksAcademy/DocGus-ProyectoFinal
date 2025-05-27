import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
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
      const response = await fetch(`${process.env.BACKEND_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "Credenciales inválidas.");
      } else {
        setSuccess("Inicio de sesión exitoso. Redirigiendo...");
        // Aquí podrías guardar el token en localStorage
        setTimeout(() => navigate("/dashboard"), 2000);
      }
    } catch (err) {
      setError("Error en el servidor.");
    }
  };

  const inputStyle = {
    backgroundColor: "#495057",
    color: "#fff",
    border: "1px solid #fff"
  };

  return (
    <div className="container-fluid min-vh-100 d-flex align-items-center justify-content-center px-3" style={{ backgroundColor: "#800000", color: "#fff" }}>
      <div className="card p-4 w-100" style={{ maxWidth: "600px", backgroundColor: "#343a40", border: "1px solid #fff" }}>
        <h2 className="text-center text-white mb-4">Iniciar Sesión</h2>

        <form onSubmit={handleSubmit}>
          <div className="row g-3">
            <div className="col-12">
              <label className="form-label text-white">Correo Electrónico</label>
              <input
                type="email"
                name="email"
                className="form-control"
                style={inputStyle}
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="col-12">
              <label className="form-label text-white">Contraseña</label>
              <input
                type="password"
                name="password"
                className="form-control"
                style={inputStyle}
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          {error && <div className="alert alert-danger mt-4">{error}</div>}
          {success && <div className="alert alert-success mt-4">{success}</div>}

          <div className="text-center mt-4">
            <button type="submit" className="btn btn-light btn-lg text-dark w-100">Entrar</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
