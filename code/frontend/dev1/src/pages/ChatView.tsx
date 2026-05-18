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
  const [streamingContentAlt, setStreamingContentAlt] = useState('');
  const [feedbackId, setFeedbackId] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const feedbackIdRef = useRef<string | null>(null);
  const messageIdRef = useRef<string | null>(null);
  const isChoosingRef = useRef<boolean>(false);

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
        } else if (data.type === 'content_alt') {
          setStreamingContentAlt(prev => prev + (data.delta || ''));
        } else if (data.type === 'rlhf_start') {
          isChoosingRef.current = true;
          setFeedbackId('pending');
        } else if (data.type === 'rlhf_feedback_id') {
          feedbackIdRef.current = data.id;
          setFeedbackId(data.id);
        } else if (data.type === 'message_id') {
          messageIdRef.current = data.id;
        } else if (data.type === 'done') {
          setIsGenerating(false);
          if (!isChoosingRef.current) {
            api.getMessages(convId).then(msgs => {
              setMessages(msgs.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()));
              setStreamingContent('');
              setStreamingContentAlt('');
            });
          }
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

  const handleChoice = async (chosen: string, rejected: string) => {
    if (!feedbackIdRef.current || !id) return;
    try {
      await api.updateFeedback(id, feedbackIdRef.current, chosen, rejected, messageIdRef.current || undefined);
      api.getMessages(convId!).then(msgs => {
        setMessages(msgs.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()));
      });
    } catch (e) {
      console.error(e);
    } finally {
      feedbackIdRef.current = null;
      messageIdRef.current = null;
      isChoosingRef.current = false;
      setFeedbackId(null);
      setStreamingContent('');
      setStreamingContentAlt('');
    }
  };

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isGenerating || feedbackId) return;

    const messageText = input;
    setInput('');
    setIsGenerating(true);
    setStreamingContent('');
    setStreamingContentAlt('');
    setFeedbackId(null);
    feedbackIdRef.current = null;
    messageIdRef.current = null;
    isChoosingRef.current = false;

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

            {isGenerating && !feedbackId && (
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
            
            {feedbackId && (
              <div className="rlhf-container">
                <div className="rlhf-header">
                  <Bot size={20} />
                  <span>Please choose the best response</span>
                </div>
                <div className="rlhf-choices">
                  <div className="rlhf-choice glass-panel">
                    <div className="rlhf-content">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{streamingContent}</ReactMarkdown>
                    </div>
                    <button 
                      className="button primary" 
                      onClick={() => handleChoice(streamingContent, streamingContentAlt)}
                      disabled={isGenerating || feedbackId === 'pending'}
                    >
                      Choose Option A
                    </button>
                  </div>
                  <div className="rlhf-choice glass-panel">
                    <div className="rlhf-content">
                      {streamingContentAlt ? (
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{streamingContentAlt}</ReactMarkdown>
                      ) : (
                        <span className="typing-indicator">Generating alternative...</span>
                      )}
                    </div>
                    <button 
                      className="button primary" 
                      onClick={() => handleChoice(streamingContentAlt, streamingContent)}
                      disabled={isGenerating || feedbackId === 'pending'}
                    >
                      Choose Option B
                    </button>
                  </div>
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
            disabled={isGenerating || feedbackId !== null}
            autoFocus
          />
          <button
            type="submit"
            className="button primary send-button"
            disabled={!input.trim() || isGenerating || feedbackId !== null}
          >
            {isGenerating ? <Loader2 className="spinner" size={18} /> : <Send size={18} />}
          </button>
        </form>
      </div>
    </div>
  );
}
