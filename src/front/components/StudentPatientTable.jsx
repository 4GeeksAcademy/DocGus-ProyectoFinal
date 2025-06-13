// Tabla Para el Dashboard de Estudiantes donde se muestran los pacientes que no tienen expediente


// Importa el componente Button de Bootstrap (aunque no se usa en el componente)
import { Button } from 'bootstrap';

// Importa React y los hooks useEffect y useState
import React, { useEffect, useState } from 'react';

// Importa el componente Link para navegación interna con React Router
import { Link } from 'react-router-dom';

// Define el componente funcional StudentPatientTable
const StudentPatientTable = () => {
    // Declara el estado 'patients', inicialmente como arreglo vacío
    const [patients, setPatients] = useState([]);

    // Obtiene la URL del backend desde las variables de entorno
    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    // Hook que se ejecuta al montar el componente (equivalente a componentDidMount)
    useEffect(() => {
        // Función asíncrona para obtener la lista de pacientes del backend
        const fetchPatients = async () => {
            try {
                // Realiza una solicitud GET a la API de pacientes
                const response = await fetch(`${backendUrl}/api/student/patients`, {
                    method: 'GET',
                    headers: {
                        // Añade el token de autenticación desde localStorage
                        "Authorization": `Bearer ${localStorage.getItem('token')}`
                    }
                });

                // Si la respuesta no es exitosa, lanza un error
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                // Convierte la respuesta en JSON
                const data = await response.json();

                // Actualiza el estado con los datos recibidos
                setPatients(data);
            } catch (error) {
                // Muestra en consola si ocurre un error al obtener los datos
                console.error('Error fetching patients:', error);
            }
        };

        // Llama a la función para obtener pacientes
        fetchPatients();
    }, []); // [] significa que se ejecuta solo una vez, al montar

    // 🗑️ Función que elimina un paciente al hacer clic en "Eliminar"
    const handleDelete = async (userId) => {
        // Pide confirmación al usuario antes de eliminar
        const confirm = window.confirm("¿Estás seguro que deseas eliminar este usuario?");
        if (!confirm) return;

        try {
            // Solicitud DELETE al backend con el ID del usuario
            const response = await fetch(`${backendUrl}/api/user/${userId}`, {
                method: 'DELETE',
                headers: {
                    // Incluye el token de autenticación
                    "Authorization": `Bearer ${localStorage.getItem('token')}`
                }
            });

            // Verifica si la respuesta es válida
            if (!response.ok) {
                throw new Error('No se pudo eliminar el usuario');
            }

            // Filtra al paciente eliminado y actualiza el estado
            setPatients(patients.filter(user => user.id !== userId));
        } catch (error) {
            // Muestra un error si la eliminación falla
            console.error('Error eliminando usuario:', error);
        }
    };

    // JSX que renderiza la tabla con los pacientes
    return (
        <>
        <table className="table table-hover"> {/* Tabla con estilo Bootstrap */}
            <thead>
                <tr>
                    {/* Encabezados de la tabla */}
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
                {/* Mapea el arreglo de pacientes para generar una fila por cada uno */}
                {patients.map((patient, index) => (
                    <tr key={patient.id}> {/* La clave única es el id del paciente */}
                        <th scope="row">{index + 1}</th> {/* Número de fila */}
                        <td>{`${patient.first_name}`}</td> {/* Primer nombre */}
                        <td>{`${patient.second_name}`}</td> {/* Segundo nombre */}
                        <td>{`${patient.first_surname}`}</td> {/* Primer apellido */}
                        <td>{`${patient.second_surname}`}</td> {/* Segundo apellido */}
                        <td>{patient.phone}</td> {/* Teléfono */}
                        <td>{patient.email}</td> {/* Correo electrónico */}
                        <td>
                            {/* Botón que lleva al formulario para completar entrevista */}
                            <Link to={`/dashboard/student/interview/${patient.id}`}
                                className="btn btn-success mx-3" >
                                Completar
                            </Link>

                            {/* Botón para eliminar al paciente */}
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
        </>
    );
};

// Exporta el componente para que pueda usarse en otros archivos
export default StudentPatientTable;
