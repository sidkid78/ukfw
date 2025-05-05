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
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-4">UKFW Knowledge Graph</h1>
      <p className="mb-4">Select a regulation to start exploring:</p>
      
      {error && <div className="text-red-600 mb-4">{error}</div>}

      {regulations.length > 0 ? (
        <ul className="space-y-1">
          {regulations.map(reg => (
            <li key={reg.id}>
              <Link 
                href={`/regulations/${reg.id}`}
                className="text-blue-600 hover:underline"
              >
                {reg.title} ({reg.id})
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        !error && <div className="text-gray-500">No regulations found.</div>
      )}
    </main>
  );
}

  