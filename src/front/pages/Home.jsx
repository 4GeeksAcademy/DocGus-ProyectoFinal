import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faUserMd,
  faUserGraduate,
  faPeopleArrows,
  faHeart,
  faLaptopMedical,
  faHandsHelping
} from "@fortawesome/free-solid-svg-icons";

export const Home = () => {
  return (
    <div
      className="container-fluid min-vh-100 d-flex flex-column text-white"
      style={{
        background: "linear-gradient(135deg, #7A1E2B 0%,rgb(0, 0, 0) 100%)",
        fontFamily: "'Playfair Display', serif",
      }}
    >
      {/* Header */}
      <header className="py-5 border-bottom border-light text-center">
        <div className="container">
          <h1 className="display-4 fw-bold">SanArte · El Arte de Sanar</h1>
          <p className="lead mt-3 text-white-50">
            Un espacio donde lo clínico, lo académico y lo humano convergen con propósito.
          </p>
        </div>
      </header>

      {/* Main Section */}
      <main className="flex-grow-1 container py-5">
        {/* Módulos */}
        <div className="row row-cols-1 row-cols-md-3 g-4">
          {[
            {
              icon: faUserGraduate,
              title: "Entorno Académico",
              text: "Aprendizaje con expedientes reales y supervisión constante.",
            },
            {
              icon: faUserMd,
              title: "Gestión Profesional",
              text: "Herramientas clínicas para optimizar atención y seguimiento.",
            },
            {
              icon: faPeopleArrows,
              title: "Trabajo Interdisciplinario",
              text: "Un enfoque integral entre profesionales y pacientes.",
            },
          ].map((item, i) => (
            <div className="col" key={i}>
              <div
                className="card h-100 border-0 shadow"
                style={{
                  backgroundColor: "rgba(255,255,255,0.05)",
                  backdropFilter: "blur(4px)",
                  color: "#FFFFFF",
                }}
              >
                <div className="card-body text-center">
                  <FontAwesomeIcon icon={item.icon} size="2x" className="mb-3" />
                  <h5 className="card-title fw-bold">{item.title}</h5>
                  <p className="card-text">{item.text}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Beneficios */}
        <section className="mt-5">
          <h2 className="text-center mb-4 fw-bold">Beneficios de SanArte</h2>
          <div className="row text-center">
            <div className="col-md-4 mb-4">
              <FontAwesomeIcon icon={faLaptopMedical} size="2x" className="mb-3" />
              <h5>Accesibilidad Total</h5>
              <p className="text-white-50">
                Información clínica disponible desde cualquier dispositivo.
              </p>
            </div>
            <div className="col-md-4 mb-4">
              <FontAwesomeIcon icon={faHeart} size="2x" className="mb-3" />
              <h5>Cuidado Humano</h5>
              <p className="text-white-50">
                El paciente es protagonista de un proceso ético y empático.
              </p>
            </div>
            <div className="col-md-4 mb-4">
              <FontAwesomeIcon icon={faHandsHelping} size="2x" className="mb-3" />
              <h5>Red Colaborativa</h5>
              <p className="text-white-50">
                Profesionales y estudiantes conectados por un mismo propósito.
              </p>
            </div>
          </div>
        </section>

        {/* Testimonios */}
        <section className="mt-5">
          <h2 className="text-center mb-4 fw-bold">Voces que Sanan</h2>
          <div className="row g-4">
            {[
              {
                quote: "Una herramienta humana que me hizo sentir acompañada en todo momento.",
                author: "— Paciente",
              },
              {
                quote: "SanArte me ayudó a integrar la práctica real con el aprendizaje académico.",
                author: "— Estudiante de Terapia",
              },
              {
                quote: "Por fin una plataforma hecha desde la vocación, no solo desde la tecnología.",
                author: "— Profesional en salud",
              },
            ].map((t, i) => (
              <div className="col-md-4" key={i}>
                <div
                  className="card bg-transparent text-white border-light h-100 shadow-sm"
                  style={{ border: "1px solid rgba(255,255,255,0.2)" }}
                >
                  <div className="card-body">
                    <p className="card-text">“{t.quote}”</p>
                    <h6 className="card-subtitle mt-3 text-white-50">{t.author}</h6>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Video */}
        <section className="mt-5 text-center">
          <h2 className="mb-4 fw-bold">Descubre SanArte en acción</h2>
          <div className="ratio ratio-16x9">
<iframe width="560" height="315" src="https://www.youtube.com/embed/Hac-5Z_1aVA?si=K51vqjvC4KSJ_4hN" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
          </div>
        </section>

        {/* Botones de registro */}
        <div className="text-center mt-5">
          <h4 className="mb-4">Crea tu cuenta</h4>
          <div className="d-flex justify-content-center flex-wrap gap-3">
            <Link to="/register?rol=profesional" className="btn btn-outline-light btn-lg">
              Profesional
            </Link>
            <Link to="/register?rol=estudiante" className="btn btn-outline-light btn-lg">
              Estudiante
            </Link>
            <Link to="/register?rol=paciente" className="btn btn-outline-light btn-lg">
              Paciente
            </Link>
          </div>
        </div>

        {/* Botón de login */}
        <div className="text-center mt-4">
          <p className="text-white-50 mb-2">¿Ya tienes una cuenta?</p>
          <Link to="/login" className="btn btn-light btn-lg text-dark">
            Iniciar Sesión
          </Link>
        </div>
      </main>
    </div>
  );
};

export default Home;
