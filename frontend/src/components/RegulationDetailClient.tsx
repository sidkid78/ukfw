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
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="md:col-span-2">
        <h2 className="text-2xl font-semibold mb-2">Provisions Graph</h2>
        {initialProvisions.length > 0 ? (
          <GraphViewer 
            nodes={initialProvisions} 
            onNodeClick={handleNodeClick} 
          />
        ) : (
          <p>No provisions found for this regulation.</p>
        )}
      </div>
      <div>
        <h2 className="text-2xl font-semibold mb-2">Details</h2>
        <NodeDetailPanel node={selectedProvision} />
      </div>
    </div>
  );
} 