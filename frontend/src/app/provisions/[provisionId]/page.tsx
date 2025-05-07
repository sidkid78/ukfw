import { getProvision } from '@/lib/api'; // Corrected path assuming api.ts is in @/lib
import { Provision } from '@/lib/types';   // Corrected path
import Link from 'next/link';
import ComplianceBadge from '@/components/ComplianceBadge'; // Assuming this component exists

// Props for the page component, including the dynamic parameter
interface ProvisionPageProps {
  params: {
    provisionId: string;
  };
}

export default async function ProvisionPage({ params: paramsPromise }: ProvisionPageProps) {
  const params = await paramsPromise; // Await params
  const provisionId = params.provisionId;
  let provision: Provision | null = null;
  let error: string | null = null;

  try {
    provision = await getProvision(provisionId);
  } catch (err) {
    console.error(`Error fetching provision ${provisionId}:`, err);
    error = `Could not load provision with ID: ${provisionId}.`;
  }

  if (error) {
    return (
      <main className="p-8">
        <div className="text-red-600 mb-4">{error}</div>
        <Link href="/" className="text-blue-600 hover:underline">Go back to Home</Link>
      </main>
    );
  }

  if (!provision) {
    return (
      <main className="p-8">
        <div className="text-gray-500">Provision not found or still loading...</div>
        <Link href="/" className="text-blue-600 hover:underline">Go back to Home</Link>
      </main>
    );
  }

  return (
    <main className="container mx-auto p-6 md:p-8 bg-white shadow-xl rounded-lg mt-6 mb-6">
      <h1 className="text-4xl font-bold mb-4 text-gray-900">{provision.title}</h1>
      <p className="text-lg text-gray-700 mb-8 leading-relaxed">{provision.text}</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6 mb-8 text-base">
        <div className="flex flex-col"><span className="font-semibold text-gray-700">ID:</span> <code className="bg-gray-100 px-2 py-1 rounded text-gray-800 mt-1">{provision.id}</code></div>
        <div className="flex flex-col"><span className="font-semibold text-gray-700">Regulation:</span> <Link href={`/regulations/${provision.regulation_id}`} className="text-blue-600 hover:text-blue-800 hover:underline mt-1">{provision.regulation_id}</Link></div>
        {provision.section && <div className="flex flex-col"><span className="font-semibold text-gray-700">Section:</span> <code className="bg-gray-100 px-2 py-1 rounded text-gray-800 mt-1">{provision.section}</code></div>}
        {provision.hierarchy_level !== undefined && <div className="flex flex-col"><span className="font-semibold text-gray-700">Hierarchy Level:</span> <code className="bg-gray-100 px-2 py-1 rounded text-gray-800 mt-1">{provision.hierarchy_level}</code></div>}
        {provision.parent_id && <div className="flex flex-col"><span className="font-semibold text-gray-700">Parent Provision:</span> <code className="bg-gray-100 px-2 py-1 rounded text-gray-800 mt-1">{provision.parent_id}</code></div>} {/* Link this later if needed */}
        {provision.jurisdiction && <div className="flex flex-col"><span className="font-semibold text-gray-700">Jurisdiction:</span> <span className="text-gray-800 mt-1">{provision.jurisdiction}</span></div>}
      </div>

      {provision.tags && provision.tags.length > 0 && (
        <div className="mb-6 p-4 bg-slate-50 rounded-lg shadow"> 
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Tags</h2> 
          <div className="flex flex-wrap gap-2">
            {provision.tags.map(tag => (
              <span key={tag} className="bg-sky-100 text-sky-800 px-3 py-1 rounded-full text-sm font-medium">{tag}</span>
            ))}
          </div>
        </div>
      )}
      
      {provision.crosswalks && provision.crosswalks.length > 0 && (
         <div className="mb-6 p-4 bg-slate-50 rounded-lg shadow"> 
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Compliance Crosswalks</h2> 
          <ComplianceBadge tags={provision.crosswalks} />
        </div>
      )}

      {provision.roles_responsible && provision.roles_responsible.length > 0 && (
        <div className="mb-6 p-4 bg-slate-50 rounded-lg shadow"> 
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Responsible Roles</h2> 
          <ul className="list-disc list-inside space-y-1 mt-1"> 
            {provision.roles_responsible.map(roleId => (
              <li key={roleId}>
                <Link href={`/roles/${roleId}`} className="text-blue-600 hover:text-blue-800 hover:underline">
                  {roleId} {/* You might want to fetch role names for better display */}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {/* Placeholder for other detailed sections if needed */}
      {/* For example, Spiderweb links, Octopus refs, metadata like confidence */}
      {/* 
      {provision.metadata?.confidence && (
        <div className="mt-4 p-3 bg-gray-50 rounded">
          <h3 className="font-semibold text-gray-700">Confidence Score:</h3>
          <p className="text-lg text-green-600">{(provision.metadata.confidence * 100).toFixed(1)}%</p>
        </div>
      )}
      */}

      <div className="mt-8">
        <Link href={`/regulations/${provision.regulation_id}`} className="inline-flex items-center text-blue-700 hover:text-blue-900 hover:underline group text-sm">
          <svg className="w-4 h-4 mr-1 transform transition-transform duration-150 group-hover:-translate-x-0.5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clipRule="evenodd"></path></svg>
          Back to {provision.regulation_id} Overview
        </Link>
      </div>    
    </main>
  );
}       

