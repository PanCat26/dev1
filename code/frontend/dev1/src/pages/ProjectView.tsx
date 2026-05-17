import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api, type RepositoryOut, type ConversationOut } from '../services/api';
import { MessageSquare, Plus, RefreshCw } from 'lucide-react';
import { format } from 'date-fns';
import './ProjectView.css';

export function ProjectView() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [repo, setRepo] = useState<RepositoryOut | null>(null);
  const [conversations, setConversations] = useState<ConversationOut[]>([]);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    if (!id) return;

    // Fetch repo details
    api.getRepositories().then(repos => {
      const found = repos.find(r => r.id === id);
      if (found) setRepo(found);
    });

    fetchConversations();
  }, [id]);

  const fetchConversations = async () => {
    if (!id) return;
    try {
      const convs = await api.getConversations(id);
      // Sort by newest first
      convs.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
      setConversations(convs);
    } catch (e) {
      console.error('Failed to fetch conversations', e);
    }
  };

  const handleRefresh = async () => {
    if (!id) return;
    setRefreshing(true);
    try {
      await api.refreshRepository(id);
      // Optionally we could show a toast here
    } catch (e) {
      console.error('Failed to refresh repo', e);
    } finally {
      setRefreshing(false);
    }
  };

  const handleNewChat = async () => {
    if (!id) return;
    try {
      const newConv = await api.createConversation(id);
      navigate(`/project/${id}/chat/${newConv.id}`);
    } catch (e) {
      console.error('Failed to create chat', e);
    }
  };

  if (!repo) {
    return <div className="project-view-empty">Loading project details...</div>;
  }

  return (
    <div className="project-view">
      <div className="project-header glass-panel">
        <div className="project-title-area">
          <h1>{repo.name}</h1>
          <span className={`repo-status badge status-${repo.status}`}>{repo.status}</span>
        </div>
        <button
          className="button secondary"
          onClick={handleRefresh}
          disabled={refreshing}
        >
          <RefreshCw size={16} className={refreshing ? 'spinner' : ''} />
          {refreshing ? 'Updating...' : 'Update Project'}
        </button>
      </div>

      <div className="project-content">
        <div className="conversations-header">
          <h2>Your Chats</h2>
          <button className="button primary" onClick={handleNewChat}>
            <Plus size={16} /> New Chat
          </button>
        </div>

        <div className="conversations-grid">
          {conversations.map(conv => (
            <div
              key={conv.id}
              className="conversation-card glass-panel"
              onClick={() => navigate(`/project/${id}/chat/${conv.id}`)}
            >
              <div className="card-icon">
                <MessageSquare size={24} />
              </div>
              <div className="card-details">
                <h3>Chat</h3>
                <span className="card-date">
                  {format(new Date(conv.created_at), 'MMM d, yyyy h:mm a')}
                </span>
              </div>
            </div>
          ))}
          {conversations.length === 0 && (
            <div className="empty-state">
              No chats yet. Start a new chat to explore the repository!
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
