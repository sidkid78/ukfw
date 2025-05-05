'use client';

import React from 'react';
import { ProvenanceMetadata } from '../lib/types';

export default function ProvenancePanel({ metadata }: { metadata: ProvenanceMetadata }) {
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
