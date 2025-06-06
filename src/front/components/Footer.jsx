export const Footer = () => (
  <footer
    className="text-center py-4 border-top text-white bg-body-tertiary"
    style={{
      fontFamily: "'Playfair Display', serif",
      fontSize: "0.9rem",
    }}
    data-bs-theme="dark"
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
