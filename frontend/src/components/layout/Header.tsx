import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">
          <Link to="/">Reharmonizer</Link>
        </h1>
        <nav className="header-nav">
          <Link to="/key-to-chords" className="nav-link">
            Key to Chords
          </Link>
          <Link to="/substitution" className="nav-link">
            Chord Substitution
          </Link>
          <Link to="/chord-to-notes" className="nav-link">
            Chord to Notes
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
