'use client';
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { PersonaTrace } from "@/types/quad-persona";

export default function PersonaCard({ trace }: { trace: PersonaTrace }) {
  const [showMeta, setShowMeta] = useState(false);
  const meta = trace.persona;
  return (
    <div className="border rounded p-4 bg-white mb-3">
      <h4 className="text-md font-semibold mb-1">
        Step {trace.step}: {trace.title}
        <span className="ml-2 text-gray-500">({meta.persona_type})</span>
      </h4>
      <div className="mb-2 prose prose-sm max-w-none">
        <ReactMarkdown>{trace.summary}</ReactMarkdown>
      </div>
      <button onClick={() => setShowMeta(!showMeta)} className="text-blue-600 underline text-sm">
        {showMeta ? "Hide Expert Metadata" : "Show Expert Metadata"}
      </button>
      {showMeta && (
        <div className="mt-2 text-xs text-gray-800 bg-gray-50 border rounded p-2">
          <b>Name:</b> {meta.name} <br/>
          <b>Job roles:</b> {meta.job_roles.join(', ')} <br/>
          <b>Skills:</b> {meta.skills.join(', ')} <br/>
          <b>Certifications:</b> {meta.certifications.join(', ')} <br/>
          <b>Training:</b> {meta.training.join(', ')} <br/>
          <b>Education:</b> {meta.education.join(', ')} <br/>
          <b>Research:</b> {meta.research_base.join(', ')}
        </div>
      )}
    </div>
  );
}
