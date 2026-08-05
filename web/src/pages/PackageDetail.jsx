import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Terminal, ShieldCheck, Copy, Check } from 'lucide-react';
import { api } from '../api/client';

export default function PackageDetail() {
  const { name } = useParams();
  const [pkg, setPkg] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    api.getPackage(name)
      .then(setPkg)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [name]);

  const copyInstall = () => {
    navigator.clipboard.writeText(`openmcp install ${name}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) return <div className="container"><p>Loading...</p></div>;
  if (!pkg) return <div className="container"><p>Package not found.</p></div>;

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '2.5rem', margin: 0 }}>
            {pkg.name}
            {pkg.is_verified && <ShieldCheck size={28} color="var(--accent-cyan)" />}
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', marginTop: '0.5rem' }}>
            {pkg.description}
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '2rem' }}>
        <div>
          <div className="card" style={{ marginBottom: '2rem' }}>
            <h3 style={{ marginBottom: '1rem', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>Readme</h3>
            <p style={{ color: 'var(--text-muted)' }}>
              (Markdown rendering would go here. For now, this is a placeholder for the package README.)
            </p>
          </div>
        </div>

        <div>
          <div className="card" style={{ position: 'sticky', top: '2rem' }}>
            <h4 style={{ marginBottom: '1rem' }}>Install</h4>
            
            <div 
              style={{ 
                background: '#000', 
                padding: '1rem', 
                borderRadius: '8px', 
                display: 'flex', 
                justifyContent: 'space-between',
                alignItems: 'center',
                fontFamily: 'var(--font-mono)',
                border: '1px solid var(--border)',
                marginBottom: '1.5rem'
              }}
            >
              <span><span style={{color: 'var(--accent-cyan)'}}>$</span> openmcp install {name}</span>
              <button 
                onClick={copyInstall}
                style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
                title="Copy to clipboard"
              >
                {copied ? <Check size={18} color="var(--accent-cyan)" /> : <Copy size={18} />}
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', fontSize: '0.9rem' }}>
              <div>
                <strong style={{ color: 'var(--text-muted)' }}>Status</strong>
                <div style={{ marginTop: '0.2rem' }}>
                  {pkg.is_verified ? <span style={{color: 'var(--accent-cyan)'}}>Verified Publisher</span> : <span>Unverified</span>}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
