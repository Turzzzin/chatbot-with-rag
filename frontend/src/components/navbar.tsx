'use client'

import { ThemeToggle } from './theme-toggle'

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/80 px-4 backdrop-blur-sm dark:border-zinc-800 dark:bg-zinc-900/80">
      <div className="mx-auto flex h-16 max-w-4xl items-center justify-between">
        <h1 className="text-lg font-semibold">Assistente de Medicamentos</h1>
        <div className="relative">
          <ThemeToggle />
        </div>
      </div>
    </header>
  )
}