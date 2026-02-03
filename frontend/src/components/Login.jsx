import React, { useState } from 'react';
import api from '../api';

const Login = ({ onLogin }) => {
    const [isRegistering, setIsRegistering] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [successMessage, setSuccessMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccessMessage('');

        if (isRegistering) {
            if (password !== confirmPassword) {
                setError("Passwords do not match");
                return;
            }
        }

        setLoading(true);

        try {
            if (isRegistering) {
                await api.post('register/', { username, password });
                setSuccessMessage("Registration successful! Please login.");
                setIsRegistering(false);
                setPassword('');
                setConfirmPassword('');
            } else {
                const token = btoa(`${username}:${password}`);
                // Test credentials
                await api.get('history/', {
                    headers: { 'Authorization': `Basic ${token}` }
                });
                // If successful, save token and switch view
                localStorage.setItem('auth_token', token);
                onLogin();
            }
        } catch (err) {
            console.error(err);
            if (isRegistering) {
                setError("Registration failed. Username may already be taken.");
            } else {
                setError("Invalid credentials or server error");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            height: '100vh',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            background: 'var(--bg-color)'
        }}>
            <form className="card" onSubmit={handleSubmit} style={{ width: '300px' }}>
                <h2 className="card-title" style={{ textAlign: 'center' }}>
                    {isRegistering ? 'Create Account' : 'Login'}
                </h2>

                {successMessage && (
                    <div style={{ color: 'green', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center' }}>
                        {successMessage}
                    </div>
                )}

                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Username</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        style={{
                            width: '100%',
                            padding: '0.5rem',
                            background: 'var(--bg-secondary)',
                            border: '1px solid var(--border-color)',
                            color: 'var(--text-primary)',
                            borderRadius: '4px'
                        }}
                    />
                </div>

                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{
                            width: '100%',
                            padding: '0.5rem',
                            background: 'var(--bg-secondary)',
                            border: '1px solid var(--border-color)',
                            color: 'var(--text-primary)',
                            borderRadius: '4px'
                        }}
                    />
                </div>

                {isRegistering && (
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>Confirm Password</label>
                        <input
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                            style={{
                                width: '100%',
                                padding: '0.5rem',
                                background: 'var(--bg-secondary)',
                                border: '1px solid var(--border-color)',
                                color: 'var(--text-primary)',
                                borderRadius: '4px'
                            }}
                        />
                    </div>
                )}

                {error && <div style={{ color: 'red', marginBottom: '1rem', fontSize: '0.9rem' }}>{error}</div>}

                <button
                    type="submit"
                    className="btn"
                    style={{ width: '100%', marginBottom: '1rem' }}
                    disabled={loading}
                >
                    {loading ? 'Please wait...' : (isRegistering ? 'Register' : 'Login')}
                </button>

                <div style={{ textAlign: 'center', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                    {isRegistering ? "Already have an account? " : "Don't have an account? "}
                    <span
                        onClick={() => {
                            setIsRegistering(!isRegistering);
                            setError('');
                            setSuccessMessage('');
                        }}
                        style={{ color: 'var(--accent-color)', cursor: 'pointer', textDecoration: 'underline' }}
                    >
                        {isRegistering ? 'Login' : 'Register'}
                    </span>
                </div>
            </form>
        </div>
    );
};

export default Login;
