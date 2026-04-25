import './App.css'

function App() {
  const wips = [
    { name: 'Project Hub v1', progress: 50, category: 'Software' },
    { name: 'Floating Shelves', progress: 85, category: 'Woodworking' },
    { name: 'Englisch Beruf v1: Software', progress: 50, category: 'Software' }
  ];

  const CircularGauge = ({ progress }: { progress: number }) => {
    const radius = 50;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (progress / 100) * circumference;

    return (
      <div className="gauge-container">
        <svg className="gauge-svg" width="140" height="140" viewBox="0 0 120 120">
          <circle className="gauge-bg" cx="60" cy="60" r={radius} />
          <circle 
            className="gauge-fill" 
            cx="60" 
            cy="60" 
            r={radius} 
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
        </svg>
        <div className="gauge-text">{progress}%</div>
      </div>
    );
  };

  return (
    <>
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap" rel="stylesheet" />
      
      <div className="container">
        <header className="header">
          <h1>Tim Bohmert</h1>
          <p>Father | Builder | Berlin</p>
          <nav className="nav">
            <a href="#">Bio</a>
            <span style={{ opacity: 0.3, cursor: 'not-allowed' }}>My Projects (WIP)</span>
            <span style={{ opacity: 0.3, cursor: 'not-allowed' }}>Learnings (WIP)</span>
          </nav>
        </header>

        <main>
          <section style={{ marginBottom: '6rem' }}>
            <h2 className="section-title">Log</h2>
            <p style={{ fontSize: '1.4rem', fontWeight: 'bold' }}>
              Building things with code, wood, and sweat. Exploring high-scale systems 
              and over-engineering for the fun of it.
            </p>
          </section>

          <section>
            <h2 className="section-title">Active WIPs</h2>
            <div className="wip-grid">
              {wips.map((wip) => (
                <div key={wip.name} className="wip-card">
                  <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>{wip.name}</h3>
                  <CircularGauge progress={wip.progress} />
                  <p style={{ fontSize: '0.8rem', fontWeight: '900', background: 'var(--black)', color: 'var(--white)', padding: '0.2rem 0.6rem' }}>
                    {wip.category.toUpperCase()}
                  </p>
                </div>
              ))}
            </div>
          </section>
        </main>

        <footer className="dad-joke">
          <p>Dad Joke: "I'm afraid for the calendar. Its days are numbered."</p>
        </footer>
      </div>
    </>
  )
}

export default App
