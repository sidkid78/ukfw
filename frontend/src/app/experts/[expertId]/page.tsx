import { getExpertById, getRoleById } from '../../../lib/api';
import { Expert, Role } from '../../../lib/types';
import Link from 'next/link';

// This page will fetch data for a specific Expert
export default async function ExpertPage({ params }: { params: { expertId: string } }) {
  // Await params before accessing properties
  const awaitedParams = await params;
  let expert: Expert | null = null;
  let role: Role | null = null; // To display role name
  let error: string | null = null;

  try {
    // Use awaitedParams.expertId
    expert = await getExpertById(awaitedParams.expertId);
    // Fetch the role details to display the role name
    if (expert?.role_id) {
      try {
        role = await getRoleById(expert.role_id);
      } catch (roleError) {
        console.warn(`Could not fetch role ${expert.role_id} for expert ${expert.id}`, roleError);
      }
    }
  } catch (err) {
    console.error("Error fetching expert:", err);
    // Use awaitedParams.expertId in error message
    error = `Could not load expert with ID: ${awaitedParams.expertId}. Please check the backend or the ID.`;
  }

  return (
    <main className="p-8">
      {error && <div className="text-red-600 mb-4">{error}</div>}
      
      {expert ? (
        <div>
          <h1 className="text-3xl font-bold mb-2">Expert: {expert.name}</h1>
          <p className="mb-1 text-gray-600">ID: <code>{expert.id}</code></p>
          
          {/* Display Role */}
          {expert.role_id && (
            <p className="mb-3">
              Role: {' '}
              <Link href={`/roles/${expert.role_id}`} className="text-blue-600 hover:underline">
                {role?.name ?? expert.role_id} {/* Show role name if fetched, else ID */}
              </Link>
            </p>
          )}
          
          {expert.location && <p className="mb-3">Location: {expert.location}</p>}
          {expert.contact && <p className="mb-3">Contact: {expert.contact}</p>}
          
          <div className="mb-4">
            <h2 className="text-xl font-semibold mb-1">Expertise Domains</h2>
            {expert.domains?.length > 0 ? (
              <ul className="list-disc ml-5">
                {expert.domains.map(domain => <li key={domain}>{domain}</li>)}
              </ul>
            ) : (
              <p className="text-gray-500">No specific domains listed.</p>
            )}
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-1">Assigned Provisions</h2>
            {expert.provisions?.length > 0 ? (
              <ul className="list-disc ml-5">
                {/* TODO: Fetch provision details to show titles? */}
                {expert.provisions.map(provId => (
                  <li key={provId}>
                    <Link href={`/provisions/${provId}`} className="text-blue-600 hover:underline">
                      {provId} 
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No provisions explicitly assigned to this expert.</p>
            )}
          </div>

        </div>
      ) : (
        !error && <div className="text-gray-500">Loading expert data...</div>
      )}
    </main>
  );
} 