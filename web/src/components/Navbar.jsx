import { Link } from 'react-router-dom';
import { Terminal } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar container">
      <Link to="/" className="nav-brand">
        <Terminal color="var(--accent-cyan)" size={28} />
        OpenMCP
      </Link>
      <div className="nav-links">
        <Link to="/">Explore</Link>
        <a href="https://github.com/azlanabdulla/OpenMCP" target="_blank" rel="noreferrer">GitHub</a>
        {user ? (
          <>
            <span style={{ color: 'var(--text-muted)' }}>{user.email}</span>
            <button onClick={logout} className="btn btn-outline" style={{ padding: '0.4rem 1rem' }}>Logout</button>
          </>
        ) : (
          <Link to="/login" className="btn btn-primary" style={{ padding: '0.4rem 1rem' }}>Sign In</Link>
        )}
      </div>
    </nav>
  );
}
