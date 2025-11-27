import Image from 'next/image';

interface NavbarProps {
  userName: string;
  onLogout: () => void;
}

export default function Navbar({ userName, onLogout }: NavbarProps) {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b">
      <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
          MedQuery
        </h1>
        <div className="flex items-center gap-4">
          <span className="text-gray-600 dark:text-gray-400">Olá, {userName}</span>
          <button
            onClick={onLogout}
            className="text-red-600 hover:text-red-700 p-1"
          >
            <Image src="/logout-icon.svg" alt="Logout" width={20} height={20} />
          </button>
        </div>
      </div>
    </header>
  );
}