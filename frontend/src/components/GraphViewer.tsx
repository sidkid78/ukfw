'use client'; // Mark this component as a Client Component

import React, { useMemo } from 'react';
import dynamic from 'next/dynamic';
// Import Provision type
import { Provision } from '../lib/types'; 

// Define a type for graph links for better type safety
interface GraphLink {
  source: string | number;
  target: string | number;
  label?: string;
  weight?: number;
}

// Dynamically import ForceGraph2D to avoid SSR issues
const ForceGraph2D = dynamic(() => import('react-force-graph').then(mod => mod.ForceGraph2D), {
  ssr: false, 
  loading: () => <p>Loading graph...</p>
});

// Update props to accept Provision[] and a handler for Provision
export default function GraphViewer({ nodes = [], onNodeClick }: { nodes?: Provision[]; onNodeClick?: (node: Provision) => void }) {
  
  // Transform Provision data into graph format
  const graphData = useMemo(() => {
    // Add explicit check for Array type
    if (!Array.isArray(nodes) || nodes.length === 0) {
      return { nodes: [], links: [] };
    }

    // Map Provision properties to graph node properties
    const graphNodes = nodes.map(n => ({ 
      id: n.id, // Use Provision id
      name: n.title, // Use Provision title as name
      pillar: n.regulation_id, // Use regulation_id as pillar/grouping info
      // originalNode: n, // Pass the original Provision object
    }));

    // Links might need adjustment depending on how Provisions link to each other
    // Assuming Provisions don't directly link in this model, keep links empty for now
    const graphLinks: GraphLink[] = []; // Explicitly type graphLinks
    // const graphLinks: GraphLink[] = nodes.flatMap(n =>
    //   (n.links || []).map(l => ({
    //     source: n.id, // Use Provision id
    //     target: l.target_node_id,
    //     label: l.relationship_type,
    //     weight: l.weight || 1,
    //   }))
    // );

    return { nodes: graphNodes, links: graphLinks };

  }, [nodes]);

  // Handle node clicks, passing the original Provision data
  // Remove unused event parameter entirely
  const handleNodeClick = (graphNode: { id?: string | number }) => { 
    // Find the original Provision object
    const originalNode = nodes.find(n => n.id === graphNode.id); 
    if (onNodeClick && originalNode) {
      onNodeClick(originalNode); // Pass the Provision object
    }
  };

  return (
    <div className="border rounded p-4 bg-white shadow w-full h-[600px]">
      {graphData.nodes.length > 0 ? (
        <ForceGraph2D
          graphData={graphData}
          nodeLabel="name"
          nodeAutoColorBy="pillar" // Color nodes by regulation ID
          linkLabel="label"
          linkDirectionalParticles={graphData.links.length > 0 ? 1 : 0} // Only show particles if links exist
          linkDirectionalParticleWidth={1.5}
          onNodeClick={handleNodeClick} // Use the wrapped handler
          width={800} // Adjust as needed, or make responsive
          height={580} // Adjust as needed
        />
      ) : (
        <p className="text-gray-500">No graph data available.</p>
      )}
    </div>
  );
}
