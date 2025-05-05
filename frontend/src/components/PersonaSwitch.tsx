'use client';

import React from 'react';

export default function PersonaSwitch({ personas, value, onChange }: { personas: string[]; value: string; onChange: (persona: string) => void }) {
  return (
    <select value={value} onChange={e => onChange(e.target.value)} className="select select-bordered" title="Select a persona">
      <option value="">Default Expert</option>
      {personas.map((persona: string) => (
        <option key={persona} value={persona}>{persona}</option>
      ))}
    </select>
  );
}
