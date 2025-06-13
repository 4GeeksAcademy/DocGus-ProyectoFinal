import React, { useEffect, useState } from "react";

const initialState = {
  first_name: "",
  second_name: "",
  first_surname: "",
  second_surname: "",
  birth_day: "",
  phone: "",
  sex: "",
  address: "",
};

const FileForm = ({ onChange, onCancel, initialData }) => {
  const [form, setForm] = useState(initialState);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const updatedForm = { ...form, [name]: value };
    setForm(updatedForm);
    onChange?.(updatedForm); // Notifica al componente padre cada vez que cambia algo
  };

  useEffect(() => {
    if (initialData) {
      setForm({
        ...initialState,
        ...initialData,
      });
    }
  }, [initialData]);

  return (
    <div className="row p-4 rounded shadow-md max-w-lg mx-auto" data-bs-theme="dark">
      <h2 className="text-xl font-bold mb-4">Datos Personales del Paciente</h2>

      <div className="mb-2 col-6">
        <label className="block">Primer nombre *</label>
        <input
          name="first_name"
          value={form.first_name}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>

      <div className="mb-2 col-6">
        <label className="block">Segundo nombre</label>
        <input
          name="second_name"
          value={form.second_name}
          onChange={handleChange}
          className="form-control"
        />
      </div>

      <div className="mb-2 col-6">
        <label className="block">Apellido paterno *</label>
        <input
          name="first_surname"
          value={form.first_surname}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>

      <div className="mb-2 col-6">
        <label className="block">Apellido materno</label>
        <input
          name="second_surname"
          value={form.second_surname}
          onChange={handleChange}
          className="form-control"
        />
      </div>

      <div className="mb-2 col-6">
        <label className="block">Sexo *</label>
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
        <label className="block">Fecha de nacimiento *</label>
        <input
          type="date"
          name="birth_day"
          value={form.birth_day}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>

      <div className="mb-2 col-6">
        <label className="block">Dirección *</label>
        <input
          name="address"
          value={form.address}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>

      <div className="mb-2 col-6">
        <label className="block">Teléfono *</label>
        <input
          name="phone"
          value={form.phone}
          onChange={handleChange}
          className="form-control"
          required
        />
      </div>

      {onCancel && (
        <div className="flex gap-2 mt-4">
          <button
            type="button"
            onClick={onCancel}
            className="btn bg-gray-300 text-dark px-4 py-2 rounded"
          >
            Cancelar
          </button>
        </div>
      )}
    </div>
  );
};

export default FileForm;
