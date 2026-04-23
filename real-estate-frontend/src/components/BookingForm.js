import React, { useEffect, useState } from "react";
import api from "../api";
import { useParams, useNavigate } from "react-router-dom";

function BookingForm() {
    const { id } = useParams();
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const [property, setProperty] = useState(null);

    useEffect(() => {
        const fetchProperty = async () => {
            const response = await api.get(`properties/${id}/`);
            setProperty(response.data);
        };
        fetchProperty();
    }, [id]);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
            await api.post('/bookings/', {
                property: id,
                message: message
            });
            navigate('/my-bookings');
        } catch (error) {
            setError('Booking failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
            <h2>Book {property?.title}</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Your message:</label>
                    <textarea
                        value={message}
                        onChange={(event) => setMessage(event.target.value)}
                        rows={4}
                        style={{ width: '100%', padding: '8px', marginTop: '8px' }}
                        placeholder="Write your message to the owner..."
                        required
                    />
                </div>
                <button 
                    type="submit" 
                    disabled={loading}
                    style={{ marginTop: '20px', padding: '10px 20px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px' }}
                >
                    {loading ? 'Submitting...' : 'Submit Booking'}
                </button>
                <a href={`/properties/${id}`} style={{ marginLeft: '10px', padding: '10px 20px', textDecoration: 'none', backgroundColor: '#6c757d', color: 'white', borderRadius: '4px' }}>
                    Cancel
                </a>
            </form>
        </div>
    );
}

export default BookingForm;
