import { useEffect, useRef, useState } from 'react'
import MessageBubble from './MessageBubble'
import { useChat } from '../hooks/useChat'

/**
 * Full chat widget: header, scrollable message list, and input row.
 * Layout is fixed-height so the input row is always anchored to the bottom.
 */
export default function ChatWidget() {
  const { messages, streaming, sendMessage } = useChat()
  const [input, setInput] = useState('')
  const listRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  // Auto-scroll to bottom on every new token or message
  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight
    }
  }, [messages])

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  function handleSubmit() {
    const text = input.trim()
    if (!text || streaming) return
    setInput('')
    sendMessage(text)
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    // Enter submits; Shift+Enter inserts a newline
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="w-[420px] h-[600px] bg-gray-50 rounded-2xl shadow-xl flex flex-col overflow-hidden border border-gray-200">
      {/* Header */}
      <div className="bg-purple-600 px-5 py-4 flex items-center gap-3 shrink-0">
        <div className="w-2.5 h-2.5 rounded-full bg-green-400" />
        <span className="text-white font-semibold text-sm tracking-wide">Pura Support</span>
      </div>

      {/* Message list */}
      <div
        ref={listRef}
        className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-3"
      >
        {messages.length === 0 ? (
          // Empty state welcome message
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-400 text-sm text-center">
              Hi! Ask me anything about your Pura.
            </p>
          </div>
        ) : (
          messages.map((msg) => (
            <MessageBubble key={msg.id} role={msg.role} content={msg.content} />
          ))
        )}
      </div>

      {/* Input row */}
      <div className="shrink-0 border-t border-gray-200 bg-white px-4 py-3 flex items-end gap-2">
        <textarea
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={streaming}
          placeholder="Type a message…"
          rows={1}
          className="
            flex-1 resize-none rounded-xl border border-gray-200 px-3 py-2
            text-sm text-gray-800 placeholder-gray-400 leading-relaxed
            focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent
            disabled:opacity-50 disabled:bg-gray-50
            max-h-28 overflow-y-auto
          "
        />
        <button
          type="button"
          onClick={handleSubmit}
          disabled={streaming || !input.trim()}
          className="
            shrink-0 bg-purple-600 hover:bg-purple-700 text-white
            rounded-xl px-4 py-2 text-sm font-medium transition-colors
            disabled:opacity-40 disabled:cursor-not-allowed
          "
        >
          Send
        </button>
      </div>
    </div>
  )
}
