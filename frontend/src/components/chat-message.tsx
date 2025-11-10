'use client'

import { Message } from '@/types/chat'
import { cn } from '@/lib/utils'
import { Bot, User } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

type ChatMessageProps = {
  message: Message
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div
      className={cn(
        'flex w-full gap-3 px-4 py-3',
        isUser ? 'flex-row-reverse' : 'flex-row'
      )}
    >
      <div className={cn(
        'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full border shadow',
        isUser ? 'bg-zinc-900 text-white dark:bg-white dark:text-zinc-900' : 'bg-white dark:bg-zinc-800'
      )}>
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>
      <div className={cn(
        'flex max-w-[80%] rounded-2xl px-4 py-2',
        isUser 
          ? 'bg-zinc-900 text-white dark:bg-white dark:text-zinc-900' 
          : 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-zinc-100'
      )}>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  )
}