import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

import api from '../api';

const Dashboard = ({ data, documentId }) => {
    if (!data) return null;

    const { stats, type_distribution, data: records } = data;

    const handleDownloadReport = async () => {
        if (!documentId) return;
        try {
            const response = await api.get(`history/${documentId}/pdf/`, {
                responseType: 'blob', // Important for handling binary data
            });

            // Create a blob link to download
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `report_${documentId}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error("Failed to download PDF", error);
        }
    };

    const chartData = {
        labels: Object.keys(type_distribution),
        datasets: [
            {
                label: 'Equipment Count by Type',
                data: Object.values(type_distribution),
                backgroundColor: 'rgba(56, 189, 248, 0.6)',
                borderColor: 'rgba(56, 189, 248, 1)',
                borderWidth: 1,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
                labels: { color: '#94a3b8' }
            },
            title: {
                display: false,
            },
        },
        scales: {
            y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
            x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
        }
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '1rem' }}>
                <button
                    className="btn"
                    onClick={handleDownloadReport}
                    disabled={!documentId}
                    style={{ background: 'var(--accent-color)' }}
                >
                    Download PDF Report
                </button>
            </div>
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-value">{stats.total_count}</div>
                    <div className="stat-label">Total Equipment</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value">{stats.average_flowrate.toFixed(1)}</div>
                    <div className="stat-label">Avg. Flowrate</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value">{stats.average_pressure.toFixed(1)}</div>
                    <div className="stat-label">Avg. Pressure</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value">{stats.average_temperature.toFixed(1)}</div>
                    <div className="stat-label">Avg. Temp.</div>
                </div>
            </div>

            <div className="card">
                <h3 className="card-title">Equipment Distribution</h3>
                <div className="chart-container">
                    <Bar options={options} data={chartData} />
                </div>
            </div>

            <div className="card">
                <h3 className="card-title">Data Records</h3>
                <div style={{ overflowX: 'auto' }}>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Type</th>
                                <th>Flowrate</th>
                                <th>Pressure</th>
                                <th>Temp</th>
                            </tr>
                        </thead>
                        <tbody>
                            {records.map((row, idx) => (
                                <tr key={idx}>
                                    <td>{row['Equipment Name']}</td>
                                    <td>{row['Type']}</td>
                                    <td>{row.Flowrate}</td>
                                    <td>{row.Pressure}</td>
                                    <td>{row.Temperature}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
