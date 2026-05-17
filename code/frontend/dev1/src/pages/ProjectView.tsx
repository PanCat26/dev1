import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api, type RepositoryOut, type ConversationOut } from '../services/api';
import { MessageSquare, Plus, RefreshCw, Trash2 } from 'lucide-react';
import { format } from 'date-fns';
import './ProjectView.css';

export function ProjectView() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [repo, setRepo] = useState<RepositoryOut | null>(null);
  const [conversations, setConversations] = useState<ConversationOut[]>([]);
  const [chatNames, setChatNames] = useState<Record<string, string>>({});
  const [refreshing, setRefreshing] = useState(false);
  const [isCreatingChat, setIsCreatingChat] = useState(false);

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

      // Fetch titles based on first message
      const names: Record<string, string> = {};
      await Promise.all(convs.map(async (conv) => {
        try {
          const msgs = await api.getMessages(conv.id);
          const firstUserMsg = msgs.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()).find(m => m.role === 'user');
          if (firstUserMsg) {
             const content = firstUserMsg.content;
             names[conv.id] = content.length > 30 ? content.substring(0, 30) + '...' : content;
          } else {
             names[conv.id] = "New Chat";
          }
        } catch (e) {
          names[conv.id] = "Chat";
        }
      }));
      setChatNames(names);

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
    if (!id || isCreatingChat) return;
    setIsCreatingChat(true);
    try {
      const newConv = await api.createConversation(id);
      navigate(`/project/${id}/chat/${newConv.id}`);
    } catch (e) {
      console.error('Failed to create chat', e);
      setIsCreatingChat(false);
    }
  };

  const handleDeleteProject = async () => {
    if (!id || !window.confirm("Are you sure you want to delete this project?")) return;
    try {
      await api.deleteRepository(id);
      navigate('/');
    } catch (e) {
      console.error('Failed to delete project', e);
    }
  };

  const handleDeleteChat = async (e: React.MouseEvent, convId: string) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to delete this chat?")) return;
    try {
      await api.deleteConversation(convId);
      fetchConversations();
    } catch (err) {
      console.error('Failed to delete chat', err);
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
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            className="button danger"
            onClick={handleDeleteProject}
          >
            <Trash2 size={16} /> Delete
          </button>
          <button
            className="button secondary"
            onClick={handleRefresh}
            disabled={refreshing}
          >
            <RefreshCw size={16} className={refreshing ? 'spinner' : ''} />
            {refreshing ? 'Updating...' : 'Update'}
          </button>
        </div>
      </div>

      <div className="project-content">
        <div className="conversations-header">
          <h2>Your Chats</h2>
          <button className="button primary" onClick={handleNewChat} disabled={isCreatingChat}>
            <Plus size={16} /> {isCreatingChat ? 'Creating...' : 'New Chat'}
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
                <h3>{chatNames[conv.id] || 'Loading...'}</h3>
                <span className="card-date">
                  {format(new Date(conv.created_at), 'MMM d, yyyy h:mm a')}
                </span>
              </div>
              <button
                className="button ghost icon-button delete-chat-btn"
                onClick={(e) => handleDeleteChat(e, conv.id)}
                title="Delete Chat"
                style={{ marginLeft: 'auto', color: '#ef4444' }}
              >
                <Trash2 size={18} />
              </button>
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
