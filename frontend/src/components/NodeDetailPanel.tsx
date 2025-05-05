'use client';

import React from 'react';
// import AxisInspector from './AxisInspector';
import ComplianceBadge from './ComplianceBadge';
// import ProvenancePanel from './ProvenancePanel';
import { Provision } from '../lib/types';
import Link from 'next/link';

export default function NodeDetailPanel({ node }: { node: Provision | null }) {
  if (!node) return <div className="p-4">Select a node to see details.</div>;
  return (
    <div className="border rounded p-4 bg-white shadow">
      <h2 className="text-xl font-bold mb-2">{node.title}</h2>
      <p className="mb-2">{node.text}</p>
      <div className="mb-2">Provision ID: <code>{node.id}</code></div>
      <div className="mb-2">Regulation: <code>{node.regulation_id}</code></div>
      
      {/* TODO: Add Section and Hierarchy Level display if available */}
      {node.section && <div className="mb-2">Section: <code>{node.section}</code></div>}
      {node.hierarchy_level !== undefined && <div className="mb-2">Hierarchy Level: <code>{node.hierarchy_level}</code></div>}
      {node.parent_id && <div className="mb-2">Parent Provision: <code>{node.parent_id}</code></div>}

      {/* TODO: Update AxisInspector if its props or logic need changes for Provision */}
      {/* <AxisInspector axes={node.axes} onAxisSelect={() => {}} /> */}
      
      {/* Pass crosswalks (mapped from compliance_mapping/axis8) */}
      {/* Provide default empty array if undefined */}
      <ComplianceBadge tags={node.crosswalks ?? []} />
      
      {/* TODO: Update ProvenancePanel if its props or logic need changes for Provision */}
      {/* <ProvenancePanel metadata={node.metadata} /> */}
      
      {/* TODO: Update how confidence is derived from Provision model */}
      {/* <div className="mt-2">
        <b>Confidence:</b> {((node.axes?.axis9 ?? 0) * 100).toFixed(1)}%
      </div> */}
      
      {/* Display roles from Provision (link to Role detail page) */}
      {node.roles_responsible?.length > 0 && (
        <div className="mt-2">
          <b>Responsible Roles:</b>
          <ul className="list-disc ml-5">
            {node.roles_responsible.map(roleId => (
              <li key={roleId}>
                <Link href={`/roles/${roleId}`} className="text-blue-600 hover:underline">
                  {roleId} {/* TODO: Could fetch role names here if desired */}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
      {/* Experts are linked TO provisions, not FROM them - remove display here */}
      {/* {node.experts_assigned?.length > 0 && (...)} */}
      
      {/* Display other Provision fields */}
      <div className="mt-2">
        <b>Jurisdiction:</b> {node.jurisdiction ?? 'N/A'}
      </div>
      {/* Version is not on Provision type - remove display */}
      {/* <div className="mt-2">
        <b>Version:</b> {node.version ?? 'N/A'}
      </div> */}
       {node.tags?.length > 0 && (
        <div className="mt-2">
          <b>Tags:</b> {node.tags.join(', ')}
        </div>
      )}
       {/* Display crosswalks, spiderweb links, octopus refs if needed */}
       {node.crosswalks?.length > 0 && (
        <div className="mt-2">
          <b>Crosswalks:</b> {node.crosswalks.join(', ')}
        </div>
      )}
      {node.spiderweb_links?.length > 0 && (
        <div className="mt-2">
          <b>Spiderweb Links:</b> {node.spiderweb_links.join(', ')}
        </div>
      )}
       {node.octopus_refs?.length > 0 && (
        <div className="mt-2">
          <b>Octopus Refs:</b> {node.octopus_refs.join(', ')}
        </div>
      )}
    </div>
  );
}
