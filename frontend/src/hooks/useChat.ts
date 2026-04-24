import { useState, useCallback } from 'react'

export interface Message {
  id: string
  role: 'user' | 'agent'
  content: string
}

// Shape the backend expects for history entries
interface HistoryEntry {
  role: 'user' | 'assistant'  // Groq requires "assistant", not "agent"
  content: string
}

interface UseChatReturn {
  messages: Message[]
  streaming: boolean
  sendMessage: (text: string) => Promise<void>
}

const BACKEND_URL = 'http://localhost:8000/chat'

/**
 * Manages chat message state and the streaming fetch lifecycle.
 *
 * Flow:
 * 1. Snapshot current messages as history BEFORE any state mutations.
 * 2. Append the user message immediately so the UI feels instant.
 * 3. Append an empty agent message and set streaming=true.
 * 4. POST { message, history } to backend; read response as ReadableStream.
 * 5. Update agent bubble in-place on each chunk (no new bubble per token).
 * 6. Set streaming=false when the stream closes or errors.
 */
export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([])
  const [streaming, setStreaming] = useState(false)

  // messages is included in deps so the history snapshot is always fresh.
  // Re-creating sendMessage on each new message is acceptable — it's only
  // called via user interaction, not in a render hot path.
  const sendMessage = useCallback(async (text: string) => {
    // 1. Capture history snapshot BEFORE appending the new user message.
    //    Exclude empty agent placeholders (streaming not yet started).
    //    Map "agent" → "assistant" to match Groq's expected role values.
    const history: HistoryEntry[] = messages
      .filter((m) => m.content.length > 0)
      .map((m) => ({
        role: m.role === 'agent' ? 'assistant' : 'user',
        content: m.content,
      }))

    const userMsgId = `msg-${Date.now()}-user`
    const agentMsgId = `msg-${Date.now()}-agent`

    // 2. Show user message immediately
    setMessages((prev) => [
      ...prev,
      { id: userMsgId, role: 'user', content: text },
    ])

    // 3. Placeholder agent bubble — content grows as stream arrives
    setMessages((prev) => [
      ...prev,
      { id: agentMsgId, role: 'agent', content: '' },
    ])
    setStreaming(true)

    try {
      // 4. Include history so the backend can pass prior turns to Groq
      const response = await fetch(BACKEND_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history }),
      })

      if (!response.ok || !response.body) {
        throw new Error(`Backend error: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      // 5. Read stream chunks and append to the agent message in-place
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })

        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === agentMsgId
              ? { ...msg, content: msg.content + chunk }
              : msg,
          ),
        )
      }
    } catch {
      // 6. Replace empty agent bubble with a user-facing error message
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === agentMsgId
            ? { ...msg, content: 'Something went wrong. Please try again.' }
            : msg,
        ),
      )
    } finally {
      setStreaming(false)
    }
  }, [messages])

  return { messages, streaming, sendMessage }
}
