import Link from 'next/link';
import { getRegulations } from '../lib/api';
import { Regulation } from '../lib/types';

export default async function Home() {
  // Fetch regulations from the API
  let regulations: Regulation[] = [];
  let error: string | null = null;
  try {
    regulations = await getRegulations();
  } catch (err) {
    console.error("Failed to fetch regulations:", err);
    error = "Could not load regulations. Please ensure the backend is running.";
  }

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="container mx-auto max-w-5xl py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-extrabold text-gray-900 sm:text-6xl">
            UKFW Knowledge Graph
          </h1>
          <p className="mt-5 text-xl text-gray-600 max-w-2xl mx-auto">
            Explore interconnected regulations, provisions, roles, and expert knowledge.
          </p>
        </div>
      
        {error && <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-8 rounded-md shadow" role="alert"><p className="font-bold">Error</p><p>{error}</p></div>}

        {regulations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {regulations.map(reg => (
              <Link 
                key={reg.id} 
                href={`/regulations/${reg.id}`}
                className="block p-6 bg-white rounded-xl shadow-lg hover:shadow-2xl transition-shadow duration-300 ease-in-out transform hover:-translate-y-1"
              >
                <h2 className="text-2xl font-semibold text-gray-800 mb-2">{reg.title}</h2>
                <p className="text-sm text-gray-500 mb-3">ID: {reg.id}</p>
                <p className="text-gray-600 text-sm line-clamp-3">{reg.description || 'No description available.'}</p>
                {/* line-clamp-3 might require a plugin: @tailwindcss/line-clamp */}
              </Link>
            ))}
          </div>
        ) : (
          !error && <div className="text-center text-gray-500 text-lg py-10">No regulations found to display.</div>
        )}
      </div>
    </main>
  );
}

  