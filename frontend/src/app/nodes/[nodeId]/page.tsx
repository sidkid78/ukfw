import NodeDetailPanel from '../../../components/NodeDetailPanel';

export default async function NodePage({ params }: { params: { nodeId: string } }) {
  // TODO: Replace with real API call when backend is ready
  // const node = await getNode(params.nodeId);
  const node = {
    node_id: params.nodeId,
    label: 'Node label (mock)',
    description: 'Node description (mock)',
    pillar_id: 'Pillar1',
    axes: { axis1: 'Pillar1', axis9: 0.92 },
    metadata: {},
    simulation_roles: ['Knowledge Expert'],
    links: [],
  };
  return (
    <main className="p-8">
      <NodeDetailPanel node={node} />
    </main>
  );
}
