import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import History from './components/History';
import Login from './components/Login';
import api from './api';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeData, setActiveData] = useState(null);
  const [activeDocumentId, setActiveDocumentId] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [refreshHistory, setRefreshHistory] = useState(0);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    setIsAuthenticated(false);
    setActiveData(null);
  };

  const handleUploadSuccess = (response) => {
    setActiveData(response.analysis);
    setActiveDocumentId(response.document_id);
    setRefreshHistory(prev => prev + 1); // Trigger history refresh
  };

  const handleHistorySelect = (item) => {
    if (item.summary) {
      setActiveData(item.summary);
      setActiveDocumentId(item.id);
    }
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="logo">
          ⚡ EquipmentViz
        </div>
        <div className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
          Dashboard
        </div>
        <div className="nav-item" onClick={handleLogout} style={{ marginTop: 'auto', borderTop: '1px solid var(--border-color)' }}>
          Logout
        </div>

        {/* History Component embedded in sidebar */}
        <History key={refreshHistory} onSelectHistory={handleHistorySelect} />
      </aside>

      <main className="main-content">
        <div className="header">
          <h1 className="title">Analyze Equipment Parameters</h1>
          <p className="subtitle">Upload CSV data to generate insights.</p>
        </div>

        <FileUpload onUploadSuccess={handleUploadSuccess} />

        {activeData && (
          <div style={{ marginTop: '2rem' }}>
            <Dashboard data={activeData} documentId={activeDocumentId} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
