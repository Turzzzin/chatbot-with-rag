export type Message = {
  id: string
  content: string
  role: 'user' | 'assistant'
  timestamp: Date
}

export type ChatResponse = {
  content: string
  disclaimer: string
}