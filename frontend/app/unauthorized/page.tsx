export default function Unauthorized() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="max-w-md w-full text-center space-y-6 p-8">
        <div className="text-6xl">🔒</div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Acesso Negado
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Você precisa estar logado para acessar o chat de medicamentos.
        </p>
        <a
          href="/login"
          className="inline-block w-full py-3 px-4 bg-gray-600 hover:bg-gray-700 text-white font-medium rounded-lg transition-colors"
        >
          Fazer Login
        </a>
      </div>
    </div>
  );
}