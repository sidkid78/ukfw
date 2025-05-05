'use client';

import React, { useState } from 'react';
import { queryNodes } from '../lib/api';
import { KnowledgeNode } from '../lib/types';

export default function QueryPanel({ onResults }: { onResults: (results: KnowledgeNode[]) => void }) {
  const [axis1, setAxis1] = useState('');
  const [axis8, setAxis8] = useState('');
  const [minConfidence, setMinConfidence] = useState(0.8);
  const [persona, setPersona] = useState('');

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const results = await queryNodes({
      axisFilters: { axis1, axis8 },
      minConfidence,
      simulationRole: persona,
      compliance: axis8,
    });
    onResults(results);
  }

  return (
    <form onSubmit={submit} className="space-y-2">
      <input value={axis1} onChange={e => setAxis1(e.target.value)} placeholder="Axis1 (Pillar)" className="input input-bordered" />
      <input value={axis8} onChange={e => setAxis8(e.target.value)} placeholder="Compliance tag" className="input input-bordered" />
      <input type="number" min={0} max={1} step={0.01} value={minConfidence} onChange={e => setMinConfidence(Number(e.target.value))} className="input input-bordered" title="Minimum confidence" />
      <input value={persona} onChange={e => setPersona(e.target.value)} placeholder="Expert persona" className="input input-bordered" />
      <button type="submit" className="btn btn-primary">Query</button>
    </form>
  );
}
