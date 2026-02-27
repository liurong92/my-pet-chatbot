import { useState, useRef, useEffect, useCallback } from 'react'
import './App.css'

const API_BASE = '/api'

function useChat(activeModel) {
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const sendMessage = useCallback(async (text) => {
    if (!text.trim() || loading) return

    const userMsg = { role: 'user', text, id: Date.now() }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)
    setError(null)

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, session_id: sessionId }),
      })

      if (!res.ok) {
        const detail = await res.json().catch(() => ({}))
        throw new Error(detail.detail || `HTTP ${res.status}`)
      }

      const data = await res.json()
      setSessionId(data.session_id)
      const botMsg = { role: 'bot', text: data.response, id: Date.now() + 1 }
      setMessages((prev) => [...prev, botMsg])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [loading, sessionId])

  const resetSession = useCallback(async () => {
    if (!sessionId) return
    try {
      await fetch(`${API_BASE}/reset`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId }),
      })
    } catch (_) {}
    setMessages([])
    setError(null)
    // Keep sessionId so server-side settings are retained
  }, [sessionId])

  return { messages, loading, error, sendMessage, resetSession, sessionId, setSessionId }
}

function Message({ msg }) {
  const isUser = msg.role === 'user'
  return (
    <div className={`message-row ${isUser ? 'user-row' : 'bot-row'}`}>
      {!isUser && <div className="avatar bot-avatar">🐾</div>}
      <div className={`bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`}>
        {msg.text.split('\n').map((line, i) => (
          <span key={i}>
            {line}
            {i < msg.text.split('\n').length - 1 && <br />}
          </span>
        ))}
      </div>
      {isUser && <div className="avatar user-avatar">👤</div>}
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="message-row bot-row">
      <div className="avatar bot-avatar">🐾</div>
      <div className="bubble bot-bubble typing-bubble">
        <span className="dot" /><span className="dot" /><span className="dot" />
      </div>
    </div>
  )
}

function SettingsPanel({ activeModel, sessionId, onSaved, onClear, onClose }) {
  const [apiKey, setApiKey] = useState('')
  const [model, setModel] = useState(activeModel || '')
  const [showKey, setShowKey] = useState(false)
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState(null)

  const handleSave = async () => {
    if (!apiKey.trim() || !model.trim()) return
    setSaving(true)
    setSaveError(null)
    try {
      const res = await fetch(`${API_BASE}/settings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key: apiKey.trim(),
          model: model.trim(),
          session_id: sessionId,
        }),
      })
      if (!res.ok) {
        const detail = await res.json().catch(() => ({}))
        throw new Error(detail.detail || `HTTP ${res.status}`)
      }
      const data = await res.json()
      setApiKey('')   // clear from local state immediately after sending
      onSaved(data.session_id, data.model)
      onClose()
    } catch (err) {
      setSaveError(err.message)
    } finally {
      setSaving(false)
    }
  }

  const handleClear = () => {
    setApiKey('')
    setModel('')
    onClear()
    onClose()
  }

  return (
    <div className="settings-panel">
      <div className="settings-header">
        <span className="settings-title">自定义模型设置</span>
        <button className="settings-close" onClick={onClose} aria-label="关闭">✕</button>
      </div>

      <div className="settings-body">
        <label className="settings-label">
          API Token
          <div className="settings-input-row">
            <input
              type={showKey ? 'text' : 'password'}
              className="settings-input"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder={activeModel ? '已配置，重新输入以更新' : 'sk-ant-...'}
              autoComplete="off"
              spellCheck={false}
            />
            <button
              type="button"
              className="toggle-visibility"
              onClick={() => setShowKey((v) => !v)}
              aria-label={showKey ? '隐藏' : '显示'}
            >
              {showKey ? '🙈' : '👁'}
            </button>
          </div>
        </label>

        <label className="settings-label">
          Model
          <input
            type="text"
            className="settings-input"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            placeholder="anthropic:claude-sonnet-4-5"
            autoComplete="off"
            spellCheck={false}
          />
          <span className="settings-hint">
            支持格式：<code>anthropic:claude-...</code>、<code>openai:gpt-...</code>、<code>google-gla:gemini-...</code>
          </span>
        </label>

        {saveError && <p className="settings-error">⚠️ {saveError}</p>}
      </div>

      <div className="settings-actions">
        {activeModel && (
          <button className="settings-btn-clear" onClick={handleClear}>清除配置</button>
        )}
        <button
          className="settings-btn-save"
          onClick={handleSave}
          disabled={saving || !apiKey.trim() || !model.trim()}
        >
          {saving ? '保存中…' : '保存'}
        </button>
      </div>
    </div>
  )
}

export default function App() {
  const [activeModel, setActiveModel] = useState(null) // model name stored on server
  const [settingsOpen, setSettingsOpen] = useState(false)
  const { messages, loading, error, sendMessage, resetSession, sessionId, setSessionId } = useChat(activeModel)
  const [input, setInput] = useState('')
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const handleSubmit = (e) => {
    e.preventDefault()
    const text = input.trim()
    if (!text) return
    setInput('')
    sendMessage(text)
    inputRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleSettingsSaved = (newSessionId, model) => {
    setSessionId(newSessionId)
    setActiveModel(model)
  }

  const handleSettingsClear = () => {
    setActiveModel(null)
    // Session still exists server-side, but api_key/model will be cleared on next save
    // For a full clear we could call a dedicated endpoint; here we just reset local state
    setSessionId(null)
  }

  const suggestions = [
    "What is Rong's pet name?",
    "Tell me about April's colors",
    "What is Lan's pet name?",
    "What pets do you know about?",
  ]

  return (
    <div className="chat-container">
      {/* Header */}
      <header className="chat-header">
        <div className="header-left">
          <span className="header-icon">🐾</span>
          <div>
            <h1 className="header-title">Pet Assistant</h1>
            <p className="header-subtitle">Ask me anything about your pets</p>
          </div>
        </div>
        <div className="header-actions">
          <button
            className={`settings-btn ${activeModel ? 'settings-btn-active' : ''}`}
            onClick={() => setSettingsOpen((v) => !v)}
            title="自定义模型"
            aria-label="设置"
          >
            ⚙
            {activeModel && <span className="settings-badge" />}
          </button>
          <button
            className="reset-btn"
            onClick={resetSession}
            disabled={!sessionId && messages.length === 0}
            title="Start new conversation"
          >
            New Chat
          </button>
        </div>
      </header>

      {/* Settings panel */}
      {settingsOpen && (
        <SettingsPanel
          activeModel={activeModel}
          sessionId={sessionId}
          onSaved={handleSettingsSaved}
          onClear={handleSettingsClear}
          onClose={() => setSettingsOpen(false)}
        />
      )}

      {/* Messages */}
      <main className="chat-messages">
        {messages.length === 0 && !loading && (
          <div className="empty-state">
            <div className="empty-icon">🐱</div>
            <h2>Hello! I'm your Pet Assistant</h2>
            <p>Ask me about your pets' information, health, and more.</p>
            <div className="suggestions">
              {suggestions.map((s) => (
                <button
                  key={s}
                  className="suggestion-btn"
                  onClick={() => sendMessage(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <Message key={msg.id} msg={msg} />
        ))}

        {loading && <TypingIndicator />}

        {error && (
          <div className="error-banner">
            ⚠️ {error}
          </div>
        )}

        <div ref={bottomRef} />
      </main>

      {/* Input */}
      <footer className="chat-footer">
        <form className="input-form" onSubmit={handleSubmit}>
          <textarea
            ref={inputRef}
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about your pets… (Enter to send)"
            rows={1}
            disabled={loading}
          />
          <button
            type="submit"
            className="send-btn"
            disabled={!input.trim() || loading}
            aria-label="Send"
          >
            <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
            </svg>
          </button>
        </form>
        <p className="footer-note">
          {activeModel
            ? `自定义模型: ${activeModel}`
            : 'Powered by Claude · Pet data stored in Qdrant'}
        </p>
      </footer>
    </div>
  )
}
