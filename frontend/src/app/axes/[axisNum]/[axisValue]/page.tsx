export default async function AxisValuePage({ params }: { params: { axisNum: string, axisValue: string } }) {
  // Await params as recommended for Server Components
  const resolvedParams = await params; 

  // TODO: Replace with real API call when backend is ready
  // const nodes = await queryNodes({ axisFilters: { [resolvedParams.axisNum]: resolvedParams.axisValue } });
  return (
    <main className="p-8">
      <h2 className="text-2xl font-semibold mb-2">Axis {resolvedParams.axisNum}: {resolvedParams.axisValue}</h2>
      {/* TODO: Render nodes for this axis value */}
      <div className="text-gray-500">[Nodes for this axis value coming soon]</div>
    </main>
  );
}
