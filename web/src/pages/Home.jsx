import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { api } from '../api/client';
import PackageCard from '../components/PackageCard';

export default function Home() {
  const [query, setQuery] = useState('');
  const [packages, setPackages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPackages = async () => {
      setLoading(true);
      try {
        const data = await api.searchPackages(query);
        setPackages(data);
      } catch (err) {
        console.error("Failed to fetch packages", err);
      }
      setLoading(false);
    };
    
    // Simple debounce
    const timeout = setTimeout(fetchPackages, 300);
    return () => clearTimeout(timeout);
  }, [query]);

  return (
    <div className="container">
      <header style={{ textAlign: 'center', padding: '4rem 0' }}>
        <h1 className="gradient-text" style={{ fontSize: '3.5rem', letterSpacing: '-1px' }}>
          Discover AI Tools
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto 2rem' }}>
          The open marketplace for Model Context Protocol servers and AI plugins.
        </p>
        
        <div style={{ position: 'relative', maxWidth: '600px', margin: '0 auto' }}>
          <Search style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input 
            type="text" 
            placeholder="Search for packages (e.g. 'github', 'postgres')..." 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ width: '100%', paddingLeft: '3rem', fontSize: '1.1rem', borderRadius: '12px', background: 'var(--bg-card)' }}
          />
        </div>
      </header>

      <main>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>
          {query ? `Search results for "${query}"` : 'Featured Packages'}
        </h2>
        
        {loading ? (
          <p style={{ color: 'var(--text-muted)' }}>Loading packages...</p>
        ) : packages.length > 0 ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
            {packages.map(pkg => (
              <PackageCard key={pkg.name} pkg={pkg} />
            ))}
          </div>
        ) : (
          <p style={{ color: 'var(--text-muted)' }}>No packages found.</p>
        )}
      </main>
    </div>
  );
}
