import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from './components/Login';
import Register from './components/Register';
import PropertyList from './components/PropertyList';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import BookingForm from './components/BookingForm';
import MyBookings from './components/MyBookings';
import PropertyDetail from './components/PropertyDetail';
import './App.css';

function App() {
    return (
        <BrowserRouter>
        <Navbar />
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/properties" element={
                    <ProtectedRoute>
                        <PropertyList />
                    </ProtectedRoute>
                } />
                <Route path="/properties/:id" element={
                    <ProtectedRoute>
                        <PropertyDetail />
                    </ProtectedRoute>
                } />
                <Route path="/bookings/:id" element={
                    <ProtectedRoute>
                        <BookingForm />
                    </ProtectedRoute>
                } />
                <Route path="/my-bookings/" element={
                    <ProtectedRoute>
                        <MyBookings />
                    </ProtectedRoute>
                } />
                <Route path="/" element={<Navigate to="/properties" />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
