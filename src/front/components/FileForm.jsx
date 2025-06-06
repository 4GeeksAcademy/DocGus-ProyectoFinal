import React, { useEffect, useState } from "react";

const initialState = {
  first_name: "",
  second_name: "",
  first_surname: "",
  second_surname: "",
  birth_day: "",
  phone: "",
};

const FileForm = ({ onSubmit, onCancel, initialData }) => {
  const [form, setForm] = useState(initialState);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Validación simple
    if (!form.first_name || !form.first_surname || !form.birth_day || !form.phone) {
      setError("Por favor, completa todos los campos obligatorios.");
      return;
    }
    setError("");
    onSubmit(form);
  };
  useEffect(() => {
    console.log("initialData", initialData);
    if (initialData) {
      setForm({
        first_name: initialData.first_name || "",
        second_name: initialData.second_name || "",
        first_surname: initialData.first_surname || "",
        second_surname: initialData.second_surname || "",
        birth_day: initialData.birth_day || "",
        phone: initialData.phone || "",
        sex: initialData.sex || "",
        address: initialData.address || "",
      });
    }
  }, [initialData]);
  return (
    <form onSubmit={handleSubmit} className="row p-4 rounded shadow-md max-w-lg mx-auto" data-bs-theme="dark">
      <h2 className="text-xl font-bold mb-4">Datos Personales del Paciente</h2>
      <div className="mb-2 col-6">
        <label className="block">Primer nombre * </label>
        <input
          name="first_name"
          value={form.first_name}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
      
      <div className="mb-2 col-6">
        <label className="block">Segundo nombre </label>
        <input
          name="second_name"
          value={form.second_name}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
<br />
      <div className="mb-2 col-6">
        <label className="block">Apellido paterno * </label>
        <input
          name="first_surname"
          value={form.first_surname}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
      <div className="mb-2 col-6">
        <label className="block">Apellido materno </label>
        <input
          name="second_surname"
          value={form.second_surname}
          onChange={handleChange}
          className="form-control"
        />
      </div>
      <br />
      <div className="mb-2 col-6">
        <label className="block">Sexo * </label>
        <select
          name="sex"
          value={form.sex}
          onChange={handleChange}
          className="form-select"
          required
        >
          <option value="">Selecciona</option>
          <option value="femenino">Femenino</option>
          <option value="masculino">Masculino</option>
          <option value="otro">Otro</option>
        </select>
      </div>
      <div className="mb-2 col-6">
        <label className="block">Fecha de nacimiento * </label>
        <input
          type="date"
          name="birth_day"
          value={form.birth_day}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
      <br />
      <div className="mb-2 col-6">
        <label className="block">Dirección * </label>
        <input
          name="address"
          value={form.address}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
      <div className="mb-2 col-6">
        <label className="block">Teléfono * </label>
        <input
          name="phone"
          value={form.phone}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>
      {error && <div className="text-red-600 mb-2">{error}</div>}
      <div className="flex gap-2 mt-4">
        <button type="submit" className="btn btn-success">Guardar</button>
        {onCancel && (
          <button type="button" onClick={onCancel} className="btn bg-gray-300 text-dark px-4 py-2 rounded">
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
};

export default FileForm;