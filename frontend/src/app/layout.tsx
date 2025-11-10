import { Providers } from './providers'
import { Navbar } from '@/components/navbar'
import { Chat } from '@/components/chat'
import "./globals.css"

export const metadata = {
  title: 'Assistente de Medicamentos',
  description: 'Um chatbot para informações sobre medicamentos',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <body>
        <Providers>
          <div className="flex min-h-screen flex-col bg-white text-zinc-900 antialiased dark:bg-zinc-900 dark:text-zinc-50">
            <Navbar />
            <main className="flex-1">
              <Chat />
            </main>
          </div>
        </Providers>
      </body>
    </html>
  )
}
