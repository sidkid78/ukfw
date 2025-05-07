'use client'; // Mark this component as a Client Component

import React, { useEffect, useMemo, useState } from 'react';
import dynamic from 'next/dynamic';
// Import Provision type
import { Provision } from '../lib/types'; 
import 'aframe'; // Import aframe

// Define a type for graph links for better type safety
interface GraphLink {
  source: string | number | ForceGraphNode; // Can be ID or node object
  target: string | number | ForceGraphNode; // Can be ID or node object
  label?: string;
  weight?: number;
}

// For react-force-graph node object type
interface ForceGraphNode {
  id?: string | number;
  name?: string;
  pillar?: string;
  val?: number;
  originalNode?: Provision;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  index?: number; 
}

// Dynamically import ForceGraph2D to avoid SSR issues
const ForceGraph2D = dynamic(() => import('react-force-graph').then(mod => mod.ForceGraph2D), {
  ssr: false, 
  loading: () => <p>Loading graph...</p>
});

// Update props to accept Provision[] and a handler for Provision
export default function GraphViewer({ nodes = [], onNodeClick }: { nodes?: Provision[]; onNodeClick?: (node: Provision) => void }) {
  const [isClient, setIsClient] = useState(false);
  const [hoveredNodeId, setHoveredNodeId] = useState<string | number | null>(null);
  const [highlightNodes, setHighlightNodes] = useState(new Set<string | number>());
  const [highlightLinks, setHighlightLinks] = useState(new Set<string>());

  useEffect(() => {
    setIsClient(true);
    // Optional: Check if AFRAME is on window after import for debugging
    // if (typeof window !== 'undefined') {
    //   console.log('window.AFRAME available:', !!window.AFRAME);
    // }
  }, []);
  
  // Transform Provision data into graph format
  const graphData = useMemo(() => {
    if (!Array.isArray(nodes) || nodes.length === 0) {
      return { nodes: [], links: [] };
    }

    const graphNodes = nodes.map(n => ({ 
      id: n.id,
      name: n.title,
      pillar: n.regulation_id, // Used for manual coloring now
      val: n.hierarchy_level ? Math.max(1, 6 - n.hierarchy_level) : 3, 
      originalNode: n, // Keep original node for context
    }));

    const nodeIds = new Set(graphNodes.map(n => n.id));
    const graphLinks: GraphLink[] = [];

    nodes.forEach(n => {
      // Assuming spiderweb_links contains IDs of other provisions
      if (n.spiderweb_links && Array.isArray(n.spiderweb_links)) {
        n.spiderweb_links.forEach((targetId: string) => {
          if (nodeIds.has(targetId) && n.id !== targetId) { // Ensure target exists and not self-linking for this example
            graphLinks.push({ source: n.id, target: targetId });
          }
        });
      }
    });

    return { nodes: graphNodes, links: graphLinks };
  }, [nodes]);

  // Handle node clicks, passing the original Provision data
  const handleNodeClickInternal = (graphNode: ForceGraphNode) => { 
    const originalNode = graphNode.originalNode;
    if (onNodeClick && originalNode) {
      onNodeClick(originalNode);
    }
  };

  const handleNodeHover = (node: ForceGraphNode | null) => {
    const newHighlightNodes = new Set<string | number>();
    const newHighlightLinks = new Set<string>();

    if (node && node.id) {
      setHoveredNodeId(node.id);
      newHighlightNodes.add(node.id);
      graphData.links.forEach(link => {
        const sourceId = typeof link.source === 'object' && link.source.id ? link.source.id : (typeof link.source === 'string' || typeof link.source === 'number' ? link.source : undefined);
        const targetId = typeof link.target === 'object' && link.target.id ? link.target.id : (typeof link.target === 'string' || typeof link.target === 'number' ? link.target : undefined);
        
        if (node.id && (sourceId === node.id || targetId === node.id)) {
          if (sourceId && targetId) { 
            newHighlightLinks.add(`${sourceId}-${targetId}`);
          }
          const neighborId = sourceId === node.id ? targetId : sourceId;
          if (neighborId) { 
             newHighlightNodes.add(neighborId);
          }
        }
      });
    } else {
      setHoveredNodeId(null);
    }
    setHighlightNodes(newHighlightNodes);
    setHighlightLinks(newHighlightLinks);
  };

  if (!isClient) {
    return <p>Loading graph...</p>; // Render placeholder until client-side effects run
  }

  const genericDefaultNodeColor = '#A9A9A9'; // DarkGray for nodes without a pillar or when not otherwise colored
  const defaultLinkColor = 'rgba(180, 180, 180, 0.3)';

  // Helper to generate a color from a string (e.g., pillar ID)
  const colorFromString = (str: string) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
      hash = hash & hash; // Convert to 32bit integer
    }
    const c = (hash & 0x00FFFFFF).toString(16).toUpperCase();
    return "#" + "00000".substring(0, 6 - c.length) + c;
  };

  return (
    <div className="border rounded p-4 bg-white shadow w-full h-[600px]">
      {graphData.nodes.length > 0 ? (
        <ForceGraph2D
          graphData={graphData}
          nodeLabel="name"
          nodeVal="val"
          onNodeHover={handleNodeHover}
          nodeColor={node => {
            const typedNode = node as ForceGraphNode;
            let color = genericDefaultNodeColor; 
            if (typedNode.pillar) {
              color = colorFromString(typedNode.pillar);
            }
            if (hoveredNodeId || highlightNodes.size > 0) {
              return highlightNodes.has(typedNode.id as string | number) 
                ? '#FF0000' // Bright red for highlighted
                : 'rgba(200,200,200,0.3)'; // Dimmed for non-highlighted during hover event
            }
            return color; 
          }}
          linkColor={link => {
            const sourceId = typeof link.source === 'object' && link.source.id ? link.source.id : (typeof link.source === 'string' || typeof link.source === 'number' ? link.source : undefined);
            const targetId = typeof link.target === 'object' && link.target.id ? link.target.id : (typeof link.target === 'string' || typeof link.target === 'number' ? link.target : undefined);
            if (!hoveredNodeId && highlightLinks.size === 0) return defaultLinkColor;
            const linkKey1 = sourceId && targetId ? `${sourceId}-${targetId}` : '-';
            const linkKey2 = sourceId && targetId ? `${targetId}-${sourceId}` : '-';
            return highlightLinks.has(linkKey1) || highlightLinks.has(linkKey2) ? 'rgba(255,0,0,0.7)' : 'rgba(200,200,200,0.2)';
          }}
          linkWidth={link => {
            const sourceId = typeof link.source === 'object' && link.source.id ? link.source.id : (typeof link.source === 'string' || typeof link.source === 'number' ? link.source : undefined);
            const targetId = typeof link.target === 'object' && link.target.id ? link.target.id : (typeof link.target === 'string' || typeof link.target === 'number' ? link.target : undefined);
            if (!hoveredNodeId && highlightLinks.size === 0) return 1;
            const linkKey1 = sourceId && targetId ? `${sourceId}-${targetId}` : '-';
            const linkKey2 = sourceId && targetId ? `${targetId}-${sourceId}` : '-';
            return highlightLinks.has(linkKey1) || highlightLinks.has(linkKey2) ? 2 : 0.5;
          }}
          linkDirectionalParticles={graphData.links.length > 0 ? 1 : 0} // Only show particles if links exist
          linkDirectionalParticleWidth={1.5}
          onNodeClick={handleNodeClickInternal} // Use the wrapped handler
          width={800} // Adjust as needed, or make responsive
          height={580} // Adjust as needed
        />
      ) : (
        <p className="text-gray-500">No graph data available.</p>
      )}
    </div>
  );
}
