import { Routes, Route, Navigate } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { ProjectView } from './pages/ProjectView';
import { ChatView } from './pages/ChatView';

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      <Routes>
        <Route path="/" element={
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
            Select a project from the sidebar to get started.
          </div>
        } />
        <Route path="/project/:id" element={<ProjectView />} />
        <Route path="/project/:id/chat/:convId" element={<ChatView />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}

export default App;
