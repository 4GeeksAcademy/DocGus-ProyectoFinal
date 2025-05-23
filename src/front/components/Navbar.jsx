import { Link } from "react-router-dom";
import logoSanarte from "../assets/img/Sanarte pre 1.png";

export const Navbar = () => {
  return (
    <nav
      className="navbar navbar-expand-lg navbar-dark shadow-sm"
      style={{ backgroundColor: "#7A1E2B", fontFamily: "'Playfair Display', serif" }}
    >
      <div className="container">
        {/* Logo y nombre */}
        <Link to="/" className="navbar-brand d-flex align-items-center">
          <img
            src={logoSanarte}
            alt="SanArte Logo"
            style={{ height: "40px", marginRight: "10px" }}
          />
          <span className="fw-bold" style={{ fontSize: "1.2rem" }}>SanArte</span>
        </Link>

        {/* Botón/links a la derecha */}
        <div className="d-flex">
          <Link to="/demo" className="btn btn-outline-light">
            Ver Demo
          </Link>
        </div>
      </div>
    </nav>
  );
};
