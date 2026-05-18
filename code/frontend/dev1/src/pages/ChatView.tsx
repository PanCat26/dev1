import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api, type MessageOut, WS_BASE } from '../services/api';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Send, ArrowLeft, Bot, User, Loader2 } from 'lucide-react';
import './ChatView.css';

export function ChatView() {
  const { id, convId } = useParams<{ id: string, convId: string }>();
  const navigate = useNavigate();
  const [messages, setMessages] = useState<MessageOut[]>([]);
  const [input, setInput] = useState('');
  const [loadingHistory, setLoadingHistory] = useState(true);

  // Streaming state
  const [isGenerating, setIsGenerating] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');

  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent]);

  useEffect(() => {
    if (!convId) return;

    // Load history
    setLoadingHistory(true);
    api.getMessages(convId)
      .then(msgs => setMessages(msgs.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())))
      .catch(e => console.error('Failed to load history', e))
      .finally(() => setLoadingHistory(false));

    // Connect WebSocket
    const wsUrl = `${WS_BASE}/conversations/${convId}/ws`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'content') {
          setStreamingContent(prev => prev + (data.delta || ''));
        } else if (data.type === 'done') {
          setIsGenerating(false);
          // Reload messages from server to get the final persisted versions
          api.getMessages(convId).then(msgs => {
            setMessages(msgs.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()));
            setStreamingContent('');
          });
        } else if (data.type === 'error') {
          console.error('WS Error:', data.message);
          setIsGenerating(false);
          setStreamingContent(prev => prev + `\n\n**Error:** ${data.message}`);
        }
      } catch (err) {
        console.error('Failed to parse WS message', err);
      }
    };

    ws.onclose = () => {
      console.log('WS Disconnected');
    };

    return () => {
      ws.close();
    };
  }, [convId]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isGenerating) return;

    const messageText = input;
    setInput('');
    setIsGenerating(true);
    setStreamingContent('');

    // Optimistically add user message to UI
    const tempUserMsg: MessageOut = {
      id: Math.random().toString(),
      conversation_id: convId!,
      role: 'user',
      content: messageText,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMsg]);

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(messageText);
    } else {
      console.error('WebSocket is not open');
      setIsGenerating(false);
    }
  };

  return (
    <div className="chat-view">
      <div className="chat-header glass-panel">
        <button className="button ghost icon-button" onClick={() => navigate(`/project/${id}`)}>
          <ArrowLeft size={20} />
        </button>
        <h2>Chat</h2>
      </div>

      <div className="chat-messages-area">
        {loadingHistory ? (
          <div className="loading-state">
            <Loader2 className="spinner" size={24} /> Loading messages...
          </div>
        ) : (
          <div className="messages-list">
            {messages.map(msg => (
              <div key={msg.id} className={`message-wrapper ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                </div>
                <div className="message-content glass-panel">
                  {msg.role === 'user' ? (
                    <div className="raw-text">{msg.content}</div>
                  ) : (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                  )}
                </div>
              </div>
            ))}

            {isGenerating && (
              <div className="message-wrapper assistant">
                <div className="message-avatar">
                  <Bot size={20} />
                </div>
                <div className="message-content glass-panel generating">
                  {streamingContent ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{streamingContent}</ReactMarkdown>
                  ) : (
                    <span className="typing-indicator">Thinking...</span>
                  )}
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <div className="chat-input-area glass-panel">
        <form onSubmit={handleSend} className="chat-input-form">
          <input
            type="text"
            className="input chat-input"
            placeholder="Type your message..."
            value={input}
            onChange={e => setInput(e.target.value)}
            disabled={isGenerating}
            autoFocus
          />
          <button
            type="submit"
            className="button primary send-button"
            disabled={!input.trim() || isGenerating}
          >
            {isGenerating ? <Loader2 className="spinner" size={18} /> : <Send size={18} />}
          </button>
        </form>
      </div>
    </div>
  );
}
