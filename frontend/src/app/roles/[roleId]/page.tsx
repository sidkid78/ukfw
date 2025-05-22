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

  if (error) {
    return (
      <main className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Error:</strong>
          <span className="block sm:inline"> {error}</span>
        </div>
      </main>
    );
  }

  if (!role) {
    return (
      <main className="container mx-auto px-4 py-8">
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded relative" role="alert">
          <strong className="font-bold">Loading:</strong>
          <span className="block sm:inline"> Loading role data... If this persists, the role may not exist.</span>
        </div>
      </main>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="p-6">
          <h1 className="text-3xl font-bold mb-2 text-gray-800">Role: {role.name}</h1>
          <p className="text-sm text-gray-500 mb-1">ID: <code className="bg-gray-100 px-1 rounded">{role.id}</code></p>
          {role.description && 
            <p className="mb-4 text-gray-700 text-lg leading-relaxed italic">{role.description}</p>}
          {role.jurisdiction && 
            <p className="mb-4 text-gray-600"><span className="font-semibold">Jurisdiction:</span> {role.jurisdiction}</p>}
          
          <hr className="my-6" />

          <div className="mb-6">
            <h2 className="text-2xl font-semibold mb-3 text-gray-700">Expertise Domains</h2>
            {role.expertise_domains?.length > 0 ? (
              <ul className="list-disc list-inside space-y-1 text-gray-600">
                {role.expertise_domains.map(domain => <li key={domain}>{domain}</li>)}
              </ul>
            ) : (
              <p className="text-gray-500">No specific expertise domains listed for this role.</p>
            )}
          </div>

          <hr className="my-6" />

          <div>
            <h2 className="text-2xl font-semibold mb-3 text-gray-700">Responsible Provisions</h2>
            {role.provisions?.length > 0 ? (
              <ul className="list-disc list-inside space-y-1">
                {role.provisions.map(provId => (
                  <li key={provId}>
                    <Link href={`/provisions/${provId}`} className="text-blue-600 hover:text-blue-800 hover:underline">
                      View Provision: {provId}
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No provisions are directly assigned to this role.</p>
            )}
          </div>
        </div>
      </div>
    </main>
  );
} 