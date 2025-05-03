import { useState, useEffect } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  Node,
  Edge,
  Position
} from 'reactflow';
import 'reactflow/dist/style.css';

// Sample data (will be replaced with real data from the game)
const initialNodes: Node[] = [
  {
    id: 'cpu_package',
    data: { label: 'CPU Package' },
    position: { x: 250, y: 100 },
    className: 'node current'
  },
  {
    id: 'core1',
    data: { label: 'Core 1' },
    position: { x: 100, y: 200 },
    className: 'node unvisited'
  },
  {
    id: 'core2',
    data: { label: 'Core 2' },
    position: { x: 400, y: 200 },
    className: 'node unvisited'
  },
  {
    id: 'l3_cache',
    data: { label: 'L3 Cache' },
    position: { x: 250, y: 300 },
    className: 'node unvisited'
  },
  {
    id: 'memory_controller',
    data: { label: 'Memory Controller' },
    position: { x: 250, y: 400 },
    className: 'node unvisited'
  }
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: 'cpu_package', target: 'core1', animated: true },
  { id: 'e1-3', source: 'cpu_package', target: 'core2', animated: true },
  { id: 'e1-4', source: 'cpu_package', target: 'l3_cache', animated: true },
  { id: 'e4-5', source: 'l3_cache', target: 'memory_controller', animated: true }
];

// Custom node types can be defined here if needed
const nodeTypes = {};

function GameMap() {
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);

  // In a real implementation, we would fetch the current map data from the game
  useEffect(() => {
    // Example of updating node status based on game state
    const fetchMapData = async () => {
      try {
        // This would be a real API call in production
        // const response = await fetch('/api/map');
        // const data = await response.json();
        
        // For now, just simulate visited nodes
        const updatedNodes = nodes.map(node => {
          if (node.id === 'cpu_package') {
            return { ...node, className: 'node current' };
          } else if (Math.random() > 0.5) {
            return { ...node, className: 'node visited' };
          }
          return node;
        });
        
        setNodes(updatedNodes);
      } catch (error) {
        console.error('Error fetching map data:', error);
      }
    };
    
    // Update map every 5 seconds (for demo purposes)
    const interval = setInterval(fetchMapData, 5000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="map-container">
      <div className="map-title">Computer Architecture Map</div>
      <div className="map-content">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          fitView
        >
          <Controls />
          <MiniMap />
          <Background variant="dots" gap={12} size={1} />
        </ReactFlow>
      </div>
    </div>
  );
}

export default GameMap;