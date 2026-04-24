interface Props {
  role: 'user' | 'agent'
  content: string
}

/**
 * Renders a single chat message bubble.
 * User messages sit on the right in purple; agent messages sit on the left in white.
 */
export default function MessageBubble({ role, content }: Props) {
  const isUser = role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`
          max-w-[75%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed whitespace-pre-wrap
          ${isUser
            ? 'bg-purple-600 text-white rounded-br-sm'
            : 'bg-white text-gray-800 border border-gray-200 rounded-bl-sm shadow-sm'
          }
        `}
      >
        {content}
      </div>
    </div>
  )
}
