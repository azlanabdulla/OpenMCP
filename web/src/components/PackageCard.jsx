import { Link } from 'react-router-dom';
import { ShieldCheck, Download, Package } from 'lucide-react';

export default function PackageCard({ pkg }) {
  return (
    <Link to={`/package/${pkg.name}`} className="card" style={{ display: 'block' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', margin: 0 }}>
          <Package size={20} color="var(--accent-blue)" />
          {pkg.name}
          {pkg.is_verified && <ShieldCheck size={18} color="var(--accent-cyan)" />}
        </h3>
      </div>
      
      <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '0.95rem', minHeight: '3rem' }}>
        {pkg.description || "No description provided."}
      </p>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {pkg.tags?.slice(0,3).map(tag => (
            <span key={tag.name} style={{ background: '#2a2a35', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
              {tag.name}
            </span>
          ))}
        </div>
      </div>
    </Link>
  );
}
