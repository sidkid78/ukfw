'use client';

import QueryPanel from '../../components/QueryPanel';
import { useState } from 'react';
import type { Provision } from '../../lib/types';

export default function QueryPage() {
  const [results, setResults] = useState<Provision[]>([]);
  return (
    <main className="p-8">
      <h2 className="text-2xl font-semibold mb-2">Advanced Query</h2>
      <QueryPanel onResults={setResults} />
      <div className="mt-4">
        {results.length > 0 ? (
          <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto">{JSON.stringify(results, null, 2)}</pre>
        ) : (
          <div className="text-gray-500">No results yet.</div>
        )}
      </div>
    </main>
  );
}
