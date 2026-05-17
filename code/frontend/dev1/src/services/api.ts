const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const WS_BASE = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';

export interface RepositoryOut {
  id: string;
  name: string;
  github_url: string;
  default_branch: string;
  commit_sha: string;
  status: string;
  created_at: string;
}

export interface ConversationOut {
  id: string;
  repository_id: string;
  created_at: string;
}

export interface MessageOut {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

export const api = {
  getRepositories: async (): Promise<RepositoryOut[]> => {
    const res = await fetch(`${API_BASE}/repositories`);
    if (!res.ok) throw new Error('Failed to fetch repositories');
    return res.json();
  },

  addRepository: async (github_url: string): Promise<any> => {
    const res = await fetch(`${API_BASE}/repositories`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ github_url }),
      signal: AbortSignal.timeout(15000),
    });
    if (!res.ok) throw new Error('Failed to add repository');
    return res.json();
  },

  refreshRepository: async (repo_id: string): Promise<{ updated: boolean }> => {
    const res = await fetch(`${API_BASE}/repositories/${repo_id}/refresh`, {
      method: 'POST',
      signal: AbortSignal.timeout(15000),
    });
    if (!res.ok) throw new Error('Failed to refresh repository');
    return res.json();
  },

  deleteRepository: async (repo_id: string): Promise<void> => {
    const res = await fetch(`${API_BASE}/repositories/${repo_id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete repository');
  },

  getConversations: async (repo_id: string): Promise<ConversationOut[]> => {
    const res = await fetch(`${API_BASE}/repositories/${repo_id}/conversations`);
    if (!res.ok) throw new Error('Failed to fetch conversations');
    return res.json();
  },

  createConversation: async (repo_id: string): Promise<ConversationOut> => {
    const res = await fetch(`${API_BASE}/repositories/${repo_id}/conversations`, {
      method: 'POST',
      signal: AbortSignal.timeout(10000),
    });
    if (!res.ok) throw new Error('Failed to create conversation');
    return res.json();
  },

  deleteConversation: async (conv_id: string): Promise<void> => {
    const res = await fetch(`${API_BASE}/conversations/${conv_id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete conversation');
  },

  getMessages: async (conv_id: string): Promise<MessageOut[]> => {
    const res = await fetch(`${API_BASE}/conversations/${conv_id}/messages`);
    if (!res.ok) throw new Error('Failed to fetch messages');
    return res.json();
  },
};
