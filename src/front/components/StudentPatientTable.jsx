import React, { useEffect, useState } from 'react';

const StudentPatientTable = () => {
    const [patients, setPatients] = useState([]);
    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    useEffect(() => {
        const fetchPatients = async () => {
            try {
                const response = await fetch(`${backendUrl}/api/student/patients`, {
                    method: 'GET',
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem('token')}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setPatients(data);
            } catch (error) {
                console.error('Error fetching patients:', error);
            }
        };
        fetchPatients();
    }, []);

    // 🗑️ Función para eliminar usuario usando el botón "Aprobar"
    const handleDelete = async (userId) => {
        const confirm = window.confirm("¿Estás seguro que deseas eliminar este usuario?");
        if (!confirm) return;

        try {
            const response = await fetch(`${backendUrl}/api/user/${userId}`, {
                method: 'DELETE',
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem('token')}`
                }
            });
            if (!response.ok) {
                throw new Error('No se pudo eliminar el usuario');
            }

            // Actualiza la lista tras eliminar
            setPatients(patients.filter(user => user.id !== userId));
        } catch (error) {
            console.error('Error eliminando usuario:', error);
        }
    };

    return (
        <table className="table table-hover">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Primer Nombre</th>
                    <th scope="col">Segundo Nombre</th>
                    <th scope="col">Primer Apellido</th>
                    <th scope="col">Segundo Apellido</th>
                    <th scope="col">Teléfono</th>
                    <th scope="col">Email</th>
                    <th scope="col">Acciones</th>
                </tr>
            </thead>
            <tbody>
                {patients.map((patient, index) => (
                    <tr key={patient.id}>
                        <th scope="row">{index+1}</th>
                        <td>{`${patient.first_name}`}</td>
                        <td>{`${patient.second_name}`}</td>
                        <td>{`${patient.first_surname}`}</td>
                        <td>{`${patient.second_surname}`}</td>
                        <td>{patient.phone}</td>
                        <td>{patient.email}</td>
                        <td>
                            <button
                                className="btn btn-danger"
                                onClick={() => handleDelete(patient.id)}
                            >
                                Eliminar
                            </button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default StudentPatientTable;
