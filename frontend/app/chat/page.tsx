'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import ReactMarkdown from 'react-markdown';
import Navbar from '../../components/Navbar';

interface Message {
  id: number;
  text: string;
  isUser: boolean;
  sources?: string[];
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState<any>(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/unauthorized');
      return;
    }

    // Verificar se o token é válido
    fetch('http://127.0.0.1:8000/api/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(res => {
      if (!res.ok) {
        localStorage.removeItem('token');
        router.push('/unauthorized');
      } else {
        return res.json();
      }
    })
    .then(userData => {
      if (userData) {
        setUser(userData);
      }
    })
    .catch(() => {
      localStorage.removeItem('token');
      router.push('/unauthorized');
    });
  }, [router]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now(),
      text: input,
      isUser: true
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://127.0.0.1:8000/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ question: input }),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage: Message = {
          id: Date.now() + 1,
          text: data.answer,
          isUser: false,
          sources: data.sources
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        throw new Error('Erro na resposta');
      }
    } catch (err) {
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Desculpe, ocorreu um erro. Tente novamente.',
        isUser: false
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/login');
  };

  if (!user) {
    return <div className="min-h-screen flex items-center justify-center">Carregando...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar userName={user.name} onLogout={handleLogout} />

      <div className="max-w-4xl mx-auto p-4 h-[calc(100vh-80px)] flex flex-col">
        <div className="flex-1 overflow-y-auto mb-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-8">
              Faça uma pergunta sobre medicamentos para começar
            </div>
          )}
          
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-3 ${message.isUser ? 'justify-end' : 'justify-start'}`}
            >
              {!message.isUser && (
                <Image src="/bot-icon.svg" alt="Bot" width={32} height={32} className="mt-1" />
              )}
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.isUser
                    ? 'bg-gray-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white border'
                }`}
              >
                {message.isUser ? (
                  <p className="whitespace-pre-wrap">{message.text}</p>
                ) : (
                  <div className="prose prose-sm max-w-none dark:prose-invert">
                    <ReactMarkdown>
                      {message.text}
                    </ReactMarkdown>
                  </div>
                )}
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-2 text-xs text-gray-500">
                    Fontes: {message.sources.join(', ')}
                  </div>
                )}
              </div>
              {message.isUser && (
                <Image src="/user-icon.svg" alt="User" width={32} height={32} className="mt-1" />
              )}
            </div>
          ))}
          
          {loading && (
            <div className="flex items-start gap-3 justify-start">
              <Image src="/bot-icon.svg" alt="Bot" width={32} height={32} className="mt-1" />
              <div className="bg-white dark:bg-gray-800 border px-4 py-2 rounded-lg">
                Digitando...
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Digite sua pergunta sobre medicamentos..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent dark:bg-gray-800 dark:border-gray-600 dark:text-white resize-none min-h-[40px] max-h-32"
            disabled={loading}
            rows={1}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-400 text-white rounded-lg transition-colors"
          >
            <Image src="/send-icon.svg" alt="Enviar" width={20} height={20} />
          </button>
        </form>
      </div>
    </div>
  );
}