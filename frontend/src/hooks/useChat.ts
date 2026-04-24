import { useState, useCallback } from 'react'

export interface Message {
  id: string
  role: 'user' | 'agent'
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
 * 1. Append the user message immediately so the UI feels instant.
 * 2. Append an empty agent message and set streaming=true.
 * 3. Read the response body as a ReadableStream, updating the agent
 *    message's content in-place on each chunk (no new bubble per token).
 * 4. Set streaming=false when the stream closes or errors.
 */
export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([])
  const [streaming, setStreaming] = useState(false)

  const sendMessage = useCallback(async (text: string) => {
    // Stable IDs — simple incrementing string is sufficient for local state
    const userMsgId = `msg-${Date.now()}-user`
    const agentMsgId = `msg-${Date.now()}-agent`

    // 1. Show user message immediately
    setMessages((prev) => [
      ...prev,
      { id: userMsgId, role: 'user', content: text },
    ])

    // 2. Placeholder agent bubble — content grows as stream arrives
    setMessages((prev) => [
      ...prev,
      { id: agentMsgId, role: 'agent', content: '' },
    ])
    setStreaming(true)

    try {
      const response = await fetch(BACKEND_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      })

      if (!response.ok || !response.body) {
        throw new Error(`Backend error: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      // 3. Read stream chunks and append to the agent message in-place
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
      // 4. Replace empty agent bubble with a user-facing error message
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
  }, [])

  return { messages, streaming, sendMessage }
}
