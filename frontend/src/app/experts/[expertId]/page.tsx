import { getExpertById } from '@/lib/api';
import { Expert } from '@/lib/types';
import Link from 'next/link';

interface ExpertPageProps {
  params: {
    expertId: string;
  };
}

export default async function ExpertPage({ params: paramsPromise }: ExpertPageProps) {
  const params = await paramsPromise;
  const expertId = params.expertId;
  let expert: Expert | null = null;
  let error: string | null = null;

  try {
    expert = await getExpertById(expertId);
  } catch (err) {
    console.error(`Error fetching expert ${expertId}:`, err);
    error = `Could not load expert with ID: ${expertId}.`;
  }

  if (error) {
    return (
      <main className="p-8">
        <div className="text-red-600 mb-4">{error}</div>
        <Link href="/" className="text-blue-600 hover:underline">Go back to Home</Link>
      </main>
    );
  }

  if (!expert) {
    return (
      <main className="p-8">
        <div className="text-gray-500">Expert not found or still loading...</div>
        <Link href="/" className="text-blue-600 hover:underline">Go back to Home</Link>
      </main>
    );
  }

  return (
    <main className="container mx-auto p-6 md:p-8 bg-white shadow-xl rounded-lg mt-6 mb-6">
      <h1 className="text-4xl font-bold mb-1 text-gray-900">{expert.name}</h1>
      <p className="text-sm text-gray-500 mb-6">Expert ID: <code className="bg-gray-100 px-1.5 py-0.5 rounded">{expert.id}</code></p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6 mb-8 text-base">
        <div className="flex flex-col">
          <span className="font-semibold text-gray-700">Assigned Role:</span>
          <Link href={`/roles/${expert.role_id}`} className="text-blue-600 hover:text-blue-800 hover:underline mt-1">
            {expert.role_id} {/* TODO: Fetch role name for better display? */}
          </Link>
        </div>
        {expert.location && (
          <div className="flex flex-col">
            <span className="font-semibold text-gray-700">Location:</span>
            <span className="text-gray-800 mt-1">{expert.location}</span>
          </div>
        )}
        {expert.contact && (
          <div className="flex flex-col">
            <span className="font-semibold text-gray-700">Contact:</span>
            <span className="text-gray-800 mt-1">{expert.contact}</span>
          </div>
        )}
      </div>

      {expert.domains && expert.domains.length > 0 && (
        <div className="mb-6 p-4 bg-slate-50 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Expertise Domains</h2>
          <ul className="list-disc list-inside space-y-1 mt-1">
            {expert.domains.map(domain => (
              <li key={domain} className="text-gray-800">{domain}</li>
            ))}
          </ul>
        </div>
      )}

      {expert.provisions && expert.provisions.length > 0 && (
        <div className="mb-6 p-4 bg-slate-50 rounded-lg shadow">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Associated Provisions</h2>
          <ul className="list-disc list-inside space-y-1 mt-1">
            {expert.provisions.map(provisionId => (
              <li key={provisionId}>
                <Link href={`/provisions/${provisionId}`} className="text-blue-600 hover:text-blue-800 hover:underline">
                  {provisionId} {/* TODO: Fetch provision titles for better display? */}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
      
      <div className="mt-8">
        <Link href="/" className="inline-flex items-center text-blue-700 hover:text-blue-900 hover:underline group text-sm">
          <svg className="w-4 h-4 mr-1 transform transition-transform duration-150 group-hover:-translate-x-0.5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clipRule="evenodd"></path></svg>
          Back to Home
        </Link>
      </div>
    </main>
  );
} 