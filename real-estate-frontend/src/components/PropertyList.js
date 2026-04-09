import React, { useState, useEffect } from "react";
import api from "../api";

function PropertyList() {
    const [properties, setProperties] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProperties = async () => {
            try {
                const response = await api.get('properties/');
                setProperties(response.data);
            } catch (error) {
                console.error("Error fetching properties:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchProperties();
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
                <h1>Properties</h1>
                <button onClick={handleLogout} style={{ padding: '8px 16px' }}>
                    Logout
                </button>
            </div>

            {properties.length == 0 ? (
                <p>No properties found.</p>
            ) : (
                <ul style={{ listStyle: "none", padding: 0 }}>
                    {properties.map(property => (
                        <li key={property.id} style={{
                            border: '1px solid #ddd',
                            borderRadius: '8px',
                            padding: '16px',
                            marginBottom: '16px',
                            backgroundColor: '#f9f9f9'
                        }}>
                            <strong style={{ fontSize: '18px' }}>{property.title}</strong><br />
                            <span>Price: {property.price}€</span><br />
                            <span>City: {property.city}</span><br />
                            <span>Type: {property.offer_type}</span><br />
                            <span>Bedrooms: {property.bedrooms}</span><br />
                            <span>Area: {property.area} m²</span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default PropertyList;