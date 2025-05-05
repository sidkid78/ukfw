'use client'; // Mark this page as a Client Component

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation'; // Import for navigation
import { getRegulation, queryProvisions } from '../../../lib/api';
import GraphViewer from '../../../components/GraphViewer';
import { Regulation, Provision } from '../../../lib/types';
import Link from 'next/link';

export default function RegulationPage({ params }: { params: { regulationId: string } }) {
  const router = useRouter();
  const regulationId = params.regulationId;

  const [regulation, setRegulation] = useState<Regulation | null>(null);
  const [provisions, setProvisions] = useState<Provision[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      setLoading(true); setError(null);
      try {
        // Fetch regulation details
        const fetchedRegulation = await getRegulation(regulationId);
        setRegulation(fetchedRegulation);
        if (fetchedRegulation) {
          // Fetch associated provisions
          const fetchedProvisions = await queryProvisions({ regulation_id: fetchedRegulation.id });
          setProvisions(fetchedProvisions);
        }
      } catch (err) {
        setError('Failed to load regulation data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    if (regulationId) {
      loadData();
    }
  }, [regulationId]);

  // Define the click handler for provisions in the graph
  const handleProvisionClick = (provision: Provision) => {
    console.log('Provision clicked:', provision);
    router.push(`/provisions/${provision.id}`);
  };

  if (loading) return <main className="p-8">Loading...</main>;
  if (error) return <main className="p-8"><div className="text-red-500">{error}</div></main>;
  if (!regulation) return <main className="p-8">Regulation not found.</main>;

  return (
    <main className="p-8">
      <h2 className="text-2xl font-semibold mb-2">Regulation: {regulation.title} ({regulation.id})</h2>
      <p className="mb-1 text-sm text-gray-600">Jurisdiction: {regulation.jurisdiction}</p>
      <p className="mb-4 text-sm text-gray-600">Pillar: {regulation.pillar}</p>
      <p className="mb-4">{regulation.description}</p>
      
      <h3 className="text-lg font-semibold mt-6 mb-2">Provisions</h3>
      {provisions.length > 0 ? (
          <ul className="list-disc ml-5 mb-6 space-y-1">
              {provisions.map(prov => (
                  <li key={prov.id}>
                      <Link href={`/provisions/${prov.id}`} className="text-blue-600 hover:underline">
                          {prov.section} - {prov.title}
                      </Link>
                  </li>
              ))}
          </ul>
      ) : (
          <p className="text-gray-500 mb-6">No provisions found for this regulation.</p>
      )}

      <GraphViewer nodes={provisions} onNodeClick={handleProvisionClick} />
    </main>
  );
}
