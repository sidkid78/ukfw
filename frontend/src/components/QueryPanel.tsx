'use client';

import React, { useState } from 'react';
import { queryProvisions } from '../lib/api';
import { Provision } from '../lib/types';

export default function QueryPanel({ onResults }: { onResults: (results: Provision[]) => void }) {
  const [regulationId, setRegulationId] = useState('');
  const [complianceTag, setComplianceTag] = useState('');
  const [minConfidence, setMinConfidence] = useState(0.8);
  const [roleId, setRoleId] = useState('');

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const results = await queryProvisions({
      regulation_id: regulationId || undefined,
      compliance_tag: complianceTag || undefined,
      min_confidence: minConfidence,
      role_id: roleId || undefined,
    });
    onResults(results);
  }

  return (
    <form onSubmit={submit} className="space-y-2">
      <input value={regulationId} onChange={e => setRegulationId(e.target.value)} placeholder="Regulation ID (e.g., PL16)" className="input input-bordered" />
      <input value={complianceTag} onChange={e => setComplianceTag(e.target.value)} placeholder="Compliance tag (e.g., GDPR)" className="input input-bordered" />
      <input type="number" min={0} max={1} step={0.01} value={minConfidence} onChange={e => setMinConfidence(Number(e.target.value))} className="input input-bordered" title="Minimum confidence" />
      <input value={roleId} onChange={e => setRoleId(e.target.value)} placeholder="Role ID (e.g., ROLE_TP)" className="input input-bordered" />
      <button type="submit" className="btn btn-primary">Query Provisions</button>
    </form>
  );
}
