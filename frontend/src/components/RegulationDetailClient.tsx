'use client';

import React, { useState, useMemo } from 'react';
import { Provision } from '@/lib/types';
import GraphViewer from '@/components/GraphViewer';
import NodeDetailPanel from '@/components/NodeDetailPanel';

interface RegulationDetailClientProps {
  initialProvisions: Provision[];
}

export default function RegulationDetailClient({
  initialProvisions,
}: RegulationDetailClientProps) {
  const [selectedProvisionId, setSelectedProvisionId] = useState<string | null>(null);

  // Memoize the selected provision to avoid re-calculating on every render
  const selectedProvision = useMemo(() => {
    if (!selectedProvisionId) return null;
    return initialProvisions.find(p => p.id === selectedProvisionId) || null;
  }, [selectedProvisionId, initialProvisions]);

  const handleNodeClick = (node: Provision) => {
    setSelectedProvisionId(node.id);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="md:col-span-2 bg-gray-50 p-6 rounded-lg shadow">
        <h2 className="text-2xl font-semibold mb-4 text-gray-700 border-b pb-2">Provisions Graph</h2>
        {initialProvisions.length > 0 ? (
          <div className="h-[500px] w-full">
            <GraphViewer 
              nodes={initialProvisions} 
              onNodeClick={handleNodeClick} 
            />
          </div>
        ) : (
          <div className="flex items-center justify-center h-[500px] border-2 border-dashed border-gray-300 rounded-lg">
            <p className="text-gray-500">No provisions found for this regulation.</p>
          </div>
        )}
      </div>
      <div className="bg-gray-50 p-6 rounded-lg shadow">
        <h2 className="text-2xl font-semibold mb-4 text-gray-700 border-b pb-2">Details</h2>
        {selectedProvision ? (
          <NodeDetailPanel node={selectedProvision} />
        ) : (
          <div className="flex items-center justify-center h-full border-2 border-dashed border-gray-300 rounded-lg p-4">
            <p className="text-gray-500 text-center">Select a provision from the graph to see its details.</p>
          </div>
        )}
      </div>
    </div>
  );
} 