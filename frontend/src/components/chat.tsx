'use client';

import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { Message } from '@/types/chat';
import { ChatMessage } from './chat-message';
import { sendMessage } from '@/lib/api';

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await sendMessage(userMessage.content);
      console.log('Received response:', data); // Debug log

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.answer || data.content || data.message || 'Não foi possível obter uma resposta', // Handle different response formats
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="mx-auto w-full max-w-4xl px-4">
      <div className="flex h-[calc(100vh-4rem)] flex-col">
        <div className="flex-1 overflow-y-auto">
          <div className="flex flex-col space-y-4 py-4">
            {messages.length === 0 ? (
              <div className="flex flex-1 items-center justify-center p-8 text-center text-zinc-500 dark:text-zinc-400">
                <p>Comece uma conversa sobre medicamentos.</p>
              </div>
            ) : (
              messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
        <div className="border-t dark:border-zinc-800">
          <form
            onSubmit={handleSubmit}
            className="mx-auto flex max-w-4xl items-center gap-2 p-4"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Pergunte sobre medicamentos..."
            className="flex-1 rounded-md border bg-transparent px-4 py-2 outline-none focus:border-zinc-400 dark:border-zinc-800 dark:focus:border-zinc-600"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="rounded-md bg-zinc-900 p-2 text-white transition-opacity hover:opacity-90 disabled:opacity-50 dark:bg-white dark:text-zinc-900"
          >
            <Send className="h-4 w-4" />
          </button>
        </form>
      </div>
    </div>
    </div>
  );
}