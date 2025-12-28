import React, { ReactNode } from 'react';
import Header from './Header';
import './MainLayout.css';

interface MainLayoutProps {
  children: ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="main-layout">
      <Header />
      <main className="main-content">{children}</main>
    </div>
  );
};

export default MainLayout;
