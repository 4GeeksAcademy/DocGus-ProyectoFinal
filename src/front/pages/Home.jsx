import React from "react";
import { Link } from "react-router-dom";

export const Home = () => {
  return (
    <div>
    <div className="container-fluid min-vh-100 d-flex flex-column" style={{ backgroundColor: "#800000", color: "#fff" }}>
      {/* Header */}
      <header className="py-4 border-bottom border-light">
        <div className="container text-center">
          <h1 className="display-5 text-white">Ecosistema Digital para la Gestión de Expedientes Médicos</h1>
          <p className="lead mt-3 text-white">
            Una plataforma educativa y clínica que conecta estudiantes, profesionales y pacientes a través de la supervisión ética y la colaboración interdisciplinaria.
          </p>
        </div>
      </header>

      {/* Main Section */}
      <main className="flex-grow-1 container py-5">
        <div className="row row-cols-1 row-cols-md-3 g-4">
          {/* Módulo Académico */}
          <div className="col">
            <div className="card h-100 text-white" style={{ backgroundColor: "#343a40", border: "1px solid #fff" }}>
              <div className="card-body">
                <h5 className="card-title text-white">Módulo Académico</h5>
                <p className="card-text">
                  Profesores y estudiantes gestionan expedientes clínicos supervisados, asegurando ética y aprendizaje práctico.
                </p>
              </div>
            </div>
          </div>

          {/* Módulo Profesional */}
          <div className="col">
            <div className="card h-100 text-white" style={{ backgroundColor: "#343a40", border: "1px solid #fff" }}>
              <div className="card-body">
                <h5 className="card-title text-white">Módulo Profesional</h5>
                <p className="card-text">
                  Profesionales certificados gestionan pacientes y procesos administrativos con herramientas clínicas y logísticas.
                </p>
              </div>
            </div>
          </div>

          {/* Módulo Multidisciplinario */}
          <div className="col">
            <div className="card h-100 text-white" style={{ backgroundColor: "#343a40", border: "1px solid #fff" }}>
              <div className="card-body">
                <h5 className="card-title text-white">Módulo Multidisciplinario</h5>
                <p className="card-text">
                  Pacientes colaboran con profesionales de distintas disciplinas en tiempo real.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Botones de registro */}
        <div className="text-center mt-5">
          <div className="d-flex justify-content-center flex-wrap gap-3">
            <Link to="/register?rol=profesional" className="btn btn-light btn-lg text-dark">
              Registro Profesional
            </Link>
            <Link to="/register?rol=estudiante" className="btn btn-light btn-lg text-dark">
              Registro Estudiante
            </Link>
            <Link to="/register?rol=paciente" className="btn btn-light btn-lg text-dark">
              Registro Paciente
            </Link>
          </div>
        </div>

        {/* Botón de login debajo y centrado */}
        <div className="text-center mt-4">
          <Link to="/login" className="btn btn-light btn-lg text-dark">
            Iniciar Sesión
          </Link>
        </div>
      </main>
    </div>
    </div>
  );
};


