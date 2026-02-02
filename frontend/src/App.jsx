import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import History from './components/History';
import api from './api';
import './App.css';

function App() {
  const [activeData, setActiveData] = useState(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [refreshHistory, setRefreshHistory] = useState(0);

  const handleUploadSuccess = (response) => {
    setActiveData(response.analysis);
    setRefreshHistory(prev => prev + 1); // Trigger history refresh
  };

  const handleHistorySelect = (item) => {
    if (item.summary) {
      setActiveData(item.summary);
    }
  };

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="logo">
          ⚡ EquipmentViz
        </div>
        <div className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
          Dashboard
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
            <Dashboard data={activeData} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
