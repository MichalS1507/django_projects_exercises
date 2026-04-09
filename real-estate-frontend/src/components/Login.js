import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await api.post('token/', { username, password });

            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);

            navigate('/properties');
        } catch (error) {
            setError('Invalid credentials');
        }
    };

    return (
        <form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: '50px auto' }}>
            <h2>Login</h2>
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
                Login
            </button>
            <p style={{ marginTop: '20px' }}>
                Don't have an account? <a href="/register">Register</a>
            </p>
        </form>
    );
}

export default Login;