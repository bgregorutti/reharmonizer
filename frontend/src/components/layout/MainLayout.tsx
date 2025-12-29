import React, { ReactNode } from 'react';
import './MainLayout.css';

interface MainLayoutProps {
  children: ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="main-layout">
      <main className="main-content">{children}</main>
    </div>
  );
};

export default MainLayout;
