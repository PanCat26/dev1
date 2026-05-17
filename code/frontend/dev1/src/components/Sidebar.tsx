import { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { api, type RepositoryOut } from '../services/api';
import { FolderGit2, Plus, Loader2 } from 'lucide-react';
import './Sidebar.css';

export function Sidebar() {
  const [repos, setRepos] = useState<RepositoryOut[]>([]);
  const [isAdding, setIsAdding] = useState(false);
  const [newRepoUrl, setNewRepoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRepos = async () => {
    try {
      const data = await api.getRepositories();
      setRepos(data);
    } catch (e) {
      console.error('Failed to fetch repos', e);
    }
  };

  useEffect(() => {
    fetchRepos();
    const interval = setInterval(fetchRepos, 5000); // refresh every 5s for status updates
    return () => clearInterval(interval);
  }, []);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newRepoUrl) return;
    setLoading(true);
    setError(null);
    try {
      await api.addRepository(newRepoUrl);
      setNewRepoUrl('');
      setIsAdding(false);
      fetchRepos();
    } catch (err: any) {
      setError(err.message || 'Failed to add project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sidebar glass-panel">
      <div className="sidebar-header">
        <h2>Projects</h2>
        <button 
          className="button ghost icon-button" 
          onClick={() => setIsAdding(!isAdding)}
          title="Add Project"
        >
          <Plus size={20} />
        </button>
      </div>

      {isAdding && (
        <form onSubmit={handleAdd} className="add-repo-form">
          <input
            type="url"
            className="input"
            placeholder="GitHub URL..."
            value={newRepoUrl}
            onChange={(e) => setNewRepoUrl(e.target.value)}
            disabled={loading}
          />
          {error && <div className="error-text">{error}</div>}
          <div className="add-repo-actions">
            <button type="button" className="button ghost" onClick={() => setIsAdding(false)}>Cancel</button>
            <button type="submit" className="button primary" disabled={loading}>
              {loading ? <Loader2 className="spinner" size={16} /> : 'Add'}
            </button>
          </div>
        </form>
      )}

      <div className="repo-list">
        {repos.map(repo => (
          <NavLink
            key={repo.id}
            to={`/project/${repo.id}`}
            className={({ isActive }) => `repo-item ${isActive ? 'active' : ''}`}
          >
            <div className="repo-icon">
              <FolderGit2 size={18} />
            </div>
            <div className="repo-info">
              <span className="repo-name">{repo.name}</span>
              <span className={`repo-status status-${repo.status}`}>
                {repo.status}
              </span>
            </div>
          </NavLink>
        ))}
        {repos.length === 0 && !isAdding && (
          <div className="empty-state">No projects yet. Click + to add one.</div>
        )}
      </div>
    </div>
  );
}
