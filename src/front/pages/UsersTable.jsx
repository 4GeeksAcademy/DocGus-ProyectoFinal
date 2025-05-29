import React, { useEffect, useState } from 'react';

const UsersTable = () => {
    const [users, setUsers] = useState([]);
    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await fetch(`${backendUrl}/api/users`, {
                    method: 'GET',
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem('token')}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setUsers(data);
            } catch (error) {
                console.error('Error fetching users:', error);
            }
        };
        fetchUsers();
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
            setUsers(users.filter(user => user.id !== userId));
        } catch (error) {
            console.error('Error eliminando usuario:', error);
        }
    };

    return (
        <table className="table table-hover">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Nombre Completo</th>
                    <th scope="col">Rol</th>
                    <th scope="col">Status</th>
                    <th scope="col">Acciones</th>
                </tr>
            </thead>
            <tbody>
                {users.map((user) => (
                    <tr key={user.id}>
                        <th scope="row">{user.id}</th>
                        <td>{`${user.names} ${user.first_surname} ${user.second_surname}`}</td>
                        <td>{user.role}</td>
                        <td>{user.status}</td>
                        <td>
                            <button
                                className="btn btn-danger"
                                onClick={() => handleDelete(user.id)}
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

export default UsersTable;
