import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
    const navigate = useNavigate();
    const token = localStorage.getItem('access_token');

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/login');
    };

    if (!token) return null;
    
    return (
        <nav style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white'
        }}>
            <div style={{ display: 'flex', gap: '20px' }}>
                <Link to="/properties" style={{ color: 'white', textDecoration: 'none' }}>Properties</Link>
                <Link to="/my-bookings" style={{ color: 'white', textDecoration: 'none' }}>My Bookings</Link>
            </div>
            <button onClick={handleLogout} style={{ padding: '5px 10px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px' }}>
                Logout
            </button>
        </nav>
    );
}

export default Navbar;