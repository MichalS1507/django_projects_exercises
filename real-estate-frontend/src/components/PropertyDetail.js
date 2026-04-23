import React, { useEffect, useState } from "react";
import api from "../api";
import { useParams } from "react-router-dom";

function PropertyDetail() {
    const { id } = useParams();
    const [property, setProperty] = useState();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProperty = async () => {
            try {
                const response = await api.get(`properties/${id}/`);
                setProperty(response.data);
            } catch (error) {
                console.error("Error fetching property:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchProperty();
    }, [id]);

    if (loading) return <div style={{ textAlign: 'center', marginTop: '50px' }}>Loading...</div>;
    if (!property) return <div>Property not found.</div>;

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <h1>{property.title}</h1>
                <a href="/properties" style={{ padding: '8px 16px', textDecoration: 'none', color: 'white', backgroundColor: '#007bff', borderRadius: '4px' }}>
                    Back to Properties
                </a>
            </div>

            <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '20px', marginTop: '20px', backgroundColor: '#f9f9f9' }}>
                <p><strong>Price:</strong> {property.price}€</p>
                <p><strong>City:</strong> {property.city}</p>
                <p><strong>Address:</strong> {property.address}</p>
                <p><strong>Zip code:</strong> {property.zip_code}</p>
                <p><strong>Property type:</strong> {property.property_type}</p>
                <p><strong>Offer type:</strong> {property.offer_type}</p>
                <p><strong>Bedrooms:</strong> {property.bedrooms}</p>
                <p><strong>Bathrooms:</strong> {property.bathrooms}</p>
                <p><strong>Area:</strong> {property.area} m²</p>
                <p><strong>Description:</strong> {property.description}</p>
            </div>

            <a href={`/bookings/${property.id}`} 
                style={{ 
                    display: 'inline-block', 
                    marginTop: '20px', 
                    padding: '10px 20px', 
                    textDecoration: 'none', 
                    color: 'white', 
                    backgroundColor: '#28a745', 
                    borderRadius: '4px' 
                }}>
                    Book this Property
             </a>
        </div>
    );
}

export default PropertyDetail;