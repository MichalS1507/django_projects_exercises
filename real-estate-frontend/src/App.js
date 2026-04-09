import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from './components/Login';
import Register from './components/Register';
import PropertyList from './components/PropertyList';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                <Route path="/properties" element={
                    <ProtectedRoute>
                        <PropertyList />
                    </ProtectedRoute>
                } />

                <Route path="/" element={<Navigate to="/properties" />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
