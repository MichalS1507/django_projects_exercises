import React, { useState, useEffect } from "react";
import api from "../api";

function MyBookings() {
    const [bookings, setBookings] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const response = await api.get('bookings/');
                setBookings(response.data);
            } catch (error) {
                console.error("Error fetching bookings:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchBookings();
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
    };

    if (loading) return <div style={{ textAlign: 'center', marginTop: '50px' }}>Loading...</div>;

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h1>My Bookings</h1>
                <button onClick={handleLogout} style={{ padding: '8px 16px' }}>
                    Logout
                </button>
            </div>

            {bookings.length == 0 ? (
                <p>No bookings found.</p>
            ) : (
                <ul style={{ listStyle: "none", padding: 0 }}>
                    {bookings.map(booking => (
                        <li key={booking.id} style={{
                            border: '1px solid #ddd',
                            borderRadius: '8px',
                            padding: '16px',
                            marginBottom: '16px',
                            backgroundColor: '#f9f9f9'
                        }}>
                            <strong style={{ fontSize: '18px' }}>
                                <a href={`/properties/${booking.property_detail?.id}`} style={{ textDecoration: 'none', color: '#007bff' }}>
                                    {booking.property_detail?.title || 'Unknown Property'}
                                </a>
                            </strong><br />
                            <span>Message: {booking.message}</span><br />
                            <span>Booked on: {new Date(booking.created_at).toLocaleDateString()}</span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default MyBookings;