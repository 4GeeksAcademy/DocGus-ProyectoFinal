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
      const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "Error al iniciar sesión");
      } else {
        localStorage.setItem("token", data.token);
        localStorage.setItem("user", JSON.stringify(data.user));
        setSuccess("Inicio de sesión exitoso. Redirigiendo...");
        setTimeout(() => navigate("/"), 2000);
      }
    } catch (err) {
      setError("Ocurrió un error al conectar con el servidor.");
    }
  };

  return (
    <div className="container-fluid min-vh-100 d-flex align-items-center justify-content-center" style={{ backgroundColor: "#800000", color: "#fff" }}>
      <div className="card p-4 w-100" style={{ maxWidth: "500px", backgroundColor: "#343a40", border: "1px solid #fff" }}>
        <h2 className="text-center text-white mb-4">Iniciar Sesión</h2>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label text-white">Correo Electrónico</label>
            <input
              type="email"
              name="email"
              className="form-control"
              style={{ backgroundColor: "#495057", color: "#fff", border: "1px solid #fff" }}
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label text-white">Contraseña</label>
            <input
              type="password"
              name="password"
              className="form-control"
              style={{ backgroundColor: "#495057", color: "#fff", border: "1px solid #fff" }}
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          {error && <div className="alert alert-danger mt-3">{error}</div>}
          {success && <div className="alert alert-success mt-3">{success}</div>}

          <div className="text-center mt-4">
            <button type="submit" className="btn btn-light btn-lg text-dark w-100">Entrar</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
