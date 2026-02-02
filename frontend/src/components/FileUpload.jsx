import React, { useState } from 'react';
import api from '../api';

const FileUpload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setError(null);
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Please select a file first");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        try {
            const response = await api.post('upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            onUploadSuccess(response.data);
            setFile(null);
        } catch (err) {
            console.error(err);
            setError("Failed to upload file. Please check the format.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card">
            <h3 className="card-title">Upload Equipment Data</h3>
            <div className="upload-area">
                <div style={{ marginBottom: '1rem' }}>
                    <input
                        type="file"
                        accept=".csv"
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                        id="file-input"
                    />
                    <label htmlFor="file-input" className="btn" style={{ background: 'transparent', border: '1px solid var(--accent-color)', color: 'var(--accent-color)' }}>
                        {file ? file.name : "Choose CSV File"}
                    </label>
                </div>
                {file && (
                    <button className="btn" onClick={handleUpload} disabled={loading}>
                        {loading ? "Processing..." : "Analyze Data"}
                    </button>
                )}
            </div>
            {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}
        </div>
    );
};

export default FileUpload;
