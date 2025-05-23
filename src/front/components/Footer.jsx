export const Footer = () => (
  <footer
    className="text-center py-4 border-top text-white"
    style={{
      backgroundColor: "#7A1E2B",
      fontFamily: "'Playfair Display', serif",
      fontSize: "0.9rem",
    }}
  >
    <div className="container">
      <p className="mb-1">
        &copy; {new Date().getFullYear()} SanArte · El Arte de Sanar
      </p>
      <p className="mb-0 text-white-50">
        Contacto: <a href="mailto:info@expedientedigital.com" className="text-white">info@expedientedigital.com</a>
      </p>
      <p className="mb-0 text-white-50">
        Proyecto Full Stack desarrollado con 💻 por estudiantes de <strong>4Geeks Academy</strong>
      </p>
    </div>
  </footer>
);
