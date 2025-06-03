import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';

const AdminDashLayout = () => {
  const location = useLocation();

  const linkStyle = {
    color: "#fff",
    backgroundColor: "#495057",
    marginBottom: "10px",
    border: "1px solid #fff",
    padding: "10px",
    borderRadius: "8px",
    textAlign: "center",
    textDecoration: "none"
  };

  const activeLinkStyle = {
    ...linkStyle,
    backgroundColor: "#6c757d",
    fontWeight: "bold"
  };

  return (
    <div className="container-fluid min-vh-100 d-flex" style={{ backgroundColor: "#800000" }}>
      <div className="d-flex flex-column col-12 col-md-3 p-3" style={{ backgroundColor: "#343a40", borderRight: "1px solid #fff" }}>
        <h4 className="text-white text-center mb-4">Panel</h4>
        <Link to="/admin" style={location.pathname === "/admin" ? activeLinkStyle : linkStyle}>
          Usuarios
        </Link>
        {/* Puedes añadir más links aquí */}
      </div>

      <div className="col-12 col-md-9 p-4">
        <div className="card p-4" style={{ backgroundColor: "#343a40", border: "1px solid #fff", color: "#fff" }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default AdminDashLayout;

