import React, { useEffect, useState } from 'react';
import api from '../api';

const History = ({ onSelectHistory }) => {
    const [history, setHistory] = useState([]);

    const fetchHistory = async () => {
        try {
            const response = await api.get('history/');
            setHistory(response.data);
        } catch (error) {
            console.error("Failed to fetch history", error);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    // Also expose a way to refresh history from parent if needed, 
    // but for now we just load on mount. 
    // We can export the refresh function if we used context, 
    // but here we might just rely on parent passing a "refresh trigger".

    return (
        <div className="card" style={{ marginTop: 'auto' }}>
            <h3 className="card-title">Recent Uploads</h3>
            {history.length === 0 ? (
                <p className="subtitle">No history yet.</p>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {history.map((item) => (
                        <div key={item.id} className="history-item" onClick={() => onSelectHistory(item)}>
                            <div style={{ fontWeight: 500 }}>ID: {item.id}</div>
                            <div className="history-date">{new Date(item.uploaded_at).toLocaleString()}</div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default History;
