import React from 'react';
import { getRegulation, queryProvisions } from '@/lib/api';
import { Regulation, Provision } from '@/lib/types';
import RegulationDetailClient from '@/components/RegulationDetailClient';
// import GraphViewer from '@/components/GraphViewer'; // Placeholder
// import NodeDetailPanel from '@/components/NodeDetailPanel'; // Placeholder

interface RegulationPageProps {
  params: {
    regulationId: string;
  };
}

export default async function RegulationPage({ params: paramsPromise }: RegulationPageProps) {
  const params = await paramsPromise;
  const regulationId = params.regulationId;
  let regulation: Regulation | null = null;
  let provisions: Provision[] = [];
  let error: string | null = null;

  try {
    regulation = await getRegulation(regulationId);
    if (regulation) {
      provisions = await queryProvisions({ regulation_id: regulationId });
    } else {
      error = `Regulation with ID ${regulationId} not found.`;
    }
  } catch (e) {
    console.error(`Failed to load data for regulation ${regulationId}:`, e);
    error = e instanceof Error ? e.message : 'Failed to load regulation data.';
  }

  if (error) {
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Error</h1>
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (!regulation) {
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">Regulation Not Found</h1>
        <p>The regulation with ID {regulationId} could not be loaded.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-2">{regulation.title}</h1>
      <p className="text-sm text-gray-600 mb-1">ID: {regulation.id}</p>
      {regulation.description && <p className="mb-4 text-gray-700">{regulation.description}</p>}
      
      <RegulationDetailClient initialProvisions={provisions} />
    </div>
  );
}
