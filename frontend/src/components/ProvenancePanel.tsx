'use client';

import React from 'react';

// Define a simple type for the expected metadata structure
interface PanelMetadata {
  provenance?: string;
  audit_trail?: unknown[];
  // Add other expected fields if necessary
}

export default function ProvenancePanel({ metadata }: { metadata: PanelMetadata | null | undefined }) {
  if (!metadata) return null;
  return (
    <div className="mt-2">
      {metadata.provenance && (
        <div>
          <b>Source:</b> {metadata.provenance}
        </div>
      )}
      {metadata.audit_trail && (
        <pre className="bg-gray-100 p-2 rounded text-xs mt-1 overflow-x-auto">{JSON.stringify(metadata.audit_trail, null, 2)}</pre>
      )}
    </div>
  );
}
