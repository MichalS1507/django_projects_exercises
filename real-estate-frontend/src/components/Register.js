import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            await api.post('register/', { username, password });

            navigate('/login');
        } catch (error) {
            setError('Registration failed. Username may already exist.');
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: '50px auto' }}>
            <h2>Register</h2>
            {error && <p style={{color: 'red'}}>{error}</p>}
            <div>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    style={{ width: '100%', padding: '8px', margin: '8px 0' }}
                />
            </div>
            <div>
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    style={{ width: '100%', padding: '8px', margin: '8px 0' }}
                />
            </div>
            <button type="submit" style={{ padding: '10px 20px', marginTop: '10px' }}>
                Register
            </button>
            <p style={{ marginTop: '20px' }}>
                Already have an account? <a href="/login">Login</a>
            </p>
        </form>
    );
}

export default Register;