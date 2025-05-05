import { getRoleById } from '../../../lib/api';
import { Role } from '../../../lib/types';
import Link from 'next/link';

// This page will fetch data for a specific Role
export default async function RolePage({ params }: { params: { roleId: string } }) {
  // Await params before accessing properties
  const awaitedParams = await params;
  let role: Role | null = null;
  let error: string | null = null;

  try {
    // Use awaitedParams.roleId
    role = await getRoleById(awaitedParams.roleId);
  } catch (err) {
    console.error("Error fetching role:", err);
    // Use awaitedParams.roleId in error message too
    error = `Could not load role with ID: ${awaitedParams.roleId}. Please check the backend or the ID.`;
  }

  return (
    <main className="p-8">
      {error && <div className="text-red-600 mb-4">{error}</div>}
      
      {role ? (
        <div>
          <h1 className="text-3xl font-bold mb-2">Role: {role.name}</h1>
          <p className="mb-1 text-gray-600">ID: <code>{role.id}</code></p>
          {role.description && <p className="mb-3 italic text-gray-700">{role.description}</p>}
          {role.jurisdiction && <p className="mb-3">Jurisdiction: {role.jurisdiction}</p>}
          
          <div className="mb-4">
            <h2 className="text-xl font-semibold mb-1">Expertise Domains</h2>
            {role.expertise_domains?.length > 0 ? (
              <ul className="list-disc ml-5">
                {role.expertise_domains.map(domain => <li key={domain}>{domain}</li>)}
              </ul>
            ) : (
              <p className="text-gray-500">No specific expertise domains listed.</p>
            )}
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-1">Responsible Provisions</h2>
            {role.provisions?.length > 0 ? (
              <ul className="list-disc ml-5">
                {/* This list is populated by _link_entities on the backend */}
                {role.provisions.map(provId => (
                  <li key={provId}>
                    <Link href={`/provisions/${provId}`} className="text-blue-600 hover:underline">
                      {provId}
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No provisions directly assigned to this role.</p>
            )}
          </div>
          
          {/* TODO: Add section to list Experts assigned to this Role? */}

        </div>
      ) : (
        !error && <div className="text-gray-500">Loading role data...</div>
      )}
    </main>
  );
} 