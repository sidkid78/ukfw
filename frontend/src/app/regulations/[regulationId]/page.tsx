'use client';

import { useEffect, useState, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import { getRegulation, queryProvisions, runQuadReasoning } from '@/lib/api';
import { Regulation, Provision, ReasoningTrace } from '@/lib/types';
import GraphViewer from '@/components/GraphViewer';

interface RegulationPageProps {
  params: {
    regulationId: string;
  };
}

type RegulationState = {
  data: Regulation | null;
  provisions: Provision[];
  isLoading: boolean;
  error: string | null;
};

type ReasoningState = {
  query: string;
  result: ReasoningTrace | null;
  isLoading: boolean;
  error: string | null;
};

const DEFAULT_QUERY_MAP = {
  regulation: (title: string) => `What are the key implications of ${title}?`,
  provision: (title: string) => `Analyze risks and mitigations for provision: "${title}"`,
  fallback: 'Enter your query for the regulation.'
};

export default function RegulationPage({ params }: RegulationPageProps) {
  const { regulationId } = params;
  const [regulationState, setRegulationState] = useState<RegulationState>({
    data: null,
    provisions: [],
    isLoading: true,
    error: null
  });
  const [reasoningState, setReasoningState] = useState<ReasoningState>({
    query: '',
    result: null,
    isLoading: false,
    error: null
  });
  const [selectedProvision, setSelectedProvision] = useState<Provision | null>(null);

  const getDefaultQuery = useCallback(() => {
    if (selectedProvision) {
      const excerpt = selectedProvision.text.length > 200 
        ? `${selectedProvision.text.substring(0, 200)}...`
        : selectedProvision.text;
      return `${DEFAULT_QUERY_MAP.provision(selectedProvision.title)} Details: "${excerpt}"`;
    }
    return regulationState.data 
      ? DEFAULT_QUERY_MAP.regulation(regulationState.data.title)
      : DEFAULT_QUERY_MAP.fallback;
  }, [regulationState.data, selectedProvision]);

  useEffect(() => {
    const fetchRegulationData = async () => {
      try {
        const [regData, provData] = await Promise.all([
          getRegulation(regulationId),
          queryProvisions({ regulation_id: regulationId })
        ]);

        if (!regData) throw new Error('Regulation not found');
        
        setRegulationState(prev => ({
          ...prev,
          data: regData,
          provisions: provData,
          isLoading: false
        }));
        setReasoningState(prev => ({ ...prev, query: DEFAULT_QUERY_MAP.regulation(regData.title) }));
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to fetch regulation data';
        setRegulationState(prev => ({
          ...prev,
          error: errorMessage,
          isLoading: false
        }));
      }
    };

    fetchRegulationData();
  }, [regulationId]);

  const handleRunReasoning = async () => {
    if (!reasoningState.query.trim()) {
      setReasoningState(prev => ({ ...prev, error: 'Query cannot be empty' }));
      return;
    }

    setReasoningState(prev => ({ ...prev, isLoading: true, error: null, result: null }));
    
    try {
      const result = await runQuadReasoning(
        reasoningState.query,
        selectedProvision?.id
      );
      setReasoningState(prev => ({ ...prev, result }));
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Reasoning process failed';
      setReasoningState(prev => ({ ...prev, error: errorMessage }));
    } finally {
      setReasoningState(prev => ({ ...prev, isLoading: false }));
    }
  };

  const handleProvisionSelection = (provision: Provision | null) => {
    setSelectedProvision(provision);
    setReasoningState(prev => ({ ...prev, query: getDefaultQuery() }));
  };

  if (regulationState.isLoading) return <LoadingState message="Loading regulation details..." />;
  if (regulationState.error) return <ErrorState message={regulationState.error} />;
  if (!regulationState.data) return <ErrorState message="Regulation not found" />;

  return (
    <div className="container mx-auto p-4 space-y-8">
      <RegulationHeader regulation={regulationState.data} />
      
      <section className="my-8 p-4 border rounded-lg shadow">
        <h2 className="text-2xl font-semibold mb-4">AI Reasoning</h2>
        
        <ProvisionContextPreview provision={selectedProvision} />
        <ReasoningInput
          query={reasoningState.query}
          onQueryChange={(value) => setReasoningState(prev => ({ ...prev, query: value }))}
          selectedProvision={selectedProvision}
          regulation={regulationState.data}
          defaultQuery={getDefaultQuery()}
        />
        <ReasoningControls
          isLoading={reasoningState.isLoading}
          onRun={handleRunReasoning}
        />
        <ReasoningStatus 
          error={reasoningState.error}
          isLoading={reasoningState.isLoading}
        />
        {reasoningState.result && <ReasoningResultDisplay result={reasoningState.result} />}
      </section>

      {selectedProvision && (
        <SelectedProvisionDetail
          provision={selectedProvision}
          onClose={() => handleProvisionSelection(null)}
        />
      )}

      <ProvisionGraphSection
        provisions={regulationState.provisions}
        regulationTitle={regulationState.data.title}
        onNodeClick={handleProvisionSelection}
      />
    </div>
  );
}

// Subcomponents
const LoadingState = ({ message }: { message: string }) => (
  <div className="container mx-auto p-4">{message}</div>
);

const ErrorState = ({ message }: { message: string }) => (
  <div className="container mx-auto p-4 text-red-500">Error: {message}</div>
);

const RegulationHeader = ({ regulation }: { regulation: Regulation }) => (
  <section>
    <h1 className="text-3xl font-bold mb-2">{regulation.title}</h1>
    <p className="text-gray-600 mb-1">ID: {regulation.id}</p>
    <p className="text-gray-700 mb-4">{regulation.description}</p>
    {regulation.pillar && <p className="text-sm text-gray-500">Pillar: {regulation.pillar}</p>}
  </section>
);

const ProvisionContextPreview = ({ provision }: { provision: Provision | null }) => (
  provision && (
    <div className="mb-4 p-3 border border-gray-200 rounded-md bg-gray-50 max-h-48 overflow-y-auto">
      <h4 className="text-sm font-semibold text-gray-600 mb-1">
        Context from selected provision: &quot;{provision.title}&quot;
      </h4>
      <div className="prose prose-sm max-w-none text-gray-700">
        <ReactMarkdown>{provision.text}</ReactMarkdown>
      </div>
    </div>
  )
);

const ReasoningInput = ({
  query,
  onQueryChange,
  selectedProvision,
  regulation,
  defaultQuery
}: {
  query: string;
  onQueryChange: (value: string) => void;
  selectedProvision: Provision | null;
  regulation: Regulation;
  defaultQuery: string;
}) => (
  <div className="space-y-4">
    <div>
      <label htmlFor="reasoningQuery" className="block text-sm font-medium text-gray-700 mb-1">
        {selectedProvision 
          ? `Query based on: "${selectedProvision.title}"`
          : `Query for Regulation: "${regulation.title}"`}
      </label>
      <textarea
        id="reasoningQuery"
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        placeholder={selectedProvision ? `Analyze: ${selectedProvision.title}` : defaultQuery}
        rows={3}
        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      />
    </div>
  </div>
);

const ReasoningControls = ({ isLoading, onRun }: { isLoading: boolean; onRun: () => void }) => (
  <button
    onClick={onRun}
    disabled={isLoading}
    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition duration-150 ease-in-out"
  >
    {isLoading ? 'Analyzing...' : 'Analyze with AI'}
  </button>
);

const ReasoningStatus = ({ error, isLoading }: { error: string | null; isLoading: boolean }) => (
  <>
    {error && <p className="text-red-500">Error: {error}</p>}
    {isLoading && <p>Loading analysis results...</p>}
  </>
);

const ReasoningResultDisplay = ({ result }: { result: ReasoningTrace }) => (
  <div className="mt-4 p-4 bg-gray-50 rounded-md border border-gray-200">
    <h3 className="text-xl font-semibold mb-2">Analysis Result:</h3>
    <p className="text-gray-800 mb-2">
      <strong>Summary:</strong> {result.final_response_summary || 'No summary provided.'}
    </p>
    <div className="text-sm text-gray-600 space-y-1">
      <p><strong>Confidence:</strong> {result.overall_confidence_score?.toFixed(2) ?? 'N/A'}</p>
      <p>Task ID: {result.task_id}</p>
    </div>
    {result.steps?.length > 0 && <ReasoningSteps steps={result.steps} />}
  </div>
);

const ReasoningSteps = ({ steps }: { steps: ReasoningTrace['steps'] }) => (
  <div className="mt-4 pt-3 border-t border-gray-300">
    <h4 className="text-md font-semibold text-gray-700 mb-2">Reasoning Process:</h4>
    <ul className="space-y-3">
      {steps.map((step, index) => (
        <ReasoningStepItem key={step.step_id || index} step={step} index={index} />
      ))}
    </ul>
  </div>
);

const ReasoningStepItem = ({ step, index }: { step: ReasoningTrace['steps'][number]; index: number }) => {
  const statusColor = step.status === 'success' ? 'text-green-600' : 'text-red-600';
  const statusMessage = step.status === 'success' ? 'Completed' : 'Failed';

  return (
    <li className="p-3 bg-white border border-gray-200 rounded-md shadow-sm">
      <p className="text-sm font-semibold text-indigo-600">
        Step {index + 1}: {step.persona_display_name}
      </p>
      <p className="text-xs text-gray-500 italic mb-1">{step.description}</p>
      <div className="text-xs text-gray-500 space-y-1">
        {step.model_used && <p>Model: {step.model_used}</p>}
        <p>Status: <span className={`font-medium ${statusColor}`}>{statusMessage}</span></p>
        {typeof step.confidence_score === 'number' && (
          <p>Confidence: {step.confidence_score.toFixed(2)}</p>
        )}
      </div>
      {typeof step.output_generated === 'string' && (
        <div className="mt-2">
          <p className="text-xs font-medium text-gray-600">Output:</p>
          <pre className="mt-1 p-2 text-xs bg-gray-100 rounded-sm overflow-x-auto max-h-40 whitespace-pre-wrap break-all">
            {step.output_generated}
          </pre>
        </div>
      )}
      {step.issues_identified?.length > 0 && (
        <div className="mt-2">
          <p className="text-xs font-medium text-red-500">Issues Identified:</p>
          <ul className="list-disc list-inside pl-2">
            {step.issues_identified.map((issue: string, idx: number) => (
              <li key={idx} className="text-xs text-red-400">{issue}</li>
            ))}
          </ul>
        </div>
      )}
    </li>
  );
};

const SelectedProvisionDetail = ({ provision, onClose }: { provision: Provision; onClose: () => void }) => (
  <section className="my-8 p-6 bg-indigo-50 border border-indigo-200 rounded-lg shadow-md">
    <div className="flex justify-between items-center mb-3">
      <h2 className="text-2xl font-semibold text-indigo-700">Selected Provision Details</h2>
      <button 
        onClick={onClose}
        className="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
      >
        Close
      </button>
    </div>
    <ProvisionContent provision={provision} />
  </section>
);

const ProvisionContent = ({ provision }: { provision: Provision }) => (
  <>
    <h3 className="text-xl font-medium text-gray-800 mb-1">{provision.title}</h3>
    <p className="text-sm text-gray-500 mb-1">ID: {provision.id} | Section: {provision.section}</p>
    <div className="prose prose-sm max-w-none mt-2 text-gray-700 bg-white p-3 rounded border border-gray-200">
      <ReactMarkdown>{provision.text}</ReactMarkdown>
    </div>
    {provision.roles_responsible?.length > 0 && (
      <div className="mt-3">
        <h4 className="text-md font-semibold text-gray-700">Responsible Roles:</h4>
        <ul className="list-disc list-inside text-sm text-gray-600">
          {provision.roles_responsible.map(roleId => <li key={roleId}>{roleId}</li>)}
        </ul>
      </div>
    )}
    {provision.tags?.length > 0 && (
      <div className="mt-3">
        <h4 className="text-md font-semibold text-gray-700">Tags:</h4>
        <div className="flex flex-wrap gap-2 mt-1">
          {provision.tags.map(tag => (
            <span key={tag} className="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded-full">
              {tag}
            </span>
          ))}
        </div>
      </div>
    )}
  </>
);

const ProvisionGraphSection = ({
  provisions,
  regulationTitle,
  onNodeClick
}: {
  provisions: Provision[];
  regulationTitle: string;
  onNodeClick: (provision: Provision) => void;
}) => (
  <section>
    <h2 className="text-2xl font-semibold mb-4">Provisions for {regulationTitle}</h2>
    {provisions.length > 0 ? (
      <div className="h-[600px] border rounded-lg shadow-lg overflow-hidden">
        <GraphViewer nodes={provisions} onNodeClick={onNodeClick} />
      </div>
    ) : (
      <p>No provisions found for this regulation.</p>
    )}
  </section>
);