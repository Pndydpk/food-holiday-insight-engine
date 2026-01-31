import React, { useState, useEffect } from 'react';

function App() {
  const [holidays, setHolidays] = useState([]);
  const [selectedHoliday, setSelectedHoliday] = useState(null); // Nothing selected at first
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/holidays/upcoming')
      .then((res) => res.json())
      .then((data) => {
        setHolidays(data);
        // Automatically select the first holiday in the list as the default
        if (data.length > 0) setSelectedHoliday(data[0]);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="dashboard-container" style={{ display: 'flex', gap: '20px', padding: '20px' }}>
      
      {/* 1. THE HERO & SIDEBAR (Updates based on selection) */}
      <main style={{ flex: 2 }}>
        {selectedHoliday && (
          <section className="hero-section" style={{ background: '#f0f0f0', padding: '40px', borderRadius: '12px' }}>
            <h1>{selectedHoliday.holiday_name}</h1>
            <p>Popularity Score: <strong>{selectedHoliday.popularity_score}</strong></p>
            <div className="ai-strategy">
              <h3>💡 AI Marketing Strategy</h3>
              <p>Since this holiday has a score of {selectedHoliday.popularity_score}, 
                 we recommend a {selectedHoliday.popularity_score > 10 ? 'Major Campaign' : 'Social Media Shoutout'}.</p>
            </div>
          </section>
        )}
      </main>

      {/* 2. THE INTERACTIVE LIST (Click to select) */}
      <aside style={{ flex: 1 }}>
        <h2>Upcoming</h2>
        {holidays.map((item, index) => (
          <div 
            key={index} 
            onClick={() => setSelectedHoliday(item)} // This is the magic "Update" button
            style={{
              padding: '15px',
              margin: '10px 0',
              border: selectedHoliday?.holiday_name === item.holiday_name ? '2px solid #00ff00' : '1px solid #ccc',
              borderRadius: '8px',
              cursor: 'pointer'
            }}
          >
            <h3>{item.holiday_name}</h3>
            <p>🚀 {item.days_from_today} days to go!</p>
          </div>
        ))}
      </aside>

    </div>
  );
}

export default App;